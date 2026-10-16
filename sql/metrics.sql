-- Monetary values are integer IDR. Refunds are attributed to the original order.
WITH completed AS (SELECT * FROM lines WHERE status = 'completed'),
buyers AS (SELECT customer_id, COUNT(DISTINCT order_id) AS orders FROM completed GROUP BY customer_id),
totals AS (
 SELECT COALESCE(SUM(gross),0) gross, COALESCE(SUM(discount),0) discount,
 COALESCE(SUM(refund),0) refund, COUNT(DISTINCT order_id) orders,
 COUNT(DISTINCT customer_id) customers FROM completed
)
SELECT gross,discount,refund,gross-discount-refund AS net,orders,customers,
 CASE WHEN orders=0 THEN 0 ELSE 1.0*(gross-discount-refund)/orders END aov,
 COALESCE((SELECT 100.0*SUM(CASE WHEN orders>=2 THEN 1 ELSE 0 END)/COUNT(*) FROM buyers),0) repeat_rate
FROM totals;
