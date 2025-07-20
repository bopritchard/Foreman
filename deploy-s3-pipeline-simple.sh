#!/bin/bash

# Foreman S3 Pipeline Simple Deployment Script
set -e

STACK_NAME="foreman-s3-pipeline-simple-dev"
TEMPLATE_FILE="cloudformation/foreman-s3-pipeline-simple.yaml"
REGION="us-east-1"

echo "🚀 Deploying Foreman Simple S3 Pipeline to AWS..."
echo "📦 Deploying CloudFormation stack: $STACK_NAME"

# Deploy the stack
aws cloudformation deploy \
    --template-file "$TEMPLATE_FILE" \
    --stack-name "$STACK_NAME" \
    --region "$REGION" \
    --capabilities CAPABILITY_NAMED_IAM \
    --parameter-overrides \
        Environment=dev \
        ProjectName=foreman

echo "⏳ Waiting for stack deployment to complete..."
aws cloudformation wait stack-create-complete --stack-name "$STACK_NAME" --region "$REGION"

echo "📋 Getting stack outputs..."
aws cloudformation describe-stacks \
    --stack-name "$STACK_NAME" \
    --region "$REGION" \
    --query 'Stacks[0].Outputs'

echo "✅ Simple S3 Pipeline deployment completed successfully!"

echo ""
echo "🔧 Next steps:"
echo "1. Configure S3 bucket notifications manually:"
echo "   aws s3api put-bucket-notification-configuration --bucket foreman-dev-csv-uploads --notification-configuration '{\"LambdaFunctionConfigurations\":[{\"Id\":\"CSVProcessor\",\"LambdaFunctionArn\":\"arn:aws:lambda:us-east-1:631138567000:function:foreman-dev-s3-processor\",\"Events\":[\"s3:ObjectCreated:*\"],\"Filter\":{\"Key\":{\"FilterRules\":[{\"Name\":\"suffix\",\"Value\":\".csv\"}]}}}]}'"
echo ""
echo "2. Test with a CSV file:"
echo "   aws s3 cp sample.csv s3://foreman-dev-csv-uploads/"
echo ""
echo "3. Check CloudWatch logs:"
echo "   aws logs tail /aws/lambda/foreman-dev-s3-processor --follow" 