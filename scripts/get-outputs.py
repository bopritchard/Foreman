#!/usr/bin/env python3

import boto3
import json
import os

def get_stack_outputs():
    """Get outputs from the CloudFormation stack"""
    cloudformation = boto3.client('cloudformation', region_name='us-east-1')
    
    try:
        response = cloudformation.describe_stacks(StackName='foreman-dev')
        stack = response['Stacks'][0]
        
        outputs = {}
        for output in stack.get('Outputs', []):
            outputs[output['OutputKey']] = output['OutputValue']
        
        return outputs
    except Exception as e:
        print(f"Error getting stack outputs: {e}")
        return None

def update_env_file(outputs):
    """Update .env file with stack outputs"""
    if not outputs:
        print("No outputs to update")
        return
    
    # Read current .env file
    env_content = ""
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            env_content = f.read()
    
    # Update with new values
    if 'AppSyncApiUrl' in outputs:
        env_content = env_content.replace(
            'GRAPHQL_URL=https://example.com/graphql',
            f'GRAPHQL_URL={outputs["AppSyncApiUrl"]}'
        )
        env_content = env_content.replace(
            'APPSYNC_API_URL=',
            f'APPSYNC_API_URL={outputs["AppSyncApiUrl"]}'
        )
    
    if 'AppSyncApiKey' in outputs:
        env_content = env_content.replace(
            'APPSYNC_API_KEY=',
            f'APPSYNC_API_KEY={outputs["AppSyncApiKey"]}'
        )
    
    # Write updated .env file
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Updated .env file with stack outputs")
    print(f"AppSync URL: {outputs.get('AppSyncApiUrl', 'Not found')}")
    print(f"AppSync API Key: {outputs.get('AppSyncApiKey', 'Not found')}")

if __name__ == "__main__":
    print("🔍 Getting CloudFormation stack outputs...")
    outputs = get_stack_outputs()
    if outputs:
        update_env_file(outputs)
    else:
        print("❌ Failed to get stack outputs") 