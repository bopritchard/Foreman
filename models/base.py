# models/base.py
"""
Base model class for all data types in Foreman
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Tuple, Optional
import pandas as pd


class BaseModel(ABC):
    """Base class for all data models"""
    
    def __init__(self, name: str, schema: Dict[str, str]):
        self.name = name
        self.schema = schema
        self.required_fields = [field for field, config in schema.items() 
                              if config.get('required', False)]
    
    @abstractmethod
    def validate_row(self, row: pd.Series) -> List[str]:
        """Validate a single row of data"""
        pass
    
    @abstractmethod
    def map_fields(self, df: pd.DataFrame) -> pd.DataFrame:
        """Map CSV columns to internal schema"""
        pass
    
    @abstractmethod
    def create_mutation(self, row: pd.Series) -> Tuple[str, Dict[str, Any]]:
        """Create GraphQL mutation for this data type"""
        pass
    
    @abstractmethod
    def get_query(self, id: str) -> Tuple[str, Dict[str, Any]]:
        """Create GraphQL query for this data type"""
        pass
    
    def detect_from_csv(self, df: pd.DataFrame) -> bool:
        """Detect if this model matches the CSV structure"""
        # Default implementation - check if required fields are present
        csv_columns = set(df.columns.str.lower())
        required_lower = {field.lower() for field in self.required_fields}
        return required_lower.issubset(csv_columns)
    
    def get_validation_errors(self, row: pd.Series) -> List[str]:
        """Get validation errors for a row"""
        errors = []
        
        # Check required fields
        for field in self.required_fields:
            if pd.isna(row.get(field)) or str(row.get(field)).strip() == '':
                errors.append(f"Required field '{field}' is missing or empty")
        
        return errors 