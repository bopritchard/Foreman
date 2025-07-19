# models/customer.py
"""
Customer data model for Foreman
"""

from typing import Dict, Any, List, Tuple
import pandas as pd
from .base import BaseModel


class CustomerModel(BaseModel):
    """Customer data model"""
    
    def __init__(self):
        schema = {
            'name': {'required': True, 'type': 'string'},
            'email': {'required': True, 'type': 'email'},
            'signupDate': {'required': False, 'type': 'date'},
            'companyName': {'required': False, 'type': 'string'},
            'phone': {'required': False, 'type': 'phone'}
        }
        super().__init__('customer', schema)
    
    def validate_row(self, row: pd.Series) -> List[str]:
        """Validate customer data"""
        errors = self.get_validation_errors(row)
        
        # Email validation
        email = row.get('email', '')
        if email and '@' not in str(email):
            errors.append("Invalid email format")
        
        # Phone validation (basic)
        phone = row.get('phone', '')
        if phone and len(str(phone).replace('-', '').replace('(', '').replace(')', '')) < 10:
            errors.append("Invalid phone number format")
        
        return errors
    
    def map_fields(self, df: pd.DataFrame) -> pd.DataFrame:
        """Map CSV columns to customer schema"""
        # Create a copy to avoid modifying original
        mapped_df = df.copy()
        
        # Standard field mappings
        field_mappings = {
            'full_name': 'name',
            'customerEmail': 'email',
            'joined_on': 'signupDate',
            'companyName': 'companyName',
            'phone': 'phone'
        }
        
        # Apply mappings
        for csv_col, schema_field in field_mappings.items():
            if csv_col in mapped_df.columns:
                mapped_df[schema_field] = mapped_df[csv_col]
        
        # Ensure all required fields exist
        for field in self.required_fields:
            if field not in mapped_df.columns:
                mapped_df[field] = None
        
        return mapped_df
    
    def create_mutation(self, row: pd.Series) -> Tuple[str, Dict[str, Any]]:
        """Create GraphQL mutation for customer"""
        mutation = """
        mutation CreateCustomer($input: CustomerInput!) {
          createCustomer(input: $input) {
            id
            name
            email
            signupDate
          }
        }
        """
        
        variables = {
            "input": {
                "name": row.get("name"),
                "email": row.get("email"),
                "signupDate": row.get("signupDate")
            }
        }
        
        return mutation, variables
    
    def detect_from_csv(self, df: pd.DataFrame) -> bool:
        """Detect if this model matches the CSV structure"""
        # Check for customer-specific field patterns
        csv_columns = set(df.columns.str.lower())
        
        # Look for common customer field patterns
        customer_patterns = [
            'full_name', 'name', 'customer_name',
            'email', 'customer_email', 'email_address',
            'phone', 'phone_number', 'telephone'
        ]
        
        # If we find at least 2 customer-related fields, it's likely a customer CSV
        found_patterns = sum(1 for pattern in customer_patterns if pattern in csv_columns)
        return found_patterns >= 2
    
    def get_query(self, id: str) -> Tuple[str, Dict[str, Any]]:
        """Create GraphQL query for customer"""
        query = """
        query GetCustomer($id: ID!) {
          getCustomer(id: $id) {
            id
            name
            email
            signupDate
            createdAt
            updatedAt
          }
        }
        """
        
        variables = {"id": id}
        return query, variables 