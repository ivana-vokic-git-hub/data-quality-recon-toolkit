import pandas as pd
from pathlib import Path

OUTPUT_DIR = Path("outputs/reports")


def reconcile_transactions(bank_df: pd.DataFrame, ledger_df: pd.DataFrame) -> pd.DataFrame:
    merged = pd.merge(
        bank_df,
        ledger_df,
        left_on=["date", "amount", "account"],
        right_on=["posting_date", "amount", "account"],
        how="outer",
        indicator=True,
        suffixes=("_bank", "_ledger"),
    )
    return merged


def export_reconciliation_reports(merged: pd.DataFrame):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    matched = merged[merged["_merge"] == "both"].copy()
    missing_in_ledger = merged[merged["_merge"] == "left_only"].copy()
    extra_in_ledger = merged[merged["_merge"] == "right_only"].copy()

    matched.to_csv(OUTPUT_DIR / "recon_matched.csv", index=False)
    missing_in_ledger.to_csv(OUTPUT_DIR / "recon_missing_in_ledger.csv", index=False)
    extra_in_ledger.to_csv(OUTPUT_DIR / "recon_extra_in_ledger.csv", index=False)

    print(f"Saved: {OUTPUT_DIR / 'recon_matched.csv'}")
    print(f"Saved: {OUTPUT_DIR / 'recon_missing_in_ledger.csv'}")
    print(f"Saved: {OUTPUT_DIR / 'recon_extra_in_ledger.csv'}")

    return matched, missing_in_ledger, extra_in_ledger