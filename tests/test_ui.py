import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app as flask_app


def test_index_shows_console_for_localhost():
    client = flask_app.test_client()
    # emulate request coming from localhost
    resp = client.get('/', headers={'Host': '127.0.0.1:5000'})
    assert resp.status_code == 200
    html = resp.get_data(as_text=True)
    assert 'Console (local)' in html
    assert 'id="console"' in html
    assert 'id="consoleToggle"' in html
    assert 'Legend:' in html
    assert '▲ Up' in html
    # ensure remove button exists in client-side template code
    assert 'remove-btn' in html
    assert 'id="exportBtn"' in html


def test_index_hides_console_for_remote_host():
    client = flask_app.test_client()
    resp = client.get('/', headers={'Host': 'example.com'})
    assert resp.status_code == 200
    html = resp.get_data(as_text=True)
    assert 'Console (local)' not in html
    assert 'id="console"' not in html
    assert 'id="consoleToggle"' not in html
    assert 'id="exportBtn"' not in html
    assert 'Legend:' not in html
