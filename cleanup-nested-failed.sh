#!/bin/bash

# Clean up nested failed files in S3
echo "🧹 Cleaning up nested failed files in S3..."

BUCKET="foreman-dev-csv-uploads"

# List all files with nested failed/ prefixes
echo "📋 Finding nested failed files..."
aws s3 ls s3://$BUCKET/ --recursive | grep 'failed/failed/' | while read -r line; do
    # Extract the key from the ls output
    key=$(echo "$line" | awk '{print $4}')
    
    if [ ! -z "$key" ]; then
        echo "🔧 Processing: $key"
        
        # Extract the filename without the nested failed/ prefixes
        filename=$(echo "$key" | sed 's/failed\/failed\///g')
        
        # Move to the correct failed/ location
        echo "📦 Moving $key to failed/$filename"
        aws s3 mv "s3://$BUCKET/$key" "s3://$BUCKET/failed/$filename"
        
        if [ $? -eq 0 ]; then
            echo "✅ Successfully moved: $key"
        else
            echo "❌ Failed to move: $key"
        fi
    fi
done

echo "🎉 Cleanup completed!"
echo "📊 Current S3 structure:"
aws s3 ls s3://$BUCKET/ --recursive 