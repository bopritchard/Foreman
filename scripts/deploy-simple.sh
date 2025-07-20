#!/bin/bash

# Simple deployment script for Foreman infrastructure
set -e

ENVIRONMENT=${1:-dev}
STACK_NAME="foreman-s3-pipeline-simple-${ENVIRONMENT}"
REGION="us-east-1"

echo "🚀 Deploying Foreman Infrastructure to AWS..."
echo "📦 Stack: ${STACK_NAME}"

# Deploy the CloudFormation stack
aws cloudformation deploy \
    --template-file cloudformation/foreman-s3-pipeline-simple.yaml \
    --stack-name ${STACK_NAME} \
    --region ${REGION} \
    --capabilities CAPABILITY_NAMED_IAM \
    --parameter-overrides \
        Environment=${ENVIRONMENT} \
        ProjectName=foreman

echo "✅ Deployment completed!" 