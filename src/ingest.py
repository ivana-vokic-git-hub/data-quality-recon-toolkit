import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/sample")


def _safe_read_csv(file_path: Path) -> pd.DataFrame:
    if not file_path.exists():
        raise FileNotFoundError(f"Missing file: {file_path}. Did you create it in data/sample?")
    if file_path.stat().st_size == 0:
        raise ValueError(f"File is empty: {file_path}. Open it and paste the sample CSV content, then save.")
    return pd.read_csv(file_path)


def load_bank_transactions():
    file_path = DATA_PATH / "bank_transactions.csv"
    df = _safe_read_csv(file_path)
    df["date"] = pd.to_datetime(df["date"])
    return df


def load_ledger_entries():
    file_path = DATA_PATH / "ledger_entries.csv"
    df = _safe_read_csv(file_path)
    df["posting_date"] = pd.to_datetime(df["posting_date"], dayfirst=True)
    return df


def dataset_summary(df, name):
    print(f"\nDataset: {name}")
    print("-" * 40)
    print("Rows:", len(df))
    print("Columns:", list(df.columns))
    print("\nPreview:")
    print(df.head())