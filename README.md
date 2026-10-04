#  RetailPulse — Retail Sales Intelligence & Data Quality Platform

> An end-to-end retail analytics project that transforms raw transactional data into validated, business-ready insights using Python, PostgreSQL, SQL and Power BI.

---

##  Project Overview

**RetailPulse** is an end-to-end retail analytics platform designed to demonstrate how raw transactional data can be transformed into a reliable, business-ready analytics solution.

The project covers the complete analytics workflow:

**Raw Data → Data Quality Validation → Data Cleaning → PostgreSQL → Star Schema → Business Analysis → Power BI**

The solution combines data engineering, data analytics, database design and business intelligence to answer practical retail questions around:

- Revenue performance
- Customer value
- Product performance
- Geographic concentration
- Data quality
- Business anomalies

RetailPulse is a **portfolio case study** and does not use proprietary client or company data.

---

#  Business Problem

Retail transaction datasets can contain significant data-quality and analytical challenges, including:

- Missing customer information
- Duplicate transactions
- Cancelled orders
- Invalid quantities
- Zero or invalid prices
- Incomplete reporting periods
- Product concentration
- Customer concentration
- Geographic revenue concentration

Simply creating charts directly from raw data can therefore lead to misleading business conclusions.

RetailPulse addresses this problem by introducing a structured data-quality, database and analytics workflow before the data reaches the business dashboard.

---

#  Project Objectives

1. Validate and assess the quality of raw retail transaction data.
2. Clean and prepare reliable sales data for analysis.
3. Build a structured PostgreSQL analytics database.
4. Implement a dimensional star-schema model.
5. Calculate important retail KPIs and business metrics.
6. Identify high-performing products and customers.
7. Analyze geographic revenue concentration.
8. Identify unusual product-level sales patterns requiring investigation.
9. Build interactive Power BI dashboards for business analysis.

---

#  Technology Stack

| Area | Technology |
|---|---|
| Programming | Python |
| Data Processing | Pandas |
| Database | PostgreSQL 18 |
| Query Language | SQL |
| Business Intelligence | Microsoft Power BI |
| Data Source | UCI Online Retail Dataset |
| Development Environment | VS Code |
| Version Control | Git & GitHub |

---

#  Dataset

The project uses the **Online Retail** transactional dataset containing retail purchases recorded between December 2010 and December 2011.

## Original Dataset

| Attribute | Value |
|---|---:|
| Records | 541,909 |
| Columns | 8 |
| Unique Invoices | 25,900 |
| Unique Products | 4,070 |
| Unique Customers | 4,372 |
| Countries | 38 |
| Start Date | 2010-12-01 |
| End Date | 2011-12-09 |

## Original Columns

```text
InvoiceNo
StockCode
Description
Quantity
InvoiceDate
UnitPrice
CustomerID
Country