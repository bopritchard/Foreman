"""
Scalable GraphQL client for Foreman
"""

import requests
import os
from typing import Dict, Any, Tuple, Optional
from models.base import BaseModel


class GraphQLClient:
    """Generic GraphQL client for AppSync"""
    
    def __init__(self):
        self.graphql_url = os.getenv("GRAPHQL_URL")
        self.api_key = os.getenv("APPSYNC_API_KEY")
        
        if not self.graphql_url:
            raise ValueError("GRAPHQL_URL environment variable is required. Please set it in your .env file.")
        
        if not self.api_key:
            raise ValueError("APPSYNC_API_KEY environment variable is required. Please set it in your .env file.")
    
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers"""
        headers = {
            "Content-Type": "application/json",
        }
        
        if self.api_key:
            headers["x-api-key"] = self.api_key
        
        return headers
    
    def submit_record(self, model: BaseModel, row) -> Tuple[bool, Any]:
        """Submit a record using the provided model"""
        try:
            mutation, variables = model.create_mutation(row)
            
            response = requests.post(
                self.graphql_url,
                json={'query': mutation, 'variables': variables},
                headers=self._get_headers()
            )
            
            if response.status_code != 200:
                return False, f"HTTP {response.status_code}: {response.text}"
            
            data = response.json()
            
            if "errors" in data:
                return False, data["errors"]
            
            if "data" in data and data["data"]:
                # Extract the result from the first key in data
                result_key = list(data["data"].keys())[0]
                return True, data["data"][result_key]
            else:
                return False, "No data returned from mutation"
                
        except Exception as e:
            return False, str(e)
    
    def get_record(self, model: BaseModel, record_id: str) -> Tuple[bool, Any]:
        """Get a record using the provided model"""
        try:
            query, variables = model.get_query(record_id)
            
            response = requests.post(
                self.graphql_url,
                json={'query': query, 'variables': variables},
                headers=self._get_headers()
            )
            
            if response.status_code != 200:
                return False, f"HTTP {response.status_code}: {response.text}"
            
            data = response.json()
            
            if "errors" in data:
                return False, data["errors"]
            
            if "data" in data and data["data"]:
                # Extract the result from the first key in data
                result_key = list(data["data"].keys())[0]
                return True, data["data"][result_key]
            else:
                return False, "Record not found"
                
        except Exception as e:
            return False, str(e)
    
    def test_connection(self) -> Tuple[bool, str]:
        """Test the GraphQL connection"""
        try:
            response = requests.post(
                self.graphql_url,
                json={'query': '{ __schema { types { name } } }'},
                headers=self._get_headers()
            )
            
            if response.status_code == 200:
                return True, "Connection successful"
            else:
                return False, f"Connection failed: HTTP {response.status_code}"
                
        except Exception as e:
            return False, f"Connection error: {str(e)}" 