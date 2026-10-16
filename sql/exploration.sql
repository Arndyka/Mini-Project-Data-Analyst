-- Run after python -m retaillens.build using data/retail.sqlite.
-- Net sales is calculated on completed orders; integer IDR throughout.
SELECT substr(date,1,7) month,COUNT(DISTINCT order_id) orders,
 SUM(gross-discount-refund) net_sales
FROM lines WHERE status='completed' GROUP BY month ORDER BY month;

SELECT category,channel,COUNT(DISTINCT order_id) orders,
 SUM(gross) gross_sales,SUM(discount) discounts,SUM(refund) refunds,
 SUM(gross-discount-refund) net_sales
FROM lines WHERE status='completed' GROUP BY category,channel ORDER BY net_sales DESC;

SELECT customer_id,CAST(julianday('2026-01-01')-julianday(MAX(date)) AS INTEGER) recency_days,
 COUNT(DISTINCT order_id) frequency,SUM(gross-discount-refund) monetary
FROM lines WHERE status='completed' GROUP BY customer_id ORDER BY monetary DESC;
