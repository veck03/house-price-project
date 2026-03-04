const API = 'http://127.0.0.1:8000';

// Check API status on page load
async function checkStatus() {
  const dot = document.getElementById('statusDot');
  const txt = document.getElementById('statusText');
  try {
    const r = await fetch(API + '/');
    if (r.ok) {
      dot.className = 'status-dot online';
      txt.textContent = 'api online';
    } else {
      dot.className = 'status-dot offline';
      txt.textContent = 'api error';
    }
  } catch {
    dot.className = 'status-dot offline';
    txt.textContent = 'api offline';
  }
}

checkStatus();

// Predict function
async function predict() {
  const btn     = document.getElementById('predictBtn');
  const priceEl = document.getElementById('priceDisplay');
  const metaEl  = document.getElementById('resultMeta');
  const errEl   = document.getElementById('errorMsg');

  const fields = [
    'MS Zoning', 'Neighborhood', 'Lot Area', 'MS SubClass',
    'Overall Qual', 'Overall Cond', 'Exter Qual', 'Kitchen Qual',
    'Gr Liv Area', 'Total Bsmt SF', '1st Flr SF', '2nd Flr SF',
    'Full Bath', 'Half Bath', 'Bedroom AbvGr', 'TotRms AbvGrd',
    'Year Built', 'Year Remod/Add', 'Garage Cars', 'Garage Area', 'Fireplaces'
  ];

  // Gather input values
  const data = {};
  for (const f of fields) {
    const el = document.getElementById(f);
    data[f] = el.tagName === 'SELECT' ? el.value : parseFloat(el.value) || 0;
  }

  // Loading state
  btn.disabled = true;
  btn.textContent = 'Estimating...';
  priceEl.className = 'price-display loading';
  priceEl.textContent = '...';
  errEl.className = 'error-msg';
  metaEl.className = 'result-meta';

  try {
    const res = await fetch(API + '/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ data })
    });

    if (!res.ok) throw new Error('Server error ' + res.status);

    const json  = await res.json();
    const price = json.predicted_price;

    priceEl.textContent = '$' + price.toLocaleString('en-US', { maximumFractionDigits: 0 });
    priceEl.className   = 'price-display visible';

    const now = new Date().toLocaleTimeString();
    metaEl.textContent = `Prediction made at ${now} based on ${fields.length} input features.`;
    metaEl.className   = 'result-meta visible';

  } catch (e) {
    priceEl.textContent = '—';
    priceEl.className   = 'price-display';
    errEl.textContent   = 'Could not reach API. Make sure uvicorn is running on port 8000.';
    errEl.className     = 'error-msg visible';
  }

  btn.disabled        = false;
  btn.textContent     = 'Estimate Price →';
}