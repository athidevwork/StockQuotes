import os
import sys
import pytest

# Ensure repo root is on sys.path so `from app import app` works when pytest runs
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app as flask_app


class FakeTicker:
    def __init__(self, ticker):
        # expose both fast_info and info to mirror real object
        self.fast_info = {"last_price": 100.5}
        self.info = {"regularMarketPrice": 100.5}


class RaisingTicker:
    def __init__(self, ticker):
        raise RuntimeError("network error")


def test_api_quotes_returns_prices(monkeypatch):
    # Patch yfinance.Ticker used in app.fetch_price
    monkeypatch.setattr('app.yf.Ticker', FakeTicker)
    client = flask_app.test_client()
    resp = client.get('/api/quotes?tickers=AAPL,MSFT')
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'quotes' in data
    assert len(data['quotes']) == 2
    for q in data['quotes']:
        assert q['price'] == 100.5


def test_api_quotes_handles_errors(monkeypatch):
    monkeypatch.setattr('app.yf.Ticker', RaisingTicker)
    client = flask_app.test_client()
    resp = client.get('/api/quotes?tickers=FOO')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['quotes'][0]['price'] is None
