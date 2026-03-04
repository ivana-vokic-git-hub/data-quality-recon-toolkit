import argparse
from ingest import load_bank_transactions, load_ledger_entries, dataset_summary


def main():
    parser = argparse.ArgumentParser(description="Data Quality & Reconciliation Toolkit")
    parser.add_argument("--version", action="store_true", help="Show version and exit")
    parser.add_argument("--ingest", action="store_true", help="Load datasets and show summary")
    parser.add_argument("--helpme", action="store_true", help="Try --ingest to load data")
                        

    args = parser.parse_args()

    if args.version:
        print("dq-recon-toolkit v0.1.0")
        return

    if args.ingest:
        bank = load_bank_transactions()
        ledger = load_ledger_entries()

        dataset_summary(bank, "Bank Transactions")
        dataset_summary(ledger, "Ledger Entries")

        return
    
    if args.helpme:
        print("It looks like you might need some help. Try running with --ingest to load the sample datasets and see their summaries.")
        return

    print("Run with --ingest to load sample datasets.")


if __name__ == "__main__":
    main()