# gql_client.py

import requests
import os
import json

GRAPHQL_URL = os.getenv("GRAPHQL_URL", "https://example.com/graphql")
APPSYNC_API_KEY = os.getenv("APPSYNC_API_KEY", "")

def submit_customer(row):
    """
    Submit a customer to the AppSync GraphQL API
    """
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
            "email": row.get("customerEmail"),
            "signupDate": row.get("signupDate")
        }
    }

    headers = {
        "Content-Type": "application/json",
    }
    
    # Add API key if available (for AppSync)
    if APPSYNC_API_KEY:
        headers["x-api-key"] = APPSYNC_API_KEY

    try:
        response = requests.post(
            GRAPHQL_URL,
            json={'query': mutation, 'variables': variables},
            headers=headers
        )
        
        if response.status_code != 200:
            return False, f"HTTP {response.status_code}: {response.text}"
        
        data = response.json()
        
        if "errors" in data:
            return False, data["errors"]
        
        if "data" in data and data["data"]:
            return True, data["data"]["createCustomer"]
        else:
            return False, "No data returned from mutation"
            
    except Exception as e:
        return False, str(e)

def get_customer(customer_id):
    """
    Get a customer by ID from the AppSync GraphQL API
    """
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

    variables = {
        "id": customer_id
    }

    headers = {
        "Content-Type": "application/json",
    }
    
    # Add API key if available (for AppSync)
    if APPSYNC_API_KEY:
        headers["x-api-key"] = APPSYNC_API_KEY

    try:
        response = requests.post(
            GRAPHQL_URL,
            json={'query': query, 'variables': variables},
            headers=headers
        )
        
        if response.status_code != 200:
            return False, f"HTTP {response.status_code}: {response.text}"
        
        data = response.json()
        
        if "errors" in data:
            return False, data["errors"]
        
        if "data" in data and data["data"]:
            return True, data["data"]["getCustomer"]
        else:
            return False, "Customer not found"
            
    except Exception as e:
        return False, str(e)
