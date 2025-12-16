# Copilot instructions for StockQuotes

This repository is a small Flask single-page app that serves a static HTML page and a JSON quotes API. The goal of this doc is to give AI coding agents the immediate, practical knowledge needed to be productive here.

- **Big picture:** Browser loads `/` (template `templates/index.html`) and client-side JS polls `/api/quotes` with a comma-separated `tickers` query param. The server (`app.py`) uses `yfinance` to fetch prices and returns JSON of shape `{quotes:[{symbol, price, timestamp}]}`. Default symbols are defined in `DEFAULT_STOCKS`.

- **Key files:**
  - [app.py](app.py): Main Flask app and `fetch_price()` implementation.
  - [templates/index.html](templates/index.html): Minimal client-side UI and polling logic.
  - [requirements.txt](requirements.txt): Dependencies (Flask, yfinance, pandas).
  - [README.md](README.md): Setup and run commands.

- **Data flow & patterns:**
  - `index()` renders the template with `stocks` and `default_refresh` values.
  - Client JS keeps `symbols` (uppercased, deduplicated) and polls the API at the configured interval.
  - `api_quotes` reads `tickers` query param (comma-separated) or falls back to `DEFAULT_STOCKS`.
  - `fetch_price(ticker)` prefers `Ticker.fast_info['last_price']` for speed and falls back to `Ticker.info` fields if missing; it catches exceptions and returns `None` on failure (front-end displays `N/A`).

- **Important behaviors / gotchas to preserve when changing code:**
  - Null/failed prices are valid and intentional (returned as `null` in JSON and rendered as `N/A`).
  - `yfinance` is a network-dependent dependency; when adding tests or CI, mock `yfinance.Ticker` or `fetch_price` to avoid flakiness.
  - `app.py` runs with `debug=True` in `__main__` for local development; production should use a WSGI server if needed.

- **Developer workflows (explicit commands found in repo):**
  - Create and activate a venv, then `pip install -r requirements.txt` (see README).
  - Run locally: `python app.py` and visit `http://127.0.0.1:5000`.
  - Example API request: `curl "http://127.0.0.1:5000/api/quotes?tickers=AAPL,MSFT"` → returns JSON with `quotes` array.

- **Where to make typical changes:**
  - Add/remove default displayed symbols: edit `DEFAULT_STOCKS` in `app.py`.
  - Change initial refresh interval: change `default_refresh` value passed into the template (see `index()` in `app.py` and `refreshInput` default in `templates/index.html`).
  - To add server-side caching or rate-limiting, keep response shape the same (`quotes` array) so the UI continues to work unchanged.

- **Testing guidance (project specific):**
  - There are no tests yet. When adding tests, patch or mock `yfinance.Ticker` (or `fetch_price`) to assert API behavior deterministically. Example test target: `api_quotes` returns correct JSON shape for given tickers and handles missing symbols gracefully.

- **Conventions and style:**
  - Keep logic small and testable; `fetch_price` is intentionally the single place for yfinance access.
  - Preserve the simple JSON API contract so the client-side code needs minimal changes.

If anything here is unclear or you want me to expand examples (tests, CI notes, or mock patterns), tell me which area to elaborate.  
