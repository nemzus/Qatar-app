import os, sqlite3
from contextlib import contextmanager
DB_PATH = os.environ.get('DB_PATH', 'prices.db')
SEED = [
    ('Carrefour', 'Tomato Round 500g - Pack size By Weight', 3.50),
    ('Lulu', 'Local Tomatoes 1kg', 6.00),
    ('Al Meera', 'Premium Fresh Tomato Loose 1 Kilo', 5.50),
    ('Safari Mall', 'Cucumber Local kg', 3.00),
    ('Family Food Center', 'Fresh Tomato Pack 250g', 2.00)]

@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_PATH); conn.row_factory = sqlite3.Row
    try: yield conn; conn.commit()
    finally: conn.close()

def init_db():
    with get_connection() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT, store TEXT NOT NULL,
            raw_title TEXT NOT NULL, price_qar REAL NOT NULL,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        if conn.execute('SELECT COUNT(*) AS c FROM products').fetchone()['c'] == 0:
            conn.executemany('INSERT INTO products (store, raw_title, price_qar) VALUES (?,?,?)', SEED)