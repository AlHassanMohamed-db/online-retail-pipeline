/* ============================================================
   Online Retail Pipeline — Analytical Queries
   Run against: OnlineRetailDB (SQL Server)
   Purpose: Documents the exploratory SQL analysis performed on
            the clean_sales table, and the key insights each
            query produced (see README.md for the full write-up).
   ============================================================ */
-- 1. Top 10 best-selling products by quantity
SELECT   TOP 10 Description,
                sum(Quantity) AS Total_qty
FROM     clean_sales
GROUP BY Description
ORDER BY Total_qty DESC;

-- 2. Total revenue by country (top 10)
-- Insight: UK dominates (~76% of total revenue)
SELECT   TOP 10 Country,
                SUM(Quantity * UnitPrice) AS total_revenue
FROM     clean_sales
GROUP BY Country
ORDER BY total_revenue DESC;

-- 3. Average invoice value by country
-- Insight: Netherlands has the highest average invoice value (~£2,846),
-- suggesting a wholesale/B2B buying pattern rather than retail.
-- unique_invoices is included to flag countries with too few invoices
-- for the average to be statistically meaningful (e.g. single-invoice countries).
SELECT   Country,
         COUNT(DISTINCT InvoiceNo) AS unique_invoices,
         SUM(Quantity * UnitPrice) / COUNT(DISTINCT InvoiceNo) AS avg_invoice_value
FROM     clean_sales
GROUP BY Country
ORDER BY avg_invoice_value DESC;

-- 4. Monthly sales trend
-- Insight: November 2011 is the clear peak (pre-holiday shopping).
-- December 2011 appears to drop sharply, but the dataset ends Dec 9th,
-- so this reflects partial-month data, not an actual sales decline
-- (see query 5).
SELECT   FORMAT(InvoiceDate, 'yyyy-MM') AS sales_month,
         COUNT(DISTINCT InvoiceNo) AS num_invoices,
         SUM(Quantity * UnitPrice) AS total_revenue
FROM     clean_sales
GROUP BY FORMAT(InvoiceDate, 'yyyy-MM')
ORDER BY sales_month;

-- 5. Date range check (data completeness verification)
-- Confirms the dataset covers 2010-12-01 to 2011-12-09 (partial December).
SELECT MIN(InvoiceDate) AS earliest_date,
       MAX(InvoiceDate) AS latest_date
FROM   clean_sales;

-- 6. Top 10 customers by total spend
-- Insight: customers with similar total spend can have very different
-- buying patterns (frequent/small orders vs. rare/large orders),
-- suggesting different segments (loyal retail vs. wholesale-like).
SELECT   TOP 10 CustomerID,
                COUNT(DISTINCT InvoiceNo) AS num_orders,
                SUM(Quantity * UnitPrice) AS total_spent,
                SUM(Quantity * UnitPrice) / COUNT(DISTINCT InvoiceNo) AS avg_order_value
FROM     clean_sales
GROUP BY CustomerID
ORDER BY total_spent DESC;

-- 7. Gross sales vs. returns vs. net sales
-- Insight: return rate is ~6.9% of gross sales, within the typical
-- 5-10% e-commerce benchmark range.
SELECT SUM(CASE WHEN Quantity > 0 THEN Quantity * UnitPrice ELSE 0 END) AS gross_sales,
       SUM(CASE WHEN Quantity < 0 THEN Quantity * UnitPrice ELSE 0 END) AS total_returns,
       SUM(Quantity * UnitPrice) AS net_sales
FROM   clean_sales;