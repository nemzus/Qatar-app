// Removed imports: useState is grabbed directly from the global React object, 
// and getCheapestPrices is already globally available via api.js

function SearchBox() {
  const [q, setQ] = React.useState('');
  const [data, setData] = React.useState(null);
  const [constErr, setErr] = React.useState('');

  async function onSearch(e) {
    e.preventDefault(); 
    setErr('');
    try {
      const r = await getCheapestPrices(q);
      if (r.notFound) { 
        setErr('No matching groceries found.'); 
        setData(null); 
      } else {
        setData(r);
      }
    } catch (err) { 
      setErr(err.message); 
    }
  }

  return (
    <div style={{ maxWidth: 600, margin: '2rem auto', fontFamily: 'system-ui', backgroundColor: '#1f2937', padding: '20px', borderRadius: '8px', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.5)' }}>
      <form onSubmit={onSearch} style={{ display: 'flex', gap: 8 }}>
        <input 
          value={q} 
          onChange={e => setQ(e.target.value)}
          placeholder='Search e.g. tomato' 
          style={{ flex: 1, padding: 10, borderRadius: '4px', border: '1px solid #4b5563', backgroundColor: '#374151', color: '#fff' }} 
        />
        <button type='submit' style={{ padding: '10px 16px', borderRadius: '4px', border: 'none', backgroundColor: '#2563eb', color: '#fff', cursor: 'pointer', fontWeight: 'bold' }}>Search</button>
      </form>
      
      {constErr && <p style={{ color: '#ef4444', marginTop: '12px' }}>{constErr}</p>}
      
      {data && (
        <div style={{ marginTop: '20px' }}>
          <h3 style={{ fontSize: '1.2rem', fontWeight: 'bold', marginBottom: '4px' }}>
            Cheapest: <span style={{ color: '#10b981' }}>{data.cheapest_store}</span> - QAR {data.lowest_price_qar} ({data.normalized_unit})
          </h3>
          <p style={{ color: '#9ca3af', fontSize: '0.9rem', marginBottom: '16px' }}>
            Potential savings: <span style={{ color: '#10b981', fontWeight: 'bold' }}>QAR {data.calculated_savings_qar}</span>
          </p>
          
          <table width='100%' cellPadding={8} style={{ borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.9rem' }}>
            <thead>
              <tr style={{ borderBottom: '2px solid #4b5563', color: '#9ca3af' }}>
                <th align='left'>Store</th>
                <th align='left'>Item</th>
                <th style={{ textAlign: 'center' }}>Listed Price</th>
                <th style={{ textAlign: 'center' }}>Per Base</th>
              </tr>
            </thead>
            <tbody>
              {data.deals.map((d, i) => (
                <tr key={i} style={{ borderBottom: '1px solid #374151' }}>
                  <td style={{ padding: '10px 4px' }}>{d.store}</td>
                  <td style={{ padding: '10px 4px', color: '#d1d5db' }}>{d.original_title}</td>
                  <td align='center' style={{ padding: '10px 4px' }}>QAR {d.listed_price}</td>
                  <td align='center' style={{ padding: '10px 4px', color: '#10b981' }}><b>QAR {d.normalized_base_price}</b></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

// Make SearchBox accessible globally to index.html mounting script
window.SearchBox = SearchBox;
