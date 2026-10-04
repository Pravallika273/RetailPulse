from pathlib import Path
import pandas as pd


RAW_FILE = Path("data/raw/Online Retail.xlsx")
CLEAN_FILE = Path("data/processed/retail_cleaned.csv")
VALID_FILE = Path("data/processed/valid_sales.csv")

REPORT_FILE = Path(
    "reports/data_quality_report.csv"
)


def load_data():

    raw = pd.read_excel(RAW_FILE)
    clean = pd.read_csv(
        CLEAN_FILE,
        parse_dates=["InvoiceDate"]
    )
    valid = pd.read_csv(
        VALID_FILE,
        parse_dates=["InvoiceDate"]
    )

    return raw, clean, valid


def build_report(raw, clean, valid):

    report = []

    # --------------------------------------------------
    # 1. Raw records
    # --------------------------------------------------

    report.append({
        "Category": "Dataset",
        "Issue": "Raw transaction records",
        "Count": len(raw),
        "Percentage": 100.0,
        "Business_Impact":
            "Baseline transaction volume"
    })

    # --------------------------------------------------
    # 2. Duplicate records
    # --------------------------------------------------

    duplicate_count = raw.duplicated().sum()

    report.append({
        "Category": "Data Quality",
        "Issue": "Exact duplicate records",
        "Count": duplicate_count,
        "Percentage":
            duplicate_count / len(raw) * 100,
        "Business_Impact":
            "Can inflate transaction-level reporting"
    })

    # --------------------------------------------------
    # 3. Missing descriptions
    # --------------------------------------------------

    missing_description = raw["Description"].isna().sum()

    report.append({
        "Category": "Data Quality",
        "Issue": "Missing product descriptions",
        "Count": missing_description,
        "Percentage":
            missing_description / len(raw) * 100,
        "Business_Impact":
            "Reduces product-level reporting quality"
    })

    # --------------------------------------------------
    # 4. Missing customer IDs
    # --------------------------------------------------

    missing_customer = raw["CustomerID"].isna().sum()

    report.append({
        "Category": "Data Quality",
        "Issue": "Missing customer IDs",
        "Count": missing_customer,
        "Percentage":
            missing_customer / len(raw) * 100,
        "Business_Impact":
            "Prevents customer-level attribution"
    })

    # --------------------------------------------------
    # 5. Negative quantities
    # --------------------------------------------------

    negative_quantity = (
        raw["Quantity"] < 0
    ).sum()

    report.append({
        "Category": "Business Exception",
        "Issue": "Negative quantities",
        "Count": negative_quantity,
        "Percentage":
            negative_quantity / len(raw) * 100,
        "Business_Impact":
            "Likely represents returns/cancellations"
    })

    # --------------------------------------------------
    # 6. Zero prices
    # --------------------------------------------------

    zero_price = (
        raw["UnitPrice"] == 0
    ).sum()

    report.append({
        "Category": "Data Quality",
        "Issue": "Zero unit prices",
        "Count": zero_price,
        "Percentage":
            zero_price / len(raw) * 100,
        "Business_Impact":
            "Transactions contribute no positive sales value"
    })

    # --------------------------------------------------
    # 7. Negative prices
    # --------------------------------------------------

    negative_price = (
        raw["UnitPrice"] < 0
    ).sum()

    report.append({
        "Category": "Data Quality",
        "Issue": "Negative unit prices",
        "Count": negative_price,
        "Percentage":
            negative_price / len(raw) * 100,
        "Business_Impact":
            "Requires investigation before sales reporting"
    })

    # --------------------------------------------------
    # 8. Cancellation invoices
    # --------------------------------------------------

    cancellation_count = (
        raw["InvoiceNo"]
        .astype(str)
        .str.upper()
        .str.startswith("C")
        .sum()
    )

    report.append({
        "Category": "Business Exception",
        "Issue": "Cancellation invoices",
        "Count": cancellation_count,
        "Percentage":
            cancellation_count / len(raw) * 100,
        "Business_Impact":
            "Should not be treated as normal sales"
    })

    # --------------------------------------------------
    # 9. Clean transactions
    # --------------------------------------------------

    report.append({
        "Category": "Pipeline",
        "Issue": "Records after duplicate removal",
        "Count": len(clean),
        "Percentage":
            len(clean) / len(raw) * 100,
        "Business_Impact":
            "Clean transaction base"
    })

    # --------------------------------------------------
    # 10. Valid sales
    # --------------------------------------------------

    report.append({
        "Category": "Pipeline",
        "Issue": "Valid sales records",
        "Count": len(valid),
        "Percentage":
            len(valid) / len(raw) * 100,
        "Business_Impact":
            "Primary dataset for sales analytics"
    })

    # --------------------------------------------------
    # 11. Revenue
    # --------------------------------------------------

    valid_revenue = valid["Revenue"].sum()

    report.append({
        "Category": "Business KPI",
        "Issue": "Valid sales revenue",
        "Count": valid_revenue,
        "Percentage": None,
        "Business_Impact":
            "Primary revenue baseline"
    })

    # --------------------------------------------------
    # 12. Orders
    # --------------------------------------------------

    valid_orders = valid["InvoiceNo"].nunique()

    report.append({
        "Category": "Business KPI",
        "Issue": "Valid sales invoices",
        "Count": valid_orders,
        "Percentage": None,
        "Business_Impact":
            "Primary order-count baseline"
    })

    # --------------------------------------------------
    # Create dataframe
    # --------------------------------------------------

    report_df = pd.DataFrame(report)

    return report_df


def main():

    print("=" * 70)
    print("RETAILPULSE - DATA QUALITY REPORT")
    print("=" * 70)

    raw, clean, valid = load_data()

    report = build_report(
        raw,
        clean,
        valid
    )

    REPORT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    report.to_csv(
        REPORT_FILE,
        index=False
    )

    print("\nREPORT CREATED:")
    print(REPORT_FILE)

    print("\nSUMMARY")
    print(report.to_string(index=False))

    print("\n" + "=" * 70)
    print("DATA QUALITY REPORT COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()