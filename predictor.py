import yfinance as yf
import matplotlib.pyplot as plt
import io
import base64
import requests

COMPANY_TO_TICKER = {
    "APPLE": "AAPL",
    "MICROSOFT": "MSFT",
    "GOOGLE": "GOOGL",
    "AMAZON": "AMZN",
    "TESLA": "TSLA",
}

# Fallback exchange rates (USD to target currency, approximate as of June 2025)
FALLBACK_RATES = {
    "INR": 83.50,
    "EUR": 0.93,
    "GBP": 0.79,
    "JPY": 149.20,
    "CAD": 1.36,
    "AUD": 1.50
}

def get_exchange_rate(currency):
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        data = response.json()
        return data['rates'].get(currency, FALLBACK_RATES.get(currency, 1.0))
    except:
        return FALLBACK_RATES.get(currency, 1.0)

def get_ticker_from_company(user_input):
    stock = yf.Ticker(user_input)
    try:
        stock.info
        return user_input
    except:
        user_input_upper = user_input.upper()
        return COMPANY_TO_TICKER.get(user_input_upper, None)

def predict_stock_price(ticker, currency="INR"):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1mo")
    
    if hist.empty:
        return None, None, None, currency

    price = hist['Close'][-1]
    usd_price = float(price)
    exchange_rate = get_exchange_rate(currency)
    converted_price = usd_price * exchange_rate

    img = io.BytesIO()
    plt.figure(figsize=(8, 4))
    plt.plot(hist.index, hist['Close'], label='Close Price', color='blue')
    plt.title(f'Stock Price for {ticker}')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)

    image_base64 = base64.b64encode(img.getvalue()).decode()
    graph_url = f"data:image/png;base64,{image_base64}"

    return usd_price, converted_price, graph_url, currency