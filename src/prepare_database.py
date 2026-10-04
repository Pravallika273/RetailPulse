from pathlib import Path
import pandas as pd


# ============================================================
# RETAILPULSE - DATABASE PREPARATION
# ============================================================

INPUT_FILE = Path(
    "data/processed/valid_sales.csv"
)

OUTPUT_FILE = Path(
    "data/processed/final_sales.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

def load_data():

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Input file not found: {INPUT_FILE}"
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
# TRANSACTION CLASSIFICATION
# ============================================================

def classify_transactions(df):

    df["TransactionType"] = "SALE"

    # Negative quantities represent return/cancellation
    df.loc[
        df["Quantity"] < 0,
        "TransactionType"
    ] = "RETURN"

    # Zero or negative prices
    df.loc[
        df["UnitPrice"] <= 0,
        "TransactionType"
    ] = "INVALID_PRICE"

    # Cancellation invoice
    df.loc[
        df["InvoiceNo"]
        .str.upper()
        .str.startswith("C", na=False),
        "TransactionType"
    ] = "CANCELLATION"

    return df


# ============================================================
# PRODUCT CLASSIFICATION
# ============================================================

def classify_products(df):

    df["ProductType"] = "MERCHANDISE"

    # Postage-related records
    postage_mask = (
        df["Description"]
        .fillna("")
        .str.upper()
        .str.contains(
            "POSTAGE|DOTCOM POSTAGE|POST",
            regex=True,
            na=False
        )
    )

    df.loc[
        postage_mask,
        "ProductType"
    ] = "POSTAGE"

    # Manual transactions
    manual_mask = (
        df["StockCode"]
        .fillna("")
        .str.upper()
        .eq("M")
    )

    df.loc[
        manual_mask,
        "ProductType"
    ] = "MANUAL"

    return df


# ============================================================
# DATE ATTRIBUTES
# ============================================================

def create_date_attributes(df):

    df["Date"] = (
        df["InvoiceDate"]
        .dt.date
    )

    df["Year"] = (
        df["InvoiceDate"]
        .dt.year
    )

    df["Month"] = (
        df["InvoiceDate"]
        .dt.month
    )

    df["MonthName"] = (
        df["InvoiceDate"]
        .dt.strftime("%B")
    )

    df["Quarter"] = (
        "Q"
        + df["InvoiceDate"]
        .dt.quarter
        .astype(str)
    )

    df["YearMonth"] = (
        df["InvoiceDate"]
        .dt.to_period("M")
        .astype(str)
    )

    return df


# ============================================================
# REPORTING PERIOD STATUS
# ============================================================

def create_period_status(df):

    max_date = df["InvoiceDate"].max()

    max_year = max_date.year
    max_month = max_date.month

    df["IsPartialPeriod"] = (
        (df["Year"] == max_year)
        & (df["Month"] == max_month)
    )

    return df


# ============================================================
# FINAL COLUMN SELECTION
# ============================================================

def select_columns(df):

    columns = [
        "InvoiceNo",
        "StockCode",
        "Description",
        "Quantity",
        "InvoiceDate",
        "Date",
        "Year",
        "Month",
        "MonthName",
        "Quarter",
        "YearMonth",
        "UnitPrice",
        "Revenue",
        "CustomerID",
        "Country",
        "TransactionType",
        "ProductType",
        "IsPartialPeriod"
    ]

    return df[columns]


# ============================================================
# SAVE
# ============================================================

def save_data(df):

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("RETAILPULSE - DATABASE PREPARATION")
    print("=" * 70)

    df = load_data()

    print(f"\nInput rows: {len(df):,}")

    df = classify_transactions(df)

    df = classify_products(df)

    df = create_date_attributes(df)

    df = create_period_status(df)

    df = select_columns(df)

    save_data(df)

    print("\nTRANSACTION TYPES")

    print(
        df["TransactionType"]
        .value_counts()
        .to_string()
    )

    print("\nPRODUCT TYPES")

    print(
        df["ProductType"]
        .value_counts()
        .to_string()
    )

    print("\nPARTIAL PERIOD")

    print(
        df.groupby("YearMonth")[
            "IsPartialPeriod"
        ]
        .first()
        .to_string()
    )

    print("\nFINAL DATASET")

    print(f"Rows    : {len(df):,}")
    print(f"Columns : {len(df.columns)}")

    print(f"\nCreated:")
    print(OUTPUT_FILE)

    print("\n" + "=" * 70)
    print("DATABASE PREPARATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()