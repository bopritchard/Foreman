# validator.py
import pandas as pd
import re
from datetime import datetime

REQUIRED_FIELDS = ['name', 'customerEmail', 'signupDate']

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", str(email))

def is_valid_date(date_str):
    try:
        datetime.strptime(str(date_str), "%Y-%m-%d")
        return True
    except Exception:
        return False

def validate_row(row):
    errors = []

    for field in REQUIRED_FIELDS:
        if pd.isna(row.get(field)) or str(row[field]).strip() == '':
            errors.append(f"Missing value for '{field}'")

    if not is_valid_email(row.get('customerEmail')):
        errors.append("Invalid email format")

    if not is_valid_date(row.get('signupDate')):
        errors.append("Invalid signup date format (expected YYYY-MM-DD)")

    return errors
