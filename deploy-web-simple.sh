#!/bin/bash

# Foreman Simple Web Interface Deployment Script
set -e

# Configuration
STACK_NAME="foreman-web-simple-dev"
TEMPLATE_FILE="cloudformation/foreman-web-simple.yaml"
REGION="us-east-1"

echo "🌐 Deploying Foreman Simple Web Interface to AWS..."

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI is not installed. Please install it first."
    exit 1
fi

# Check if template file exists
if [ ! -f "$TEMPLATE_FILE" ]; then
    echo "❌ Template file not found: $TEMPLATE_FILE"
    exit 1
fi

# Deploy CloudFormation stack
echo "📦 Deploying CloudFormation stack: $STACK_NAME"
aws cloudformation deploy \
    --template-file "$TEMPLATE_FILE" \
    --stack-name "$STACK_NAME" \
    --region "$REGION" \
    --capabilities CAPABILITY_NAMED_IAM \
    --parameter-overrides Environment=dev ProjectName=foreman

# Wait for stack to complete
echo "⏳ Waiting for stack deployment to complete..."
aws cloudformation wait stack-create-complete \
    --stack-name "$STACK_NAME" \
    --region "$REGION" || aws cloudformation wait stack-update-complete \
    --stack-name "$STACK_NAME" \
    --region "$REGION"

# Get stack outputs
echo "📋 Getting stack outputs..."
WEB_API_URL=$(aws cloudformation describe-stacks \
    --stack-name "$STACK_NAME" \
    --region "$REGION" \
    --query 'Stacks[0].Outputs[?OutputKey==`WebApiUrl`].OutputValue' \
    --output text)

echo "✅ Simple Web Interface deployment completed successfully!"
echo ""
echo "🌐 Web Interface URL:"
echo "  $WEB_API_URL"
echo ""
echo "🧪 Test the web interface:"
echo "   curl $WEB_API_URL"
echo ""
echo "📊 Monitor:"
echo "   - CloudWatch Logs for Lambda execution"
echo "   - API Gateway Console for request metrics" 