// Set your live backend url directly
const BASE_URL = 'https://qatar-grocery-app.onrender.com';

async function getCheapestPrices(item) {
  // FIXED: Changed ?query= to ?term= to match your python backend exact rule
  const res = await fetch(`${BASE_URL}/search?term=${encodeURIComponent(item)}`);
  
  if (!res.ok) {
    if (res.status === 404) return { notFound: true, deals: [] };
    throw new Error(`API error ${res.status}`);
  }
  return res.json();
}
