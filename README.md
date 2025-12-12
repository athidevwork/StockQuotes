# StockQuotes

Simple Flask app showing live stock quotes for a configurable list of symbols. Defaults to COIN and LULU.

Getting started

1. Create and activate a virtualenv (macOS/Linux):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python app.py
```

Open http://127.0.0.1:5000 in your browser. Add symbols and set refresh seconds on the page.

To push to a remote repository, create a new repository on Git hosting (e.g., GitHub) and add it as a remote:

```bash
git init
git add .
git commit -m "Initial commit: StockQuotes Flask app"
git remote add origin <your-repo-url>
git push -u origin main
```
