from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# API URL for real-time conversion
API_URL = "https://api.exchangerate-api.com/v4/latest/USD"
#API_URL="https://api.exchangerate.host/live?access_key=081698c657af15790b3052997852926c"

@app.route("/", methods=["GET", "POST"])
def index():
    converted_amount = None
    error_message = None

    if request.method == "POST":
        from_currency = request.form["from_currency"]
        to_currency = request.form["to_currency"]
        amount = request.form["amount"]

        if from_currency and to_currency and amount:
            try:
                response = requests.get(API_URL)
                data = response.json()

                if 'error' in data:
                    error_message = f"Error: {data['error']}"
                else:
                    # Get the rates for the selected currencies
                    rate_from = data['rates'].get(from_currency)
                    rate_to = data['rates'].get(to_currency)

                    if rate_from is None or rate_to is None:
                        error_message = "Currency code not supported."
                    else:
                        # Perform the conversion
                        amount = float(amount)
                        converted_amount = (amount / rate_from) * rate_to
            except requests.exceptions.RequestException as e:
                error_message = f"API error: {e}"

    return render_template("index.html", converted_amount=converted_amount, error_message=error_message)

if __name__ == "__main__":
    app.run(debug=True)
