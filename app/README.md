# Qatar Price Comparison Engine (Free / Deterministic)

Rule-based grocery price comparison across Qatar stores. No paid AI - RapidFuzz
string matching + unit normalization. FastAPI + SQLite + Playwright scraper +
GitHub Actions daily cron. Clients for Flutter (iOS/Android) and React (web).

## Run locally
```
pip install -r requirements.txt
uvicorn app.main:app --reload
# http://localhost:8000/docs   |   http://localhost:8000/search?query=tomato
```

## How it works
1. Clean each title (stop-words + punctuation stripped).
2. Extract weight/size, normalize to base unit (kg / l / pcs).
3. Divide price by base weight -> comparable price-per-kg.
4. RapidFuzz partial_ratio matches query vs cleaned titles (>=75).
5. Sort by normalized price; savings = dearest - cheapest.

## Fixes vs. the original draft
- @get -> @app.get (the draft would not start).
- Decimal weights parse now (1.5kg, 0.5 l).
- Litre/ml support added.
- In-memory list -> real SQLite table.
- Savings/lowest-price computed consistently (draft sample JSON was inconsistent).

## Deploy free
- Backend: Render free tier (render.yaml) / Koyeb / Oracle always-free.
- DB: SQLite file committed to repo (or Render disk).
- Scraper: GitHub Actions runs 04:00 UTC daily, refreshes prices.db, commits it.

## Scraper note
scraper/scrape.py is a scaffold - replace the CSS selectors per store with real ones.