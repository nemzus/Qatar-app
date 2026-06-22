import re
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from rapidfuzz import fuzz
from .db import get_connection, init_db, DB_PATH

app = FastAPI(title='Qatar Price Comparison Free Engine', version='1.0.0')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True,
                   allow_methods=['*'], allow_headers=['*'])

STOP_WORDS = {'fresh','premium','local','imported','promo','offer','pack','size',
              'by','weight','qatar','high','quality','chilled','special','loose'}

UNIT_PATTERNS = [
    (r'(\d+(?:\.\d+)?)\s*(?:kg|kilo|kilogram)', 'kg'),
    (r'(\d+(?:\.\d+)?)\s*(?:g|gr|gram|grams)', 'g'),
    (r'(\d+(?:\.\d+)?)\s*(?:l|ltr|litre|liter)', 'l'),
    (r'(\d+(?:\.\d+)?)\s*(?:ml)', 'ml'),
    (r'(\d+)\s*(?:pc|pcs|piece|pieces)', 'pcs'),
]

def extract_weight_and_normalize(title):
    t = title.lower(); weight = 1.0; unit_found = 'kg'
    for pattern, unit in UNIT_PATTERNS:
        m = re.search(pattern, t)
        if m:
            v = float(m.group(1))
            if unit == 'g': weight, unit_found = v / 1000.0, 'kg'
            elif unit == 'ml': weight, unit_found = v / 1000.0, 'l'
            else: weight, unit_found = v, unit
            t = re.sub(pattern, '', t); break
    return t.strip(), weight, unit_found

def clean_text_pipeline(text):
    text = re.sub(r'[^\w\s]', ' ', text.lower())
    return ' '.join(w for w in text.split() if w not in STOP_WORDS)

class Deal(BaseModel):
    store: str; original_title: str; listed_price: float
    normalized_base_price: float; detected_weight: str

class SearchResponse(BaseModel):
    search_term: str; cheapest_store: str; lowest_price_qar: float
    calculated_savings_qar: float; normalized_unit: str; deals: List[Deal]

@app.on_event('startup')
def _startup(): init_db()

@app.get('/health')
def health(): return {'status': 'ok', 'db': DB_PATH}

@app.get('/search', response_model=SearchResponse)
def search_groceries(query: str = Query(..., min_length=1), threshold: int = 75):
    cleaned_query = clean_text_pipeline(query); matched = []
    with get_connection() as conn:
        rows = conn.execute('SELECT store, raw_title, price_qar FROM products').fetchall()
    for row in rows:
        no_unit, weight, unit = extract_weight_and_normalize(row['raw_title'])
        score = fuzz.partial_ratio(cleaned_query, clean_text_pipeline(no_unit))
        if score >= threshold and weight > 0:
            matched.append({
                'store': row['store'], 'original_title': row['raw_title'],
                'listed_price': row['price_qar'],
                'normalized_base_price': round(row['price_qar'] / weight, 2),
                'detected_weight': f'{weight} {unit}'})
    if not matched:
        raise HTTPException(status_code=404, detail=f"No matching groceries found for '{query}'")
    deals = sorted(matched, key=lambda x: x['normalized_base_price'])
    savings = round(deals[-1]['normalized_base_price'] - deals[0]['normalized_base_price'], 2)
    return SearchResponse(search_term=query, cheapest_store=deals[0]['store'],
        lowest_price_qar=deals[0]['normalized_base_price'], calculated_savings_qar=savings,
        normalized_unit='per base kg/l/unit', deals=deals)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('app.main:app', host='0.0.0.0', port=8000, reload=True)