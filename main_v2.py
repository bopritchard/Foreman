# main_v2.py
"""
Scalable Foreman CLI with model-based architecture
"""

import argparse
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

from models.registry import ModelRegistry
from gql_client_v2 import GraphQLClient


def preview_file(path):
    """Preview CSV file contents"""
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
    parser = argparse.ArgumentParser(description="🛠️ Foreman v2 - Scalable Data Onboarding CLI")
    parser.add_argument('--file', help="Path to CSV file")
    parser.add_argument('--model', help="Specific model to use (auto-detect if not specified)")
    parser.add_argument('--dry-run', action='store_true', help="Run validation only")
    parser.add_argument('--submit', action='store_true', help="Submit to GraphQL")
    parser.add_argument('--list-models', action='store_true', help="List available models")
    args = parser.parse_args()

    # Initialize registry and client
    registry = ModelRegistry()
    client = GraphQLClient()

    # List models if requested
    if args.list_models:
        models = registry.list_models()
        print("📋 Available Models:")
        for model_name in models:
            print(f"  - {model_name}")
        return

    # Check if file is required
    if not args.file:
        parser.error("--file is required unless --list-models is specified")

    print(f"📂 Loading file: {args.file}")
    df = preview_file(args.file)
    if df is None:
        return

    # Auto-detect or validate model
    if args.model:
        is_valid, model, message = registry.validate_csv(df, args.model)
    else:
        is_valid, model, message = registry.validate_csv(df)
    
    print(f"\n🔍 Model Detection: {message}")
    
    if not is_valid or not model:
        print("❌ No suitable model found for this CSV structure")
        print("💡 Available models:")
        for model_name in registry.list_models():
            print(f"  - {model_name}")
        print("💡 Use --model <name> to specify a model manually")
        return

    print(f"✅ Using model: {model.name}")

    # Map fields using the detected model
    print("\n🔁 Mapping fields...")
    mapped_df = model.map_fields(df)
    print("🗺️ Columns after mapping:")
    print(mapped_df.columns)

    # Validation and submission
    if args.dry_run:
        print("\n🔎 Validating rows...")
        error_count = 0
        for idx, row in mapped_df.iterrows():
            errors = model.validate_row(row)
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
            errors = model.validate_row(row)
            if errors:
                error_count += 1
                print(f"⛔ Skipping row {idx + 1} due to validation errors:")
                for err in errors:
                    print(f"  - {err}")
                continue
            
            # Submit to GraphQL using the model
            success, result = client.submit_record(model, row)
            if success:
                success_count += 1
                print(f"✅ Row {idx + 1}: {model.name.title()} created with ID {result.get('id', 'N/A')}")
            else:
                error_count += 1
                print(f"❌ Row {idx + 1}: {result}")
        
        print(f"\n📊 Submission Summary:")
        print(f"  ✅ Successful: {success_count}")
        print(f"  ❌ Failed: {error_count}")
        print(f"  📈 Total: {len(mapped_df)}")


if __name__ == "__main__":
    main() 