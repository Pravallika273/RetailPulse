from pathlib import Path
import pandas as pd


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

RAW_FILE = Path("data/raw/Online Retail.xlsx")


# ---------------------------------------------------------
# Load raw data
# ---------------------------------------------------------

def load_data(file_path: Path) -> pd.DataFrame:
    """
    Load the raw Excel file.
    """

    if not file_path.exists():
        raise FileNotFoundError(
            f"Raw data file not found: {file_path}"
        )

    df = pd.read_excel(file_path)

    return df


# ---------------------------------------------------------
# Validation checks
# ---------------------------------------------------------

def validate_data(df: pd.DataFrame) -> None:
    """
    Run basic data-quality checks.
    """

    print("=" * 70)
    print("RETAILPULSE - DATA VALIDATION REPORT")
    print("=" * 70)

    # Basic size
    print("\n1. DATASET SIZE")
    print(f"Rows    : {df.shape[0]:,}")
    print(f"Columns : {df.shape[1]}")

    # Column names
    print("\n2. COLUMN NAMES")
    for column in df.columns:
        print(f"- {column}")

    # Data types
    print("\n3. DATA TYPES")
    print(df.dtypes)

    # Missing values
    print("\n4. MISSING VALUES")
    missing = df.isnull().sum()

    for column, count in missing.items():
        percentage = (count / len(df)) * 100
        print(
            f"{column}: {count:,} "
            f"({percentage:.2f}%)"
        )

    # Duplicate rows
    print("\n5. DUPLICATE ROWS")
    duplicate_count = df.duplicated().sum()
    print(f"Duplicates: {duplicate_count:,}")

    # Negative quantity
    print("\n6. NEGATIVE QUANTITIES")
    negative_quantity = (df["Quantity"] < 0).sum()
    print(f"Negative quantity rows: {negative_quantity:,}")

    # Zero quantity
    print("\n7. ZERO QUANTITIES")
    zero_quantity = (df["Quantity"] == 0).sum()
    print(f"Zero quantity rows: {zero_quantity:,}")

    # Zero prices
    print("\n8. ZERO UNIT PRICES")
    zero_price = (df["UnitPrice"] == 0).sum()
    print(f"Zero unit-price rows: {zero_price:,}")

    # Negative prices
    print("\n9. NEGATIVE UNIT PRICES")
    negative_price = (df["UnitPrice"] < 0).sum()
    print(f"Negative unit-price rows: {negative_price:,}")

    # Cancellation invoices
    print("\n10. CANCELLATION INVOICES")

    invoice_text = df["InvoiceNo"].astype(str).str.upper()

    cancellation_count = invoice_text.str.startswith("C").sum()

    print(
        f"Cancellation rows: "
        f"{cancellation_count:,}"
    )

    # Unique values
    print("\n11. UNIQUE VALUES")

    print(
        f"Unique invoices   : "
        f"{df['InvoiceNo'].nunique():,}"
    )

    print(
        f"Unique products   : "
        f"{df['StockCode'].nunique():,}"
    )

    print(
        f"Unique customers  : "
        f"{df['CustomerID'].nunique():,}"
    )

    print(
        f"Unique countries  : "
        f"{df['Country'].nunique():,}"
    )

    # Date range
    print("\n12. DATE RANGE")

    dates = pd.to_datetime(
        df["InvoiceDate"],
        errors="coerce"
    )

    print(f"Start date: {dates.min()}")
    print(f"End date  : {dates.max()}")

    # Sample
    print("\n13. FIRST FIVE ROWS")
    print(df.head())

    print("\n" + "=" * 70)
    print("VALIDATION COMPLETE")
    print("=" * 70)


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":

    data = load_data(RAW_FILE)

    validate_data(data)