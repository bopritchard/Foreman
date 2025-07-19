# models/project.py
"""
Project data model for Foreman
"""

from typing import Dict, Any, List, Tuple
import pandas as pd
from .base import BaseModel


class ProjectModel(BaseModel):
    """Project data model"""
    
    def __init__(self):
        schema = {
            'name': {'required': True, 'type': 'string'},
            'description': {'required': False, 'type': 'string'},
            'startDate': {'required': False, 'type': 'date'},
            'endDate': {'required': False, 'type': 'date'},
            'status': {'required': False, 'type': 'string'},
            'budget': {'required': False, 'type': 'number'},
            'customerId': {'required': False, 'type': 'string'}
        }
        super().__init__('project', schema)
    
    def validate_row(self, row: pd.Series) -> List[str]:
        """Validate project data"""
        errors = self.get_validation_errors(row)
        
        # Budget validation
        budget = row.get('budget', '')
        if budget and not str(budget).replace('.', '').replace(',', '').isdigit():
            errors.append("Invalid budget format")
        
        # Date validation (basic)
        start_date = row.get('startDate', '')
        end_date = row.get('endDate', '')
        if start_date and end_date and start_date > end_date:
            errors.append("Start date cannot be after end date")
        
        return errors
    
    def map_fields(self, df: pd.DataFrame) -> pd.DataFrame:
        """Map CSV columns to project schema"""
        # Create a copy to avoid modifying original
        mapped_df = df.copy()
        
        # Standard field mappings
        field_mappings = {
            'project_name': 'name',
            'project_description': 'description',
            'start_date': 'startDate',
            'end_date': 'endDate',
            'project_status': 'status',
            'project_budget': 'budget',
            'customer_id': 'customerId'
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
        """Create GraphQL mutation for project"""
        mutation = """
        mutation CreateProject($input: ProjectInput!) {
          createProject(input: $input) {
            id
            name
            description
            startDate
            endDate
            status
            budget
          }
        }
        """
        
        variables = {
            "input": {
                "name": row.get("name"),
                "description": row.get("description"),
                "startDate": row.get("startDate"),
                "endDate": row.get("endDate"),
                "status": row.get("status"),
                "budget": row.get("budget")
            }
        }
        
        return mutation, variables
    
    def detect_from_csv(self, df: pd.DataFrame) -> bool:
        """Detect if this model matches the CSV structure"""
        # Check for project-specific field patterns
        csv_columns = set(df.columns.str.lower())
        
        # Look for common project field patterns
        project_patterns = [
            'project_name', 'name', 'title',
            'project_description', 'description', 'desc',
            'start_date', 'end_date', 'deadline',
            'project_status', 'status', 'state',
            'project_budget', 'budget', 'cost'
        ]
        
        # If we find at least 2 project-related fields, it's likely a project CSV
        found_patterns = sum(1 for pattern in project_patterns if pattern in csv_columns)
        return found_patterns >= 2
    
    def get_query(self, id: str) -> Tuple[str, Dict[str, Any]]:
        """Create GraphQL query for project"""
        query = """
        query GetProject($id: ID!) {
          getProject(id: $id) {
            id
            name
            description
            startDate
            endDate
            status
            budget
            createdAt
            updatedAt
          }
        }
        """
        
        variables = {"id": id}
        return query, variables 