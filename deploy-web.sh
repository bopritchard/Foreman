#!/bin/bash

# Foreman Web Interface Deployment Script
set -e

# Configuration
STACK_NAME="foreman-web-dev"
TEMPLATE_FILE="cloudformation/foreman-web.yaml"
REGION="us-east-1"

echo "🌐 Deploying Foreman Web Interface to AWS..."

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

CLOUDFRONT_URL=$(aws cloudformation describe-stacks \
    --stack-name "$STACK_NAME" \
    --region "$REGION" \
    --query 'Stacks[0].Outputs[?OutputKey==`CloudFrontUrl`].OutputValue' \
    --output text)

S3_WEBSITE_URL=$(aws cloudformation describe-stacks \
    --stack-name "$STACK_NAME" \
    --region "$REGION" \
    --query 'Stacks[0].Outputs[?OutputKey==`S3WebsiteUrl`].OutputValue' \
    --output text)

echo "✅ Web Interface deployment completed successfully!"
echo ""
echo "🌐 Web Interface URLs:"
echo "  API Gateway: $WEB_API_URL"
echo "  CloudFront: $CLOUDFRONT_URL"
echo "  S3 Website: $S3_WEBSITE_URL"
echo ""
echo "📤 Upload Methods:"
echo ""
echo "1. Web Interface (Recommended):"
echo "   $WEB_API_URL"
echo ""
echo "2. CloudFront (CDN):"
echo "   $CLOUDFRONT_URL"
echo ""
echo "3. Direct S3:"
echo "   $S3_WEBSITE_URL"
echo ""
echo "🧪 Test the web interface:"
echo "   curl $WEB_API_URL"
echo ""
echo "📊 Monitor:"
echo "   - CloudWatch Logs for Lambda execution"
echo "   - API Gateway Console for request metrics"
echo "   - CloudFront Console for CDN performance" 