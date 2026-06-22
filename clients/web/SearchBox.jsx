import { useState } from 'react';
import { getCheapestPrices } from './api';
export default function SearchBox() {
  const [q, setQ] = useState('');
  const [data, setData] = useState(null);
  const [err, setErr] = useState('');
  async function onSearch(e) {
    e.preventDefault(); setErr('');
    try {
      const r = await getCheapestPrices(q);
      if (r.notFound) { setErr('No matching groceries found.'); setData(null); }
      else setData(r);
    } catch (e) { setErr(e.message); }
  }
  return (
    <div style={{ maxWidth: 600, margin: '2rem auto', fontFamily: 'system-ui' }}>
      <form onSubmit={onSearch} style={{ display: 'flex', gap: 8 }}>
        <input value={q} onChange={e => setQ(e.target.value)}
          placeholder='Search e.g. tomato' style={{ flex: 1, padding: 10 }} />
        <button type='submit' style={{ padding: '10px 16px' }}>Search</button>
      </form>
      {err && <p style={{ color: 'crimson' }}>{err}</p>}
      {data && (<div>
        <h3>Cheapest: {data.cheapest_store} - QAR {data.lowest_price_qar} ({data.normalized_unit})</h3>
        <p>Potential savings: QAR {data.calculated_savings_qar}</p>
        <table width='100%' cellPadding={6} style={{ borderCollapse: 'collapse' }}>
          <thead><tr><th align='left'>Store</th><th align='left'>Item</th><th>Listed</th><th>Per base</th></tr></thead>
          <tbody>{data.deals.map((d, i) => (
            <tr key={i} style={{ borderTop: '1px solid #eee' }}>
              <td>{d.store}</td><td>{d.original_title}</td>
              <td align='center'>{d.listed_price}</td>
              <td align='center'><b>{d.normalized_base_price}</b></td>
            </tr>))}</tbody>
        </table></div>)}
    </div>);
}