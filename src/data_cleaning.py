from pathlib import Path
import pandas as pd


# =========================================================
# RETAILPULSE - DATA CLEANING PIPELINE
# =========================================================

RAW_FILE = Path("data/raw/Online Retail.xlsx")
OUTPUT_FILE = Path("data/processed/retail_cleaned.csv")


def load_raw_data():
    """Load the untouched raw Excel dataset."""

    if not RAW_FILE.exists():
        raise FileNotFoundError(
            f"Raw file not found: {RAW_FILE}"
        )

    df = pd.read_excel(RAW_FILE)

    print(f"Raw rows loaded: {len(df):,}")

    return df


def clean_data(df):
    """Clean and transform the raw retail dataset."""

    df = df.copy()

    # -----------------------------------------------------
    # 1. Standardize column names
    # -----------------------------------------------------

    df.columns = [
        column.strip()
        for column in df.columns
    ]

    # -----------------------------------------------------
    # 2. Remove exact duplicate records
    # -----------------------------------------------------

    duplicate_count = df.duplicated().sum()

    print(
        f"Exact duplicate rows removed: "
        f"{duplicate_count:,}"
    )

    df = df.drop_duplicates()

    # -----------------------------------------------------
    # 3. Standardize text fields
    # -----------------------------------------------------

    df["InvoiceNo"] = (
        df["InvoiceNo"]
        .astype(str)
        .str.strip()
    )

    df["StockCode"] = (
        df["StockCode"]
        .astype(str)
        .str.strip()
    )

    df["Description"] = (
        df["Description"]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    df["Country"] = (
        df["Country"]
        .astype("string")
        .str.strip()
    )

    # -----------------------------------------------------
    # 4. Convert dates
    # -----------------------------------------------------

    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"],
        errors="coerce"
    )

    # -----------------------------------------------------
    # 5. Create cancellation flag
    # -----------------------------------------------------

    df["IsCancelled"] = (
        df["InvoiceNo"]
        .str.upper()
        .str.startswith("C")
    )

    # -----------------------------------------------------
    # 6. Create return / negative quantity flag
    # -----------------------------------------------------

    df["IsNegativeQuantity"] = (
        df["Quantity"] < 0
    )

    # -----------------------------------------------------
    # 7. Create invalid price flag
    # -----------------------------------------------------

    df["IsInvalidPrice"] = (
        df["UnitPrice"] <= 0
    )

    # -----------------------------------------------------
    # 8. Create revenue
    # -----------------------------------------------------

    df["Revenue"] = (
        df["Quantity"] * df["UnitPrice"]
    )

    # -----------------------------------------------------
    # 9. Create date dimensions
    # -----------------------------------------------------

    df["Year"] = df["InvoiceDate"].dt.year

    df["Month"] = df["InvoiceDate"].dt.month

    df["MonthName"] = (
        df["InvoiceDate"]
        .dt.strftime("%B")
    )

    df["YearMonth"] = (
        df["InvoiceDate"]
        .dt.strftime("%Y-%m")
    )

    # -----------------------------------------------------
    # 10. Customer ID formatting
    # -----------------------------------------------------

    df["CustomerID"] = (
        df["CustomerID"]
        .astype("Int64")
    )

    # -----------------------------------------------------
    # 11. Missing description
    # -----------------------------------------------------

    df["Description"] = (
        df["Description"]
        .fillna("UNKNOWN PRODUCT")
    )

    return df


def create_valid_sales_dataset(df):
    """
    Create a business-ready sales dataset.

    A valid sale must:
    - not be cancelled
    - have positive quantity
    - have positive unit price
    """

    sales_df = df[
        (df["IsCancelled"] == False)
        & (df["Quantity"] > 0)
        & (df["UnitPrice"] > 0)
    ].copy()

    return sales_df


def save_outputs(df, sales_df):
    """Save processed datasets."""

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Full cleaned transaction dataset
    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    # Valid sales dataset
    sales_file = Path(
        "data/processed/valid_sales.csv"
    )

    sales_df.to_csv(
        sales_file,
        index=False
    )

    print("\nFILES CREATED")
    print(
        f"Cleaned transactions: "
        f"{OUTPUT_FILE}"
    )
    print(
        f"Valid sales: "
        f"{sales_file}"
    )


def print_summary(raw_df, clean_df, sales_df):
    """Print pipeline summary."""

    print("\n" + "=" * 70)
    print("RETAILPULSE - CLEANING SUMMARY")
    print("=" * 70)

    print(
        f"\nRaw rows: "
        f"{len(raw_df):,}"
    )

    print(
        f"After duplicate removal: "
        f"{len(clean_df):,}"
    )

    print(
        f"Valid sales rows: "
        f"{len(sales_df):,}"
    )

    print(
        f"Removed duplicate rows: "
        f"{len(raw_df) - len(clean_df):,}"
    )

    print(
        f"Excluded from valid sales: "
        f"{len(clean_df) - len(sales_df):,}"
    )

    print(
        f"\nValid sales revenue: "
        f"£{sales_df['Revenue'].sum():,.2f}"
    )

    print(
        f"Valid sales quantity: "
        f"{sales_df['Quantity'].sum():,}"
    )

    print(
        f"Valid invoices: "
        f"{sales_df['InvoiceNo'].nunique():,}"
    )

    print(
        f"Customers with IDs: "
        f"{sales_df['CustomerID'].nunique():,}"
    )

    print("\n" + "=" * 70)
    print("CLEANING PIPELINE COMPLETE")
    print("=" * 70)


if __name__ == "__main__":

    raw_data = load_raw_data()

    cleaned_data = clean_data(raw_data)

    valid_sales = create_valid_sales_dataset(
        cleaned_data
    )

    save_outputs(
        cleaned_data,
        valid_sales
    )

    print_summary(
        raw_data,
        cleaned_data,
        valid_sales
    )