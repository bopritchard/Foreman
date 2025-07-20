#!/bin/bash

# Deploy AWS Glue Infrastructure for Foreman
set -e

ENVIRONMENT=${1:-dev}
STACK_NAME="foreman-s3-pipeline-simple-${ENVIRONMENT}"
REGION="us-east-1"

echo "🚀 Deploying Foreman Glue Infrastructure to AWS..."
echo "📦 Deploying CloudFormation stack: ${STACK_NAME}"

# Deploy the CloudFormation stack
aws cloudformation deploy \
    --template-file cloudformation/foreman-s3-pipeline-simple.yaml \
    --stack-name ${STACK_NAME} \
    --region ${REGION} \
    --capabilities CAPABILITY_NAMED_IAM \
    --parameter-overrides \
        Environment=${ENVIRONMENT} \
        ProjectName=foreman

echo "⏳ Waiting for stack deployment to complete..."
aws cloudformation wait stack-create-complete --stack-name ${STACK_NAME} --region ${REGION}

# Get the Glue scripts bucket name
GLUE_SCRIPTS_BUCKET=$(aws cloudformation describe-stacks \
    --stack-name ${STACK_NAME} \
    --region ${REGION} \
    --query 'Stacks[0].Outputs[?OutputKey==`GlueScriptsBucketName`].OutputValue' \
    --output text)

echo "📤 Uploading Glue job script to S3..."
aws s3 cp glue_job.py s3://${GLUE_SCRIPTS_BUCKET}/

echo "✅ Glue Infrastructure deployment completed successfully!"

echo ""
echo "🔧 Infrastructure Details:"
echo "  Glue Job Name: foreman-${ENVIRONMENT}-csv-processing-job"
echo "  Glue Scripts Bucket: ${GLUE_SCRIPTS_BUCKET}"
echo "  S3 Upload Bucket: foreman-${ENVIRONMENT}-csv-uploads"
echo ""
echo "🧪 Test the Glue job:"
echo "   aws s3 cp samples/customers_valid.csv s3://foreman-${ENVIRONMENT}-csv-uploads/"
echo ""
echo "📊 Monitor Glue job runs:"
echo "   aws glue get-job-runs --job-name foreman-${ENVIRONMENT}-csv-processing-job --region ${REGION}"
echo ""
echo "🔍 Check CloudWatch logs:"
echo "   aws logs tail /aws-glue/jobs/output --follow"
echo ""
echo "📋 Verify data in DynamoDB:"
echo "   aws dynamodb scan --table-name foreman-${ENVIRONMENT}-customers --region ${REGION}" 