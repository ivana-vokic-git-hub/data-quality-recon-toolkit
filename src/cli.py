import argparse
from ingest import load_bank_transactions, load_ledger_entries, dataset_summary
from validate import (
    check_missing_critical_fields,
    check_duplicates,
    check_non_positive_amounts,
)


def main():
    parser = argparse.ArgumentParser(description="Data Quality & Reconciliation Toolkit")
    parser.add_argument("--version", action="store_true", help="Show version and exit")
    parser.add_argument("--ingest", action="store_true", help="Load datasets and show summary")
    parser.add_argument("--helpme", action="store_true", help="Try --ingest to load data")
    parser.add_argument("--validate", action="store_true", help="Run data quality checks")  
                        

    args = parser.parse_args()

    if args.version:
        print("dq-recon-toolkit v0.1.0")
        return

    if args.ingest:
        bank = load_bank_transactions()
        ledger = load_ledger_entries()

        dataset_summary(bank, "Bank Transactions")
        dataset_summary(ledger, "Ledger Entries")
        check_duplicate_transactions(bank)

        return
    
    if args.helpme:
        print("It looks like you might need some help. Try running with --ingest to load the sample datasets and see their summaries.")
        return
    
    if args.ingest or args.validate:
        bank = load_bank_transactions()
        ledger = load_ledger_entries()

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

    print("Run with --ingest to load sample datasets.")


if __name__ == "__main__":
    main()