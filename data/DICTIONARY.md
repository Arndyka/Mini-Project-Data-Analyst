# RetailLens data dictionary

All rows are synthetic. Dates are ISO `YYYY-MM-DD`; money is integer IDR. The seed is 42 and order dates cover 2025.

| Table | Key | Fields |
| --- | --- | --- |
| customers | customer_id | Fictional `C0001` IDs, fictional region, joined date before the order window |
| products | product_id | Fictional `P001` IDs, generic product name, category and list price |
| orders | order_id | Customer FK, order date, Web/App/Store channel, completed/cancelled status |
| items | item_id | Order and product FKs, positive integer quantity, nonnegative unit price and item-level discount |
| returns | return_id | Item FK, refund amount and refund date, bounded by net item value and the reporting window |
| lines | order/item linkage | Order ID, customer ID, date, category, channel, gross, discount, refund and status; each source item contributes one row |

`Unknown` is an explicit category assigned to the deliberately empty product category. It remains visible in the dashboard and is counted in the quality report.

`reports/data_quality.csv` records table, record_id, reason and action (`quarantined` or `filled_unknown`). It includes the deliberate duplicate order/item, invalid customer link/date, negative item price, and missing category.

`reports/rfm_customers.csv`: customer_id, recency_days, distinct-order frequency, net monetary value, R/F/M scores and segment. Customers without completed orders do not enter RFM. Thresholds and the fixed 2026-01-01 reference appear in reports/insights.md.

`site/data.json` stores columns separately from compact row arrays. It contains only public simulated line records, computed summary metrics and quality counts. Browser code expands the arrays using the supplied column names.
