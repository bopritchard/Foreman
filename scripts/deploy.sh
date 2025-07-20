#!/bin/bash

# Foreman AWS Infrastructure Deployment Script
set -e

# Configuration
STACK_NAME="foreman-dev"
TEMPLATE_FILE="cloudformation/foreman-core.yaml"
REGION="us-east-1"

echo "🚀 Deploying Foreman infrastructure to AWS..."

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
APPSYNC_URL=$(aws cloudformation describe-stacks \
    --stack-name "$STACK_NAME" \
    --region "$REGION" \
    --query 'Stacks[0].Outputs[?OutputKey==`AppSyncApiUrl`].OutputValue' \
    --output text)

APPSYNC_KEY=$(aws cloudformation describe-stacks \
    --stack-name "$STACK_NAME" \
    --region "$REGION" \
    --query 'Stacks[0].Outputs[?OutputKey==`AppSyncApiKey`].OutputValue' \
    --output text)

DYNAMODB_TABLE=$(aws cloudformation describe-stacks \
    --stack-name "$STACK_NAME" \
    --region "$REGION" \
    --query 'Stacks[0].Outputs[?OutputKey==`DynamoDBTableName`].OutputValue' \
    --output text)

# Update .env file with new values
echo "🔧 Updating .env file with AppSync configuration..."
sed -i.bak "s|APPSYNC_API_URL=.*|APPSYNC_API_URL=$APPSYNC_URL|" .env
sed -i.bak "s|APPSYNC_API_KEY=.*|APPSYNC_API_KEY=$APPSYNC_KEY|" .env
sed -i.bak "s|GRAPHQL_URL=.*|GRAPHQL_URL=$APPSYNC_URL|" .env

# Clean up backup file
rm -f .env.bak

echo "✅ Deployment completed successfully!"
echo ""
echo "📊 Infrastructure Details:"
echo "  AppSync URL: $APPSYNC_URL"
echo "  AppSync API Key: $APPSYNC_KEY"
echo "  DynamoDB Table: $DYNAMODB_TABLE"
echo ""
echo "🔗 AWS Console: https://us-east-1.console.aws.amazon.com/"
echo "📦 CloudFormation Stack: https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/stackinfo?stackId=$STACK_NAME"
echo ""
echo "🧪 Test the deployment:"
echo "  python main.py --file sample.csv --dry-run"
echo "  python main.py --file sample.csv --submit" 