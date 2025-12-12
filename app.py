from flask import Flask, render_template, jsonify, request
import yfinance as yf
from datetime import datetime

app = Flask(__name__)

# Default configuration
DEFAULT_STOCKS = ["COIN", "LULU"]


def fetch_price(ticker: str):
    try:
        t = yf.Ticker(ticker)
        # prefer fast_info for speed
        fi = getattr(t, "fast_info", None)
        if fi and "last_price" in fi:
            price = fi["last_price"]
        else:
            info = t.info or {}
            price = info.get("regularMarketPrice") or info.get("currentPrice")
        return price
    except Exception:
        return None


@app.route("/")
def index():
    # Render page; initial stocks and default refresh in seconds
    return render_template("index.html", stocks=DEFAULT_STOCKS, default_refresh=5)


@app.route("/api/quotes", methods=["GET"])
def api_quotes():
    # Accept tickers as comma-separated query param `tickers` or use default list
    tickers = request.args.get("tickers")
    if tickers:
        symbols = [t.strip().upper() for t in tickers.split(",") if t.strip()]
    else:
        symbols = DEFAULT_STOCKS

    results = []
    ts = datetime.utcnow().isoformat() + "Z"
    for s in symbols:
        price = fetch_price(s)
        results.append({"symbol": s, "price": price, "timestamp": ts})

    return jsonify({"quotes": results})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
