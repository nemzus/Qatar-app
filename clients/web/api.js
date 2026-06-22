const BASE_URL = import.meta.env.VITE_API_URL || 'https://your-server.example.com';
export async function getCheapestPrices(item) {
  const res = await fetch(`${BASE_URL}/search?query=${encodeURIComponent(item)}`);
  if (!res.ok) {
    if (res.status === 404) return { notFound: true, deals: [] };
    throw new Error(`API error ${res.status}`);
  }
  return res.json();
}