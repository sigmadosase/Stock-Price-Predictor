from flask import Flask, render_template, request
from predictor import predict_stock_price, get_ticker_from_company

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    price_usd = None
    price_converted = None
    currency = None
    graph_url = None
    error = None

    if request.method == "POST":
        user_input = request.form.get("ticker").strip().upper()
        currency = request.form.get("currency", "INR").upper()
        ticker = get_ticker_from_company(user_input)
        if ticker:
            usd_price, converted_price, graph_url, currency = predict_stock_price(ticker, currency)
            if usd_price is None:
                error = f"No data available for {user_input}. Please check the ticker or company name."
            else:
                price_usd = f"${usd_price:.2f}"
                price_converted = f"{get_currency_symbol(currency)}{converted_price:.2f}"
        else:
            error = f"Could not find ticker for {user_input}. Try using the stock ticker (e.g., AAPL) or a valid company name."

    return render_template("index.html", price_usd=price_usd, price_converted=price_converted, currency=currency, graph_url=graph_url, error=error)

def get_currency_symbol(currency):
    symbols = {
        "INR": "₹",
        "EUR": "€",
        "GBP": "£",
        "JPY": "¥",
        "CAD": "C$",
        "AUD": "A$"
    }
    return symbols.get(currency, currency)

if __name__ == "__main__":
    app.run(debug=True)