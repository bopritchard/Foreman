#!/bin/bash

# Foreman S3 Pipeline Deployment Script
set -e

# Configuration
STACK_NAME="foreman-s3-pipeline-dev"
TEMPLATE_FILE="cloudformation/foreman-s3-pipeline.yaml"
REGION="us-east-1"

echo "🚀 Deploying Foreman S3 Pipeline to AWS..."

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
S3_BUCKET=$(aws cloudformation describe-stacks \
    --stack-name "$STACK_NAME" \
    --region "$REGION" \
    --query 'Stacks[0].Outputs[?OutputKey==`S3BucketName`].OutputValue' \
    --output text)

S3_CONSOLE_URL=$(aws cloudformation describe-stacks \
    --stack-name "$STACK_NAME" \
    --region "$REGION" \
    --query 'Stacks[0].Outputs[?OutputKey==`S3BucketUrl`].OutputValue' \
    --output text)

DASHBOARD_URL=$(aws cloudformation describe-stacks \
    --stack-name "$STACK_NAME" \
    --region "$REGION" \
    --query 'Stacks[0].Outputs[?OutputKey==`CloudWatchDashboardUrl`].OutputValue' \
    --output text)

echo "✅ S3 Pipeline deployment completed successfully!"
echo ""
echo "📊 Pipeline Details:"
echo "  S3 Bucket: $S3_BUCKET"
echo "  S3 Console: $S3_CONSOLE_URL"
echo "  CloudWatch Dashboard: $DASHBOARD_URL"
echo ""
echo "📤 Upload Methods:"
echo ""
echo "1. AWS CLI Upload:"
echo "   aws s3 cp sample.csv s3://$S3_BUCKET/"
echo ""
echo "2. AWS Console Upload:"
echo "   $S3_CONSOLE_URL"
echo ""
echo "3. Programmatic Upload (Python):"
echo "   import boto3"
echo "   s3 = boto3.client('s3')"
echo "   s3.upload_file('sample.csv', '$S3_BUCKET', 'sample.csv')"
echo ""
echo "📈 Monitor Processing:"
echo "   $DASHBOARD_URL"
echo ""
echo "🧪 Test the pipeline:"
echo "   aws s3 cp sample.csv s3://$S3_BUCKET/"
echo "   # Check CloudWatch logs for processing results" 