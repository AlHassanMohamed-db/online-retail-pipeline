# Online Retail Data Pipeline — Project Report

## Overview

This project implements an end-to-end data pipeline for a real-world e-commerce transaction dataset, covering data ingestion, quality assessment, cleaning, storage in a relational database, and analytical reporting using SQL.

**Tech Stack:** Python (pandas), SQL Server, SQLAlchemy/pyodbc, T-SQL

---

## 1. Data Source

- **Dataset:** UK-based online retail transactions (Dec 2010 – Dec 2011)
- **Volume:** 541,909 raw transaction records
- **Columns:** InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country

---

## 2. Data Quality Assessment

Initial profiling revealed several real-world data quality issues:

| Issue | Volume | Nature |
|---|---|---|
| Missing `CustomerID` | 135,080 rows (~25%) | Valid transactions, unknown customer |
| Negative `Quantity` | 9,288 rows (~1.7%) | Legitimate order cancellations (InvoiceNo prefixed with 'C') |
| Non-positive `UnitPrice` | 2,517 rows (~0.46%) | Likely data entry errors |

**Key distinction made:** Negative quantities represent a valid business event (returns), not corrupt data — while non-positive prices represent actual data errors. Treating these identically would have been a modeling mistake.

---

## 3. Cleaning Strategy

Rather than a single "drop nulls" approach, the data was split into three purpose-built tables:

- **`clean_sales`** (406,789 rows) — valid transactions with known customer and positive price; used as the primary analysis base
- **`unknown_customer_sales`** (132,603 rows) — valid sales lacking customer attribution; preserved for separate analysis
- **`suspicious_pricing`** (2,517 rows) — records with invalid pricing; retained for manual review rather than deletion

A row-count reconciliation check confirmed 406,789 + 132,603 + 2,517 = 541,909, verifying no data loss or duplication during the split.

---

## 4. Data Storage

All three tables were loaded into a SQL Server database (`OnlineRetailDB`) using SQLAlchemy + pyodbc, replacing manual CSV-based workflows with a queryable relational store suitable for downstream analysis and reporting tools.

---

## 5. Key Analytical Findings

**Geographic concentration**
United Kingdom accounts for ~91% of transactions and ~76% of total revenue (£6.77M of £8.91M gross), making it the dominant market by a wide margin.

**Customer value varies by purchase pattern, not just total spend**
Two customers with similar total spend (~£130K) showed opposite behavior: one made 248 small orders (frequent/loyal pattern), the other made 26 large orders (bulk/wholesale pattern) — suggesting the need for distinct engagement strategies per segment.

**Netherlands shows a distinct B2B-like signature**
Despite ranking outside the top 5 countries by transaction volume, the Netherlands has the highest average invoice value (£2,846), roughly 8x the UK average (£341) — with a sample size (100 invoices) large enough to be statistically meaningful, unlike several one-invoice countries with unreliable averages.

**Seasonal peak identified — with a data completeness caveat**
November 2011 was the strongest month by both order count (3,085) and revenue (£1.13M), consistent with pre-holiday shopping behavior. December 2011 appeared to show a sharp drop, but this was traced to incomplete data (the dataset ends December 9th) rather than an actual sales decline — daily order rates for November and December were in fact comparable (~103 vs ~102 orders/day).

**Return rate within normal range**
Returns totaled £611,342 against £8.91M gross sales — a 6.9% return rate, consistent with typical e-commerce benchmarks (5–10%), indicating no product quality red flags at the aggregate level.

---

## 6. Engineering Practices Applied

- Validated assumptions against raw data before trusting query output (e.g., diagnosing the "month 13–31" anomaly back to a data type issue)
- Distinguished statistically reliable aggregates (large sample) from unreliable ones (single-invoice countries) before drawing conclusions
- Verified data completeness (min/max date range) before interpreting a time-series trend
- Used reconciliation checks after every data split to guarantee no silent data loss

---

## 7. Next Steps

- Migrate ad hoc SQL exploration into version-controlled, parameterized scripts
- Add a proper project structure (config separated from credentials, requirements file, README)
- Extend analysis to product-level trends and the `unknown_customer_sales` segment
- Push to GitHub with clear documentation for portfolio use
