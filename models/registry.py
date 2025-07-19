# models/registry.py
"""
Model registry for managing different data types
"""

from typing import List, Optional, Type, Tuple
import pandas as pd
from .base import BaseModel
from .customer import CustomerModel
from .project import ProjectModel


class ModelRegistry:
    """Registry for all available data models"""
    
    def __init__(self):
        self.models: List[BaseModel] = [
            CustomerModel(),
            ProjectModel(),
            # Add more models here as they're created
            # JobModel(),
        ]
    
    def detect_model(self, df: pd.DataFrame) -> Optional[BaseModel]:
        """Auto-detect the appropriate model for a CSV"""
        for model in self.models:
            if model.detect_from_csv(df):
                return model
        return None
    
    def get_model_by_name(self, name: str) -> Optional[BaseModel]:
        """Get a model by name"""
        for model in self.models:
            if model.name == name:
                return model
        return None
    
    def list_models(self) -> List[str]:
        """List all available model names"""
        return [model.name for model in self.models]
    
    def validate_csv(self, df: pd.DataFrame, model_name: Optional[str] = None) -> Tuple[bool, Optional[BaseModel], str]:
        """Validate that a CSV can be processed by a model"""
        if model_name:
            model = self.get_model_by_name(model_name)
            if not model:
                return False, None, f"Model '{model_name}' not found"
            if not model.detect_from_csv(df):
                return False, None, f"CSV structure doesn't match model '{model_name}'"
            return True, model, f"CSV matches model '{model_name}'"
        else:
            model = self.detect_model(df)
            if model:
                return True, model, f"Auto-detected model: {model.name}"
            else:
                return False, None, "No matching model found for CSV structure" 