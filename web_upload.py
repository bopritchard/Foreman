#!/usr/bin/env python3
"""
Simple Flask web interface for uploading CSV files to S3
"""

import os
import boto3
from flask import Flask, request, render_template_string, flash, redirect, url_for
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)
app.secret_key = 'foreman-secret-key'

# Configuration
S3_BUCKET = os.getenv('S3_BUCKET', 'foreman-dev-csv-uploads')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')

# Initialize S3 client
s3_client = boto3.client('s3', region_name=AWS_REGION)

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Foreman - CSV Upload</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        .upload-form {
            border: 2px dashed #ddd;
            padding: 40px;
            text-align: center;
            border-radius: 10px;
            margin: 20px 0;
            transition: border-color 0.3s;
        }
        .upload-form:hover {
            border-color: #007bff;
        }
        .file-input {
            margin: 20px 0;
        }
        .submit-btn {
            background: #007bff;
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        .submit-btn:hover {
            background: #0056b3;
        }
        .alert {
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }
        .alert-success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .alert-error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .info {
            background: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }
        .status {
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🛠️ Foreman CSV Upload</h1>
        
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">
                        {{ message }}
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <div class="info">
            <h3>📋 How it works:</h3>
            <ol>
                <li>Upload your CSV file using the form below</li>
                <li>File is automatically uploaded to S3</li>
                <li>S3 triggers Lambda function for processing</li>
                <li>Data is validated and submitted to GraphQL API</li>
                <li>Results are stored in DynamoDB</li>
            </ol>
        </div>
        
        <form method="POST" enctype="multipart/form-data" class="upload-form">
            <h3>📤 Upload CSV File</h3>
            <p>Select a CSV file to upload and process:</p>
            
            <div class="file-input">
                <input type="file" name="file" accept=".csv" required>
            </div>
            
            <button type="submit" class="submit-btn">🚀 Upload & Process</button>
        </form>
        
        <div class="status">
            <h3>📊 Processing Status</h3>
            <p><strong>S3 Bucket:</strong> {{ s3_bucket }}</p>
            <p><strong>Region:</strong> {{ aws_region }}</p>
            <p><strong>Auto-detection:</strong> Customer, Project, and other models</p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if file was uploaded
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        
        # Check if file was selected
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        # Check if file is CSV
        if not file.filename.lower().endswith('.csv'):
            flash('Please upload a CSV file', 'error')
            return redirect(request.url)
        
        try:
            # Secure the filename
            filename = secure_filename(file.filename)
            
            # Upload to S3
            s3_client.upload_fileobj(
                file,
                S3_BUCKET,
                filename,
                ExtraArgs={'ContentType': 'text/csv'}
            )
            
            flash(f'✅ File "{filename}" uploaded successfully! Processing started...', 'success')
            
        except Exception as e:
            flash(f'❌ Upload failed: {str(e)}', 'error')
    
    return render_template_string(
        HTML_TEMPLATE,
        s3_bucket=S3_BUCKET,
        aws_region=AWS_REGION
    )

if __name__ == '__main__':
    print("🌐 Starting Foreman Web Upload Interface...")
    print(f"📦 S3 Bucket: {S3_BUCKET}")
    print(f"🌍 Region: {AWS_REGION}")
    print("🔗 Open http://localhost:5000 in your browser")
    print("")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 