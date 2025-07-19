# 📤 Foreman Upload Guide

## 🎯 **Upload Methods Available**

Foreman supports multiple ways to upload and process CSV files, from simple CLI commands to automated S3 pipelines.

---

## 🔄 **Method 1: Local Processing (Current)**

### **Quick Start:**
```bash
# Process a local CSV file
python main_v2.py --file sample.csv --submit

# Auto-detects data type and processes
python main_v2.py --file sample_projects.csv --submit
```

### **Features:**
- ✅ **Immediate feedback** - see results in terminal
- ✅ **Auto-detection** - automatically detects customer vs project data
- ✅ **Validation** - shows validation errors before submission
- ✅ **No setup required** - works with existing infrastructure

### **Example Output:**
```bash
📂 Loading file: sample.csv
✅ CSV Loaded.
🔍 Model Detection: Auto-detected model: customer
✅ Using model: customer
🚀 Submit mode: Submitting to GraphQL...
✅ Row 1: Customer created with ID abc123-def456
📊 Submission Summary:
  ✅ Successful: 10
  ❌ Failed: 0
  📈 Total: 10
```

---

## 🌐 **Method 2: Web Interface (New)**

### **Start Web Server:**
```bash
# Install Flask
pip install flask

# Start web interface
python web_upload.py
```

### **Access Interface:**
- **URL**: http://localhost:5000
- **Features**: Drag-and-drop upload, real-time feedback
- **Auto-processing**: Files uploaded to S3 trigger processing

### **Web Interface Features:**
- 🎨 **Modern UI** - Clean, responsive design
- 📤 **Drag & Drop** - Easy file selection
- ✅ **File Validation** - Only accepts CSV files
- 📊 **Status Display** - Shows processing status
- 🔄 **Auto-processing** - Triggers S3 pipeline

---

## ☁️ **Method 3: S3 Pipeline (Phase 2)**

### **Deploy S3 Pipeline:**
```bash
# Deploy S3 infrastructure
./deploy-s3-pipeline.sh
```

### **Upload Methods:**

#### **AWS CLI:**
```bash
# Upload to S3 bucket
aws s3 cp sample.csv s3://foreman-dev-csv-uploads/

# Upload with custom name
aws s3 cp sample.csv s3://foreman-dev-csv-uploads/customers-2024.csv
```

#### **AWS Console:**
1. Go to S3 Console
2. Navigate to `foreman-dev-csv-uploads` bucket
3. Click "Upload" and select your CSV file
4. File automatically triggers processing

#### **Programmatic Upload (Python):**
```python
import boto3

s3 = boto3.client('s3')
s3.upload_file('sample.csv', 'foreman-dev-csv-uploads', 'sample.csv')
```

#### **Bash Script:**
```bash
#!/bin/bash
# upload.sh
BUCKET="foreman-dev-csv-uploads"
FILE="$1"

if [ -z "$FILE" ]; then
    echo "Usage: ./upload.sh <csv-file>"
    exit 1
fi

aws s3 cp "$FILE" "s3://$BUCKET/"
echo "✅ Uploaded $FILE to S3"
echo "🔄 Processing started automatically..."
```

---

## 📊 **Processing Flow**

### **S3 Pipeline Flow:**
```
1. 📤 Upload CSV to S3
   ↓
2. 🔔 S3 Event Notification
   ↓
3. ⚡ Lambda Function Triggered
   ↓
4. 🔍 Auto-detect Data Type
   ↓
5. ✅ Validate & Process
   ↓
6. 🚀 Submit to GraphQL API
   ↓
7. 💾 Store in DynamoDB
   ↓
8. 📁 Move to processed/failed folder
```

### **Monitoring:**
- **CloudWatch Logs**: View processing logs
- **S3 Console**: Check file status
- **DynamoDB Console**: View stored data
- **CloudWatch Dashboard**: Processing metrics

---

## 🎯 **Supported Data Types**

### **Auto-Detection:**
- **Customer CSV**: Detects `full_name`, `email`, `phone` fields
- **Project CSV**: Detects `project_name`, `budget`, `status` fields
- **Future**: Easy to add new data types

### **Manual Model Selection:**
```bash
# Force specific model
python main_v2.py --file data.csv --model customer --submit
python main_v2.py --file data.csv --model project --submit
```

### **List Available Models:**
```bash
python main_v2.py --list-models
# Output:
# 📋 Available Models:
#   - customer
#   - project
```

---

## 📋 **CSV Format Requirements**

### **Customer CSV:**
```csv
full_name,email,companyName,phone,joined_on
John Doe,john@example.com,Acme Corp,555-1234,2024-01-15
Jane Smith,jane@example.com,Tech Inc,555-5678,2024-01-16
```

### **Project CSV:**
```csv
project_name,project_description,start_date,end_date,project_status,project_budget,customer_id
Office Renovation,Complete renovation,2024-01-15,2024-06-30,In Progress,50000,CUST001
```

### **Validation Rules:**
- ✅ **Required fields** must be present
- ✅ **Email format** validation
- ✅ **Date format** validation
- ✅ **Phone number** format validation
- ✅ **Budget** numeric validation

---

## 🚀 **Quick Start Commands**

### **Local Processing:**
```bash
# Test validation only
python main_v2.py --file sample.csv --dry-run

# Submit to GraphQL
python main_v2.py --file sample.csv --submit

# List available models
python main_v2.py --list-models
```

### **Web Interface:**
```bash
# Start web server
python web_upload.py

# Open browser to http://localhost:5000
```

### **S3 Pipeline:**
```bash
# Deploy S3 infrastructure
./deploy-s3-pipeline.sh

# Upload file
aws s3 cp sample.csv s3://foreman-dev-csv-uploads/
```

---

## 🔧 **Troubleshooting**

### **Common Issues:**

#### **File Not Found:**
```bash
❌ File not found: sample.csv
# Solution: Check file path and name
```

#### **No Model Detected:**
```bash
❌ No suitable model found for this CSV structure
# Solution: Check CSV column names or specify model manually
```

#### **Validation Errors:**
```bash
❌ Row 1 errors:
  - Required field 'email' is missing or empty
# Solution: Fix CSV data or column names
```

#### **S3 Upload Failed:**
```bash
❌ Upload failed: Access Denied
# Solution: Check AWS credentials and bucket permissions
```

### **Debug Commands:**
```bash
# Check AWS credentials
aws sts get-caller-identity

# List S3 buckets
aws s3 ls

# Check CloudWatch logs
aws logs describe-log-groups --log-group-name-prefix foreman
```

---

## 📈 **Performance & Scaling**

### **Processing Capacity:**
- **Local**: Limited by your machine
- **S3 Pipeline**: Unlimited parallel processing
- **Lambda**: Up to 15 minutes per file
- **Auto-scaling**: Handles multiple files simultaneously

### **File Size Limits:**
- **Local**: Limited by available memory
- **S3**: Up to 5TB per file
- **Lambda**: 512MB memory, 15-minute timeout

### **Cost Optimization:**
- **S3 Storage**: ~$0.023 per GB/month
- **Lambda**: ~$0.20 per 1M requests
- **DynamoDB**: ~$1.25 per GB/month
- **Processing**: ~$0.001 per CSV file

---

## 🎉 **Next Steps**

### **Phase 2 Enhancements:**
- [ ] **Real-time notifications** (SNS/SES)
- [ ] **Progress tracking** in web interface
- [ ] **Batch processing** for large files
- [ ] **Error recovery** and retry logic

### **Phase 3 Features:**
- [ ] **API endpoints** for programmatic uploads
- [ ] **Webhook notifications** for processing results
- [ ] **Advanced validation** rules
- [ ] **Data transformation** capabilities

---

**Ready to upload? Choose your preferred method and start processing data! 🚀** 