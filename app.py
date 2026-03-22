from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_URL = "https://api.exchangerate-api.com/v4/latest/{}"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        from_currency = request.form.get("from_currency").upper()
        to_currency = request.form.get("to_currency").upper()
        amount = request.form.get("amount")

        try:
            amount = float(amount)

            response = requests.get(API_URL.format(from_currency))
            data = response.json()

            rate = data["rates"].get(to_currency)

            if rate:
                result = round(amount * rate, 2)
            else:
                error = "Invalid target currency"

        except Exception as e:
            error = str(e)

    return render_template("index.html", result=result, error=error)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
