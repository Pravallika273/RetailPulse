#  RetailPulse — Retail Sales Intelligence & Data Quality Platform

> An end-to-end retail analytics project that transforms raw transactional data into validated business insights using Python, PostgreSQL, SQL and Power BI.

---

##  Project Overview

**RetailPulse** is an end-to-end retail analytics platform designed to demonstrate how raw transactional data can be transformed into a reliable, business-ready analytics solution.

The project covers the complete analytics workflow:

**Raw Data → Data Quality Validation → Data Cleaning → PostgreSQL → Star Schema → Business Analysis → Power BI**

The solution combines data engineering, analytics, database design and business intelligence to answer practical retail questions around revenue, customers, products, geography and data quality.

---

##  Business Problem

Retail transaction datasets often contain:

- Missing customer information
- Duplicate transactions
- Cancelled orders
- Invalid quantities
- Zero or invalid prices
- Incomplete reporting periods
- Product and customer concentration
- Geographic revenue concentration

Simply creating charts from raw data can therefore lead to misleading business conclusions.

RetailPulse addresses this problem by introducing a structured data-quality and analytics workflow before the data reaches the business dashboard.

---

##  Project Objectives

1. Validate and assess the quality of raw retail transaction data.
2. Clean and prepare reliable sales data for analysis.
3. Build a structured PostgreSQL analytics database.
4. Implement a dimensional star-schema model.
5. Calculate important retail KPIs and business metrics.
6. Identify high-performing products and customers.
7. Analyze geographic revenue concentration.
8. Identify unusual product-level sales patterns requiring investigation.
9. Build an interactive Power BI dashboard for management-level analysis.

---

#  Solution Architecture

```text
                 RAW RETAIL DATA
                       │
                       ▼
              ┌─────────────────┐
              │ Python Validation│
              │ & Data Profiling │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Data Cleaning &  │
              │ Transformation   │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Processed Sales  │
              │ Dataset          │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │   PostgreSQL    │
              │ Analytics DB    │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │   Star Schema   │
              │ Dimensions +    │
              │ Fact Table      │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Business        │
              │ Analysis & KPIs │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │    Power BI     │
              │ Interactive     │
              │ Dashboards      │
              └─────────────────┘