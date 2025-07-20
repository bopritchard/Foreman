#!/usr/bin/env python3
"""
AWS Glue Job for CSV Processing with Pandas
Foreman Data Onboarding Platform
"""

import sys
import json
import boto3
import pandas as pd
import hashlib
import uuid
from datetime import datetime
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext
from pyspark.sql import SparkSession

# Get job parameters
args = getResolvedOptions(sys.argv, [
    'JOB_NAME',
    's3_bucket',
    's3_key',
    'job_run_id'
])

# Initialize Spark and Glue context
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

def process_csv_with_pandas():
    """Process CSV file using pandas for data validation and transformation"""
    
    s3_bucket = args['s3_bucket']
    s3_key = args['s3_key']
    job_run_id = args['job_run_id']
    
    print(f"🚀 Starting Glue job: {job_run_id}")
    print(f"📁 Processing file: s3://{s3_bucket}/{s3_key}")
    
    try:
        # Download CSV file from S3
        s3_client = boto3.client('s3')
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('foreman-dev-customers')
        
        # Download file to local storage
        local_file = f"/tmp/{s3_key.split('/')[-1]}"
        s3_client.download_file(s3_bucket, s3_key, local_file)
        
        print(f"📥 Downloaded file to: {local_file}")
        
        # Read CSV with pandas
        df = pd.read_csv(local_file)
        print(f"📊 Loaded {len(df)} records from CSV")
        
        # Calculate file hash for duplicate prevention
        with open(local_file, 'rb') as f:
            file_content = f.read()
            file_hash = hashlib.md5(file_content).hexdigest()
        
        print(f"🔐 File hash: {file_hash}")
        
        # Check for duplicate file content
        response = table.scan(
            FilterExpression='file_hash = :file_hash',
            ExpressionAttributeValues={':file_hash': file_hash}
        )
        
        if response['Items']:
            print(f"⚠️ File content with hash {file_hash} has already been processed. Skipping.")
            return {
                'success': True,
                'records_processed': 0,
                'message': 'File content already processed',
                'file_hash': file_hash
            }
        
        # Process records
        successful_records = 0
        error_records = 0
        errors = []
        
        for index, row in df.iterrows():
            try:
                # Validate required fields
                if 'email' not in row or pd.isna(row['email']):
                    raise ValueError("Email is required")
                
                if 'name' not in row or pd.isna(row['name']):
                    raise ValueError("Name is required")
                
                # Clean and validate data
                email = str(row['email']).strip().lower()
                name = str(row['name']).strip()
                phone = str(row.get('phone', '')).strip() if 'phone' in row and not pd.isna(row['phone']) else ''
                signup_date = str(row.get('signupDate', '')).strip() if 'signupDate' in row and not pd.isna(row['signupDate']) else ''
                
                # Validate email format
                if '@' not in email or '.' not in email:
                    raise ValueError("Invalid email format")
                
                # Check for duplicate email
                email_response = table.scan(
                    FilterExpression='email = :email',
                    ExpressionAttributeValues={':email': email}
                )
                
                if email_response['Items']:
                    print(f"⚠️ Duplicate email found: {email}")
                    error_records += 1
                    errors.append(f"Row {index + 1}: Duplicate email {email}")
                    continue
                
                # Create customer record
                customer_id = f"customer_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{index}"
                
                customer_data = {
                    'id': customer_id,
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'signupDate': signup_date,
                    'source_file': s3_key,
                    'file_hash': file_hash,
                    'job_run_id': job_run_id,
                    'processed_at': datetime.now().isoformat(),
                    'processing_method': 'aws_glue_pandas'
                }
                
                # Write to DynamoDB
                table.put_item(Item=customer_data)
                successful_records += 1
                
                print(f"✅ Processed record {index + 1}: {email}")
                
            except Exception as e:
                error_records += 1
                error_msg = f"Row {index + 1}: {str(e)}"
                errors.append(error_msg)
                print(f"❌ Error processing record {index + 1}: {str(e)}")
        
        # Move processed file
        processed_key = f"processed/{s3_key}"
        s3_client.copy_object(
            Bucket=s3_bucket,
            CopySource={'Bucket': s3_bucket, 'Key': s3_key},
            Key=processed_key
        )
        s3_client.delete_object(Bucket=s3_bucket, Key=s3_key)
        
        print(f"📁 Moved file to: {processed_key}")
        
        # Return results
        result = {
            'success': True,
            'records_processed': len(df),
            'successful_records': successful_records,
            'error_records': error_records,
            'errors': errors,
            'file_hash': file_hash,
            'job_run_id': job_run_id,
            'message': f'Processing complete! {successful_records} records processed successfully.'
        }
        
        print(f"🎉 Job completed successfully!")
        print(f"   Total records: {len(df)}")
        print(f"   Successful: {successful_records}")
        print(f"   Errors: {error_records}")
        
        return result
        
    except Exception as e:
        print(f"❌ Job failed with error: {str(e)}")
        
        # Move failed file
        failed_key = f"failed/{s3_key}"
        try:
            s3_client.copy_object(
                Bucket=s3_bucket,
                CopySource={'Bucket': s3_bucket, 'Key': s3_key},
                Key=failed_key
            )
            s3_client.delete_object(Bucket=s3_bucket, Key=s3_key)
            print(f"📁 Moved failed file to: {failed_key}")
        except Exception as move_error:
            print(f"⚠️ Could not move failed file: {str(move_error)}")
        
        return {
            'success': False,
            'records_processed': 0,
            'successful_records': 0,
            'error_records': 0,
            'errors': [f'Job failed: {str(e)}'],
            'message': f'Job failed: {str(e)}'
        }

# Execute the job
if __name__ == "__main__":
    result = process_csv_with_pandas()
    print(f"📊 Final result: {json.dumps(result, indent=2)}")
    
    # Exit with appropriate code
    if result['success']:
        job.commit()
        print("✅ Job committed successfully")
    else:
        print("❌ Job failed")
        sys.exit(1) 