from flask import Flask, render_template, jsonify, request
import yfinance as yf
from datetime import datetime, timezone

app = Flask(__name__)

# Default configuration
# Keep a compact list of commonly viewed tickers here. New tickers added per request.
DEFAULT_STOCKS = [
    "COIN", "LULU",
    "AAPL", "FDX", "MMM", "GME", "TEAM", "META", "DASH", "PYPL", "DIS",
    "ABNB", "HON", "NKE", "INTL", "ASAN", "AFRM", "BYND",
]


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
    host = request.host.split(':')[0]
    # show the debug console when running locally (localhost or 127.0.0.1) or when debug mode is on
    show_console = host in ("127.0.0.1", "localhost") or app.debug
    return render_template("index.html", stocks=DEFAULT_STOCKS, default_refresh=5, show_console=show_console)


@app.route("/api/quotes", methods=["GET"])
def api_quotes():
    # Accept tickers as comma-separated query param `tickers` or use default list
    tickers = request.args.get("tickers")
    if tickers:
        symbols = [t.strip().upper() for t in tickers.split(",") if t.strip()]
    else:
        symbols = DEFAULT_STOCKS

    results = []
    ts = datetime.now(timezone.utc).isoformat()
    for s in symbols:
        price = fetch_price(s)
        results.append({"symbol": s, "price": price, "timestamp": ts})

    return jsonify({"quotes": results})


if __name__ == "__main__":
    import os
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', '5000'))
    debug = os.environ.get('DEBUG', 'False').lower() in ('1', 'true', 'yes')
    # disable the reloader to avoid issues in background runs
    app.run(host=host, port=port, debug=debug, use_reloader=False)
