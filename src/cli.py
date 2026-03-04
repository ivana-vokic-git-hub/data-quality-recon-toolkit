import argparse

def main():
    parser = argparse.ArgumentParser(description="Data Quality & Reconciliation Toolkit")
    parser.add_argument("--version", action="store_true", help="Show version and exit")
    args = parser.parse_args()

    if args.version:
        print("dq-recon-toolkit v0.1.0")
        return

    print("OK: toolkit skeleton is running. Next: ingest, validate, reconcile, report.")

if __name__ == "__main__":
    main()