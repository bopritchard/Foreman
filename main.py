import argparse
import pandas as pd
import os
from mapper import map_fields
from validator import validate_row
from dotenv import load_dotenv
load_dotenv()
from gql_client import submit_customer


def preview_file(path):
    if not os.path.exists(path):
        print(f"❌ File not found: {path}")
        return None

    try:
        df = pd.read_csv(path)
        print("✅ CSV Loaded.\n")
        print("📊 Preview (first 5 rows):")
        print(df.head(), "\n")
        print("🧠 Inferred Columns:")
        for col in df.columns:
            print(f"- {col}")
        return df
    except Exception as e:
        print(f"❌ Failed to load CSV: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="🛠️ Foreman - Data Onboarding CLI")
    parser.add_argument('--file', required=True, help="Path to CSV file")
    parser.add_argument('--dry-run', action='store_true', help="Run validation only")
    parser.add_argument('--submit', action='store_true', help="Submit to GraphQL")
    args = parser.parse_args()

    print(f"📂 Loading file: {args.file}")
    df = preview_file(args.file)
    if df is None:
        return

    # Step 2: Field Mapping (placeholder)
    print("\n🔁 Mapping fields...")
    mapped_df = map_fields(df)
    print("🗺️ Columns after mapping:")
    print(mapped_df.columns)

    # Step 3+4 will come later
    if args.dry_run:
        print("\n🔎 Validating rows...")
        error_count = 0
        for idx, row in mapped_df.iterrows():
            errors = validate_row(row)
            if errors:
                error_count += 1
                print(f"\n❌ Row {idx + 1} errors:")
                for err in errors:
                    print(f"  - {err}")

        if error_count == 0:
            print("✅ All rows passed validation.")
        else:
            print(f"\n⚠️ Validation completed with {error_count} row(s) containing errors.")

    elif args.submit:
        print("\n🚀 Submit mode: Submitting to GraphQL...")
        success_count = 0
        error_count = 0
        
        for idx, row in mapped_df.iterrows():
            # Validate first
            errors = validate_row(row)
            if errors:
                error_count += 1
                print(f"⛔ Skipping row {idx + 1} due to validation errors:")
                for err in errors:
                    print(f"  - {err}")
                continue
            
            # Submit to GraphQL
            success, result = submit_customer(row)
            if success:
                success_count += 1
                print(f"✅ Row {idx + 1}: Customer created with ID {result.get('id', 'N/A')}")
            else:
                error_count += 1
                print(f"❌ Row {idx + 1}: {result}")
        
        print(f"\n📊 Submission Summary:")
        print(f"  ✅ Successful: {success_count}")
        print(f"  ❌ Failed: {error_count}")
        print(f"  📈 Total: {len(mapped_df)}")


if __name__ == "__main__":
    main()
