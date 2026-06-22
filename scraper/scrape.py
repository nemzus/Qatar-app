"""Daily scraper scaffold. Replace selectors per store. Respect robots.txt/ToS."""
import os, sqlite3
from playwright.sync_api import sync_playwright
DB_PATH = os.environ.get('DB_PATH', 'prices.db')
TARGETS = [{'store':'Carrefour',
    'url':'https://www.carrefourqatar.com/mafqat/en/c/F1600000',
    'item_sel':'[data-testid="product"]','title_sel':'[data-testid="product_name"]',
    'price_sel':'[data-testid="product_price"]'}]

def upsert(rows):
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT,
        store TEXT, raw_title TEXT, price_qar REAL, scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    for s in {r[0] for r in rows}: conn.execute('DELETE FROM products WHERE store = ?', (s,))
    conn.executemany('INSERT INTO products (store, raw_title, price_qar) VALUES (?,?,?)', rows)
    conn.commit(); conn.close()

def run():
    collected = []
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True); page = b.new_page()
        for t in TARGETS:
            try:
                page.goto(t['url'], timeout=60000)
                page.wait_for_selector(t['item_sel'], timeout=20000)
                for it in page.query_selector_all(t['item_sel']):
                    te = it.query_selector(t['title_sel']); pe = it.query_selector(t['price_sel'])
                    if not te or not pe: continue
                    title = te.inner_text().strip()
                    price = float(''.join(c for c in pe.inner_text() if c.isdigit() or c == '.') or 0)
                    if title and price > 0: collected.append((t['store'], title, price))
            except Exception as e: print(f"[warn] {t['store']} failed: {e}")
        b.close()
    if collected: upsert(collected); print(f'Saved {len(collected)} products')
    else: print('No products scraped - check selectors')

if __name__ == '__main__': run()