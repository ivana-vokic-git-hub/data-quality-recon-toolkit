import argparse
from ingest import load_bank_transactions, load_ledger_entries, dataset_summary
from validate import (
    check_missing_critical_fields,
    check_duplicates,
    check_non_positive_amounts,
)
from reconcile import reconcile_transactions, export_reconciliation_reports


def main():
    parser = argparse.ArgumentParser(description="Data Quality & Reconciliation Toolkit")
    parser.add_argument("--version", action="store_true", help="Show version and exit")
    parser.add_argument("--ingest", action="store_true", help="Load datasets and show summary")
    parser.add_argument("--validate", action="store_true", help="Run data quality checks")
    parser.add_argument("--reconcile", action="store_true", help="Run reconciliation")
    parser.add_argument("--helpme", action="store_true", help="Show beginner help")

    args = parser.parse_args()

    if args.version:
        print("dq-recon-toolkit v0.1.0")
        return

    if args.helpme:
        print("Try --ingest to load the datasets, --validate for data quality checks, or --reconcile to compare bank vs ledger.")
        return

    # Load data once if any action needs it
    if args.ingest or args.validate or args.reconcile:
        bank = load_bank_transactions()
        ledger = load_ledger_entries()
    else:
        print("No action selected. Use --ingest, --validate, or --reconcile. Run with --help to see options.")
        return

    if args.ingest:
        dataset_summary(bank, "Bank Transactions")
        dataset_summary(ledger, "Ledger Entries")
        return

    if args.validate:
        check_missing_critical_fields(
            bank,
            critical_cols=["transaction_id", "date", "amount", "account"],
            dataset_name="Bank Transactions",
        )
        check_duplicates(bank, key_col="transaction_id", dataset_name="Bank Transactions")
        check_non_positive_amounts(bank, amount_col="amount", dataset_name="Bank Transactions")

        check_missing_critical_fields(
            ledger,
            critical_cols=["ledger_id", "posting_date", "amount", "account"],
            dataset_name="Ledger Entries",
        )
        check_duplicates(ledger, key_col="ledger_id", dataset_name="Ledger Entries")
        check_non_positive_amounts(ledger, amount_col="amount", dataset_name="Ledger Entries")
        return

    if args.reconcile:
        recon = reconcile_transactions(bank, ledger)

        print("\nReconciliation results:")
        print(recon["_merge"].value_counts())

        export_reconciliation_reports(recon)
    return
    

    print("Run with --ingest to load sample datasets.")


if __name__ == "__main__":
    main()