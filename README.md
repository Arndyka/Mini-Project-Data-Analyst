# RetailLens — Retail Performance & Customer Analytics

A reproducible data analyst case study by **Arnoldus Gratio Darryl Andyka**: synthetic data → validation → SQL/Python reconciliation → customer segmentation → an interactive dashboard.

[Open dashboard](https://arndyka.github.io/Mini-Project-Data-Analyst/) · [Analysis notebook](notebooks/retail_analysis.ipynb) · [Findings in Indonesian](reports/insights.md) · [Data dictionary](data/DICTIONARY.md) · [Portfolio](https://arndyka.github.io/Portofolio/)

**All customers, products and transactions are fictional.** This is an independent learning project, not client work, company performance, or evidence of a revenue improvement. The existing `Bike Buyers.xlsx` remains unchanged as the original Excel exercise.

## Business questions

- How do monthly net sales and average order value change?
- Which product categories and channels contribute to sales?
- How do repeat-purchase behavior and descriptive RFM segments differ?
- How do cancellations, discounts, refunds and data-quality problems affect the results?

## Reproduce

Requires Python 3.12+ and Node.js 22+ for browser-metric tests. No account, API key, paid service or private dataset is needed.

```sh
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m retaillens.build
python -m unittest discover -s tests -v
node --test tests/metrics.test.mjs
python -m http.server 4190 --directory site
```

Open <http://localhost:4190>. Do not double-click the HTML file: browsers need HTTP to fetch its JSON dataset. `python -m retaillens.build` regenerates the CSVs, SQLite database, quality report, findings, charts, notebook and public dashboard data with seed **42**. Run commands from the repository root.

Open `notebooks/retail_analysis.ipynb` in Jupyter or VS Code, select the Python environment and run every cell. An executed copy is available at [reports/executed_analysis.ipynb](reports/executed_analysis.ipynb). The generated SQLite database is local/ignored: after building, `sqlite3 data/retail.sqlite < sql/metrics.sql` runs the independent SQL calculation. Additional exploration queries are in `sql/exploration.sql`.

For browser tests, run `npm ci`, then `npx playwright install chromium` outside Windows. `npm test` runs pure metric tests; `npm run test:browser` starts its own local server and checks desktop/mobile interactions and accessibility. Windows uses the installed Edge browser.

## Deliverables

| Location | Purpose |
| --- | --- |
| `data/raw/` | Seeded relational source tables with deliberate bad records |
| `data/clean/` | Validated tables and a line-level analysis view |
| `reports/data_quality.csv` | Record-level issues and actions, not silent deletion |
| `reports/summary.json` | Computed KPIs, category/channel/month totals and RFM counts |
| `reports/rfm_customers.csv` | Fictional customer IDs with documented descriptive segments |
| `reports/charts/` | Standalone charts suitable for review |
| `sql/` | Metric reconciliation and exploration queries |
| `site/` | Static responsive dashboard with date/category/channel filters |
| `tests/` | Independently calculated metric fixtures and browser journeys |

## Metric contract

All source money is **integer Indonesian rupiah**, without floating-point accumulation. Displayed AOV is rounded only for presentation.

- Completed orders exclude cancelled orders. Counts use distinct IDs, not item rows.
- Gross sales = quantity × unit price on valid completed-order lines.
- Net sales = gross − item discounts − validated refunds.
- AOV = net sales / completed orders, including orders with a full refund.
- Repeat-purchase rate = customers with at least two completed orders / customers with any completed order. It is not cohort retention.
- Refunds are attributed to the original order date, not modeled as period cash flows. Discount/refund checks prevent negative line revenue.
- Date/category/channel filters scope the sales KPIs and charts. Category-filtered AOV reflects selected-category value per order containing that category, not the whole basket.
- RFM is separate: all-year 2025, reference date **1 January 2026**. Rules and thresholds are in the report and dashboard. It is not clustering, churn prediction or a measure of actual loyalty.

Invalid/duplicate rows are recorded and quarantined. Missing product categories become `Unknown` rather than an invented classification. Raw source files remain available. The synthetic corruption consists of additional malformed/duplicate records, not unknown missing business transactions; real-world ambiguous financial records would need source reconciliation before drawing conclusions.

## Interpretation limits

The generator intentionally weights year-end orders, creates repeat-buyer and dormant groups, and changes promotional discounts. These patterns are **simulation inputs**, not independent discoveries about retail. Refund timing is bounded to the simulation window. There are no real customer demographics, acquisition costs, product costs or profit margins. Suggested actions are hypotheses for future experiments, not measured outcomes.

The site is static and uses only this public synthetic dataset. It does not send data to an analytics service or load private account records. Source material for the owner's other portfolio projects is not included here.

## Checks and deployment

GitHub Actions regenerates the case study, runs Python and JavaScript metric tests, executes the notebook, checks the dashboard in Chromium and publishes only `site/` through GitHub Pages. Local browser testing uses Edge. See [verification notes](docs/verification.md) for the actual verification record and scope.

The original Bike Buyers workbook is retained as supplied. RetailLens code and newly generated fictional datasets are available under [MIT](LICENSE). That license does not assert ownership of the pre-existing workbook or its underlying dataset.
