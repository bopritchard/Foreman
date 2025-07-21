#!/usr/bin/env python3
import json
import base64

# Test CSV data
csv_data = """name,email,phone,signupDate
John Doe,john@example.com,555-1234,2025-01-15
Jane Smith,jane@example.com,555-5678,2025-01-16
Bob Johnson,bob@example.com,555-9012,2025-01-17"""

# Encode CSV data
encoded_csv = base64.b64encode(csv_data.encode('utf-8')).decode('utf-8')

# Create test event
test_event = {
    "httpMethod": "POST",
    "queryStringParameters": {"action": "glue-upload"},
    "body": json.dumps({
        "csv_data": encoded_csv,
        "filename": "test-fix.csv"
    })
}

print("Test event:")
print(json.dumps(test_event, indent=2)) 