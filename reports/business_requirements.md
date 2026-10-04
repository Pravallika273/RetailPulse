# RetailPulse — Business Requirements

## 1. Project Context

RetailPulse is a simulated retail analytics solution built using
the UCI Online Retail dataset.

The objective is to transform raw transaction data into a
validated, business-ready analytics platform.

---

# 2. Business Problems Identified

## 2.1 Data Quality

The raw transaction dataset contains:

- Exact duplicate records
- Missing customer identifiers
- Missing product descriptions
- Negative quantities
- Zero-price transactions
- Negative-price transactions
- Cancellation transactions

These issues must be identified before business reporting.

---

## 2.2 Customer Attribution

Customer identification is incomplete.

The current analysis shows:

- 74.82% transaction-row customer identification
- 92.85% order-level customer identification
- 83.51% revenue attributable to identified customers

Customer analytics must therefore expose customer-data coverage.

---

## 2.3 Geographic Revenue Concentration

The United Kingdom contributes approximately 84.59% of
recorded revenue.

The dashboard should allow management to monitor revenue
distribution by country.

---

## 2.4 Partial Reporting Period

The dataset ends on December 9, 2011.

December 2011 is therefore an incomplete reporting period.

The analytics system must distinguish complete and partial
periods to avoid misleading comparisons.

---

## 2.5 Product Classification

The transaction data contains entries such as:

- Merchandise
- Postage
- Manual/service-related records

The dashboard should distinguish merchandise from
non-merchandise transaction types.

---

## 2.6 Transaction Anomalies

Some products show unusual relationships between:

- Quantity
- Revenue
- Order count

For example, one product currently shows very high quantity
relative to its number of orders.

The system should identify such unusual transactions for
investigation rather than automatically treating them as errors.

---

# 3. Business Objectives

1. Build a reproducible data-quality pipeline.
2. Create a validated sales dataset.
3. Create a PostgreSQL analytical database.
4. Build reusable SQL analytics.
5. Create an interactive Power BI dashboard.
6. Monitor revenue and transaction anomalies.
7. Provide management-ready insights.
8. Maintain reconciliation between Python, SQL and Power BI.

---

# 4. Core KPIs

- Total Revenue
- Total Quantity
- Total Orders
- Unique Customers
- Unique Products
- Average Order Value
- Average Units per Order
- Customer Identification Rate
- Revenue Attribution Rate
- Revenue by Month
- Revenue by Country
- Revenue by Product
- Customer Revenue
- Cancellation Activity
- Revenue Change %
- Revenue Share %

---

# 5. Technical Requirements

## Data Pipeline

Raw Excel
→ Validation
→ Cleaning
→ Processed Dataset

## Database

Python
→ PostgreSQL
→ SQL Analytics

## Visualization

PostgreSQL
→ Power BI
→ Executive Dashboard

## Quality Assurance

Python KPI
=
SQL KPI
=
Power BI KPI

---

# 6. Technology Stack

- Python
- Pandas
- PostgreSQL
- SQL
- Power BI
- Microsoft Excel
- Git
- GitHub