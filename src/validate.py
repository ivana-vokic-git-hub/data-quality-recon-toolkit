import pandas as pd


def check_missing_critical_fields(df: pd.DataFrame, critical_cols: list[str], dataset_name: str):
    missing_mask = df[critical_cols].isna().any(axis=1)
    issues = df[missing_mask].copy()

    if issues.empty:
        print(f"No missing critical fields in {dataset_name}.")
    else:
        print(f"\nMissing critical fields detected in {dataset_name}:")
        print(issues)

    return issues


def check_duplicates(df: pd.DataFrame, key_col: str, dataset_name: str):
    dup_mask = df[key_col].duplicated(keep=False)
    issues = df[dup_mask].copy()

    if issues.empty:
        print(f"No duplicates found in {dataset_name} by {key_col}.")
    else:
        print(f"\nDuplicates detected in {dataset_name} by {key_col}:")
        print(issues)

    return issues


def check_non_positive_amounts(df: pd.DataFrame, amount_col: str, dataset_name: str):
    issues = df[df[amount_col] <= 0].copy()

    if issues.empty:
        print(f"No non-positive amounts in {dataset_name}.")
    else:
        print(f"\nNon-positive amounts detected in {dataset_name}:")
        print(issues)

    return issues