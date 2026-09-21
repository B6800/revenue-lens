"""Production-friendly browser dashboard served directly by FastAPI."""

DASHBOARD_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Revenue Lens | Retail Intelligence</title>
  <style>
    :root { --bg: #0b1020; --panel: #151d33; --line: #2a3656; --text: #eff5ff; --muted: #aab8d2; --blue: #5da9ff; --green: #47d7a4; --amber: #f7b955; }
    * { box-sizing: border-box; }
    body { margin: 0; min-height: 100vh; font-family: Inter, ui-sans-serif, system-ui, sans-serif; color: var(--text); background: radial-gradient(circle at top right, #1d3970 0, transparent 34rem), var(--bg); }
    main { max-width: 1180px; margin: 0 auto; padding: 48px 24px 72px; }
    header { display: flex; align-items: flex-start; justify-content: space-between; gap: 24px; margin-bottom: 34px; }
    .eyebrow { color: var(--green); text-transform: uppercase; font-size: .75rem; font-weight: 800; letter-spacing: .14em; margin: 0 0 8px; }
    h1 { font-size: clamp(2rem, 5vw, 3.6rem); letter-spacing: -.06em; margin: 0; }
    .intro { color: var(--muted); max-width: 680px; line-height: 1.6; margin: 13px 0 0; }
    button { border: 1px solid #4d78b6; border-radius: 10px; background: #2168c5; color: white; padding: 11px 16px; font-weight: 700; cursor: pointer; white-space: nowrap; }
    button:hover { background: #2f7be0; }
    .status { color: var(--muted); font-size: .9rem; min-height: 1.4rem; margin: -14px 0 20px; }
    .metrics { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 16px; }
    .card, .panel { border: 1px solid var(--line); background: color-mix(in srgb, var(--panel) 90%, transparent); border-radius: 16px; box-shadow: 0 18px 40px #00000020; }
    .card { padding: 20px; }
    .label { color: var(--muted); font-size: .85rem; margin: 0 0 9px; }
    .value { font-size: clamp(1.4rem, 3vw, 2rem); font-weight: 800; letter-spacing: -.04em; margin: 0; }
    .layout { display: grid; grid-template-columns: 1.25fr .75fr; gap: 20px; margin-top: 20px; }
    .panel { padding: 22px; overflow: hidden; }
    h2 { margin: 0 0 6px; font-size: 1.2rem; }
    .hint { color: var(--muted); font-size: .9rem; line-height: 1.5; margin: 0 0 18px; }
    table { border-collapse: collapse; width: 100%; font-size: .92rem; }
    th { color: var(--muted); text-align: left; font-size: .75rem; letter-spacing: .06em; text-transform: uppercase; }
    th, td { padding: 12px 8px; border-bottom: 1px solid var(--line); }
    td:last-child, th:last-child { text-align: right; }
    tr:last-child td { border-bottom: 0; }
    .badge { color: #1a1d12; background: var(--amber); border-radius: 999px; padding: 4px 8px; font-size: .72rem; font-weight: 800; }
    @media (max-width: 820px) { header { flex-direction: column; } .metrics { grid-template-columns: repeat(2, 1fr); } .layout { grid-template-columns: 1fr; } }
  </style>
</head>
<body>
  <main>
    <header>
      <div>
        <p class="eyebrow">Retail intelligence platform</p>
        <h1>Revenue Lens</h1>
        <p class="intro">A live decision dashboard for revenue performance, product demand, customer retention, and transactions that deserve a human review.</p>
      </div>
      <button id="refresh" type="button">Refresh data</button>
    </header>
    <p id="status" class="status">Loading analytics…</p>
    <section class="metrics" aria-label="Key metrics">
      <article class="card"><p class="label">Total revenue</p><p id="revenue" class="value">—</p></article>
      <article class="card"><p class="label">Transactions</p><p id="transactions" class="value">—</p></article>
      <article class="card"><p class="label">Unique customers</p><p id="customers" class="value">—</p></article>
      <article class="card"><p class="label">Repeat-customer rate</p><p id="repeat-rate" class="value">—</p></article>
    </section>
    <section class="layout">
      <article class="panel">
        <h2>Top products</h2>
        <p class="hint">Products ranked by revenue across the current reporting period.</p>
        <table><thead><tr><th>Product</th><th>Category</th><th>Units</th><th>Revenue</th></tr></thead><tbody id="products"></tbody></table>
      </article>
      <article class="panel">
        <h2>Review queue</h2>
        <p class="hint">Isolation Forest flags statistically unusual transactions. A score is a review signal, not proof of fraud.</p>
        <table><thead><tr><th>Transaction</th><th>Product</th><th>Revenue</th></tr></thead><tbody id="anomalies"></tbody></table>
      </article>
    </section>
  </main>
  <script>
    const money = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 });
    const escapeHtml = value => String(value).replace(/[&<>'"]/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[char]));
    async function loadDashboard() {
      const status = document.getElementById('status');
      status.textContent = 'Loading analytics…';
      try {
        const [overview, products, anomalies] = await Promise.all([
          fetch('/analytics/overview').then(response => response.json()),
          fetch('/analytics/products?limit=6').then(response => response.json()),
          fetch('/analytics/anomalies?limit=6').then(response => response.json()),
        ]);
        document.getElementById('revenue').textContent = money.format(overview.total_revenue);
        document.getElementById('transactions').textContent = overview.transactions.toLocaleString();
        document.getElementById('customers').textContent = overview.unique_customers.toLocaleString();
        document.getElementById('repeat-rate').textContent = `${overview.repeat_customer_rate}%`;
        document.getElementById('products').innerHTML = products.map(product => `<tr><td>${escapeHtml(product.product_name)}</td><td>${escapeHtml(product.category)}</td><td>${product.units_sold}</td><td>${money.format(product.revenue)}</td></tr>`).join('');
        document.getElementById('anomalies').innerHTML = anomalies.map(item => `<tr><td><span class="badge">${escapeHtml(item.transaction_id)}</span></td><td>${escapeHtml(item.product_name)}</td><td>${money.format(item.revenue)}</td></tr>`).join('');
        status.textContent = `Reporting period: ${overview.date_range.start} to ${overview.date_range.end}`;
      } catch (error) {
        status.textContent = 'Unable to load analytics. Refresh the page to retry.';
      }
    }
    document.getElementById('refresh').addEventListener('click', loadDashboard);
    loadDashboard();
  </script>
</body>
</html>"""
