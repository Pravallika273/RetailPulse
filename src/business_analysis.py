from pathlib import Path
import pandas as pd


# ============================================================
# RETAILPULSE - BUSINESS ANALYSIS
# ============================================================

INPUT_FILE = Path(
    "data/processed/valid_sales.csv"
)

REPORT_DIR = Path("reports")


# ============================================================
# LOAD DATA
# ============================================================

def load_data():

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"File not found: {INPUT_FILE}"
        )

    df = pd.read_csv(
        INPUT_FILE,
        parse_dates=["InvoiceDate"],
        dtype={
            "InvoiceNo": "string",
            "StockCode": "string",
            "Description": "string",
            "CustomerID": "string",
            "Country": "string"
        }
    )

    return df


# ============================================================
# KPI SUMMARY
# ============================================================

def create_kpi_summary(df):

    total_revenue = df["Revenue"].sum()

    total_quantity = df["Quantity"].sum()

    total_orders = df["InvoiceNo"].nunique()

    total_customers = df["CustomerID"].nunique()

    total_products = df["StockCode"].nunique()

    average_order_value = (
        total_revenue / total_orders
    )

    average_units_per_order = (
        total_quantity / total_orders
    )

    # Customer identification at transaction-row level
    identified_customer_rows = (
        df["CustomerID"].notna().sum()
    )

    customer_identification_rate = (
        identified_customer_rows
        / len(df)
        * 100
    )

    # Revenue attributable to identified customers
    known_customer_revenue = df[
        df["CustomerID"].notna()
    ]["Revenue"].sum()

    customer_revenue_attribution = (
        known_customer_revenue
        / total_revenue
        * 100
    )

    # Orders attributable to identified customers
    known_customer_orders = df[
        df["CustomerID"].notna()
    ]["InvoiceNo"].nunique()

    customer_order_identification_rate = (
        known_customer_orders
        / total_orders
        * 100
    )

    kpi = pd.DataFrame({
        "Metric": [
            "Total Revenue",
            "Total Quantity",
            "Total Orders",
            "Unique Customers",
            "Unique Products",
            "Average Order Value",
            "Average Units Per Order",
            "Transaction Row Customer Identification Rate",
            "Order Customer Identification Rate",
            "Revenue Attributable to Identified Customers"
        ],
        "Value": [
            total_revenue,
            total_quantity,
            total_orders,
            total_customers,
            total_products,
            average_order_value,
            average_units_per_order,
            customer_identification_rate,
            customer_order_identification_rate,
            customer_revenue_attribution
        ]
    })

    return kpi


# ============================================================
# MONTHLY SALES
# ============================================================

def create_monthly_sales(df):

    monthly = (
        df.groupby("YearMonth")
        .agg(
            Revenue=("Revenue", "sum"),
            Quantity=("Quantity", "sum"),
            Orders=("InvoiceNo", "nunique"),
            Customers=("CustomerID", "nunique")
        )
        .reset_index()
    )

    monthly["AverageOrderValue"] = (
        monthly["Revenue"]
        / monthly["Orders"]
    )

    monthly["RevenueChangePct"] = (
        monthly["Revenue"]
        .pct_change()
        * 100
    )

    return monthly


# ============================================================
# PRODUCT SALES
# ============================================================

def create_product_sales(df):

    product = (
        df.groupby(
            ["StockCode", "Description"],
            dropna=False
        )
        .agg(
            Revenue=("Revenue", "sum"),
            Quantity=("Quantity", "sum"),
            Orders=("InvoiceNo", "nunique"),
            Customers=("CustomerID", "nunique")
        )
        .reset_index()
    )

    product["AverageRevenuePerOrder"] = (
        product["Revenue"]
        / product["Orders"]
    )

    product = product.sort_values(
        "Revenue",
        ascending=False
    )

    return product


# ============================================================
# COUNTRY SALES
# ============================================================

def create_country_sales(df):

    country = (
        df.groupby("Country")
        .agg(
            Revenue=("Revenue", "sum"),
            Quantity=("Quantity", "sum"),
            Orders=("InvoiceNo", "nunique"),
            Customers=("CustomerID", "nunique")
        )
        .reset_index()
    )

    country["AverageOrderValue"] = (
        country["Revenue"]
        / country["Orders"]
    )

    country["RevenueSharePct"] = (
        country["Revenue"]
        / country["Revenue"].sum()
        * 100
    )

    country = country.sort_values(
        "Revenue",
        ascending=False
    )

    return country


# ============================================================
# CUSTOMER SALES
# ============================================================

def create_customer_sales(df):

    customer = (
        df[df["CustomerID"].notna()]
        .groupby("CustomerID")
        .agg(
            Revenue=("Revenue", "sum"),
            Quantity=("Quantity", "sum"),
            Orders=("InvoiceNo", "nunique"),
            Products=("StockCode", "nunique")
        )
        .reset_index()
    )

    customer["AverageOrderValue"] = (
        customer["Revenue"]
        / customer["Orders"]
    )

    customer["CustomerType"] = customer[
        "Orders"
    ].apply(
        lambda x:
        "Repeat Customer"
        if x > 1
        else "One-Time Customer"
    )

    customer = customer.sort_values(
        "Revenue",
        ascending=False
    )

    return customer


# ============================================================
# PRODUCT CONCENTRATION
# ============================================================

def create_product_concentration(product):

    total_revenue = product["Revenue"].sum()

    top_10_revenue = (
        product.head(10)["Revenue"].sum()
    )

    top_20_revenue = (
        product.head(20)["Revenue"].sum()
    )

    concentration = pd.DataFrame({
        "Metric": [
            "Total Product Revenue",
            "Top 10 Product Revenue",
            "Top 20 Product Revenue",
            "Top 10 Revenue Share %",
            "Top 20 Revenue Share %"
        ],
        "Value": [
            total_revenue,
            top_10_revenue,
            top_20_revenue,
            top_10_revenue
            / total_revenue
            * 100,
            top_20_revenue
            / total_revenue
            * 100
        ]
    })

    return concentration


# ============================================================
# SAVE REPORTS
# ============================================================

def save_reports(
    kpi,
    monthly,
    product,
    country,
    customer,
    concentration
):

    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    kpi.to_csv(
        REPORT_DIR / "kpi_summary.csv",
        index=False
    )

    monthly.to_csv(
        REPORT_DIR / "monthly_sales.csv",
        index=False
    )

    product.to_csv(
        REPORT_DIR / "product_sales.csv",
        index=False
    )

    country.to_csv(
        REPORT_DIR / "country_sales.csv",
        index=False
    )

    customer.to_csv(
        REPORT_DIR / "customer_sales.csv",
        index=False
    )

    concentration.to_csv(
        REPORT_DIR / "product_concentration.csv",
        index=False
    )


# ============================================================
# PRINT BUSINESS FINDINGS
# ============================================================

def print_findings(
    kpi,
    monthly,
    product,
    country,
    customer,
    concentration
):

    print("\n")
    print("=" * 75)
    print("RETAILPULSE - BUSINESS INTELLIGENCE REPORT")
    print("=" * 75)

    print("\n--- CORE KPIs ---")

    print(
        kpi.to_string(index=False)
    )

    print("\n--- MONTHLY SALES ---")

    print(
        monthly[
            [
                "YearMonth",
                "Revenue",
                "Orders",
                "Customers",
                "AverageOrderValue",
                "RevenueChangePct"
            ]
        ].to_string(index=False)
    )

    print("\n--- TOP 10 PRODUCTS BY REVENUE ---")

    print(
        product[
            [
                "StockCode",
                "Description",
                "Revenue",
                "Quantity",
                "Orders"
            ]
        ]
        .head(10)
        .to_string(index=False)
    )

    print("\n--- TOP 10 COUNTRIES BY REVENUE ---")

    print(
        country[
            [
                "Country",
                "Revenue",
                "Orders",
                "Customers",
                "RevenueSharePct"
            ]
        ]
        .head(10)
        .to_string(index=False)
    )

    print("\n--- TOP 10 CUSTOMERS BY REVENUE ---")

    print(
        customer[
            [
                "CustomerID",
                "Revenue",
                "Orders",
                "Products",
                "CustomerType"
            ]
        ]
        .head(10)
        .to_string(index=False)
    )

    print("\n--- PRODUCT CONCENTRATION ---")

    print(
        concentration.to_string(index=False)
    )

    print("\n" + "=" * 75)
    print("BUSINESS ANALYSIS COMPLETE")
    print("=" * 75)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    data = load_data()

    kpi = create_kpi_summary(data)

    monthly = create_monthly_sales(data)

    product = create_product_sales(data)

    country = create_country_sales(data)

    customer = create_customer_sales(data)

    concentration = create_product_concentration(
        product
    )

    save_reports(
        kpi,
        monthly,
        product,
        country,
        customer,
        concentration
    )

    print_findings(
        kpi,
        monthly,
        product,
        country,
        customer,
        concentration
    )