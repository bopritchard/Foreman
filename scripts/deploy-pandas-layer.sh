#!/bin/bash

# Deploy Pandas Lambda Layer
# This script uploads the pandas layer to S3 and deploys the CloudFormation stack

set -e

# Configuration
STACK_NAME="foreman-dev-pandas-layer"
TEMPLATE_FILE="cloudformation/foreman-s3-pipeline-simple.yaml"
REGION="us-east-1"
ENVIRONMENT="dev"
PROJECT_NAME="foreman"

echo "🚀 Deploying Pandas Lambda Layer..."

# Check if pandas layer exists
if [ ! -f "layers/pandas-layer/pandas-layer.zip" ]; then
    echo "❌ Pandas layer not found. Please run:"
    echo "   mkdir -p layers/pandas-layer/python"
    echo "   pip install pandas numpy -t layers/pandas-layer/python"
    echo "   cd layers/pandas-layer && zip -r pandas-layer.zip python/"
    exit 1
fi

# Get the S3 bucket name from the stack (if it exists)
BUCKET_NAME=""
if aws cloudformation describe-stacks --stack-name $STACK_NAME --region $REGION >/dev/null 2>&1; then
    BUCKET_NAME=$(aws cloudformation describe-stacks \
        --stack-name $STACK_NAME \
        --region $REGION \
        --query 'Stacks[0].Outputs[?OutputKey==`PandasLayerBucketName`].OutputValue' \
        --output text 2>/dev/null || echo "")
fi

# If bucket doesn't exist, create a temporary one
if [ -z "$BUCKET_NAME" ]; then
    echo "📦 Creating temporary S3 bucket for pandas layer..."
    BUCKET_NAME="foreman-dev-pandas-layer-$(date +%s)"
    aws s3 mb s3://$BUCKET_NAME --region $REGION
    aws s3api put-bucket-versioning --bucket $BUCKET_NAME --versioning-configuration Status=Enabled
    aws s3api put-public-access-block \
        --bucket $BUCKET_NAME \
        --public-access-block-configuration \
        BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
fi

echo "📤 Uploading pandas layer to S3: s3://$BUCKET_NAME/pandas-layer.zip"
aws s3 cp layers/pandas-layer/pandas-layer.zip s3://$BUCKET_NAME/pandas-layer.zip --region $REGION

# Deploy CloudFormation stack
echo "🏗️  Deploying CloudFormation stack: $STACK_NAME"

aws cloudformation deploy \
    --template-file $TEMPLATE_FILE \
    --stack-name $STACK_NAME \
    --region $REGION \
    --capabilities CAPABILITY_IAM \
    --parameter-overrides \
        Environment=$ENVIRONMENT \
        ProjectName=$PROJECT_NAME \
    --tags \
        Environment=$ENVIRONMENT \
        Project=$PROJECT_NAME \
        Component=pandas-layer

echo "✅ Pandas layer deployment complete!"

# Get the layer ARN
LAYER_ARN=$(aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --region $REGION \
    --query 'Stacks[0].Outputs[?OutputKey==`PandasLayerArn`].OutputValue' \
    --output text)

echo "📋 Pandas Layer ARN: $LAYER_ARN"
echo "📦 S3 Bucket: s3://$BUCKET_NAME"

# Test the layer
echo "🧪 Testing pandas layer..."
aws lambda invoke \
    --function-name foreman-dev-s3-processor \
    --region $REGION \
    --payload '{"test": "pandas_layer"}' \
    /tmp/pandas-test-response.json

echo "✅ Pandas layer test complete!"
echo ""
echo "🎉 Pandas Lambda Layer successfully deployed!"
echo "   - Layer ARN: $LAYER_ARN"
echo "   - S3 Bucket: s3://$BUCKET_NAME"
echo "   - Stack Name: $STACK_NAME" 