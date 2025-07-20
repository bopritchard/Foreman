# 🛠️ Foreman - Data Onboarding Platform

A robust data onboarding platform that ingests CSV files, validates data, and submits to AWS AppSync GraphQL API with DynamoDB backend. Features automated S3 processing, web interface, and advanced duplicate prevention.

## 🏗️ Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   CSV File  │───▶│   Foreman   │───▶│  AppSync    │───▶│  DynamoDB   │
│             │    │    CLI       │    │  GraphQL    │    │   Table     │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                          │                     │
                          ▼                     ▼
                   ┌─────────────┐    ┌─────────────┐
                   │ Validation  │    │   Lambda    │
                   │   Engine    │    │  Resolvers  │
                   └─────────────┘    └─────────────┘

┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Web UI    │───▶│   S3 Bucket │───▶│   Lambda    │
│             │    │             │    │  Processor  │
└─────────────┘    └─────────────┘    └─────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- AWS CLI configured
- AWS Account with appropriate permissions

### Installation

1. **Clone and setup:**
```bash
git clone <repository>
cd Foreman
pip install -r requirements.txt
```

2. **Deploy AWS Infrastructure:**
```bash
# Deploy core infrastructure
./scripts/deploy.sh

# Deploy S3 pipeline
./scripts/deploy-s3-pipeline-simple.sh

# Deploy web interface
./scripts/deploy-web-simple.sh
```

3. **Access the platform:**
```bash
# Local CLI processing
python main.py --file samples/customers_valid.csv --submit

# Web interface
# Open: https://u26lyxxmqh.execute-api.us-east-1.amazonaws.com/prod

# S3 automated processing
aws s3 cp samples/customers_valid.csv s3://foreman-dev-csv-uploads/
```

## 📁 Project Structure

```
Foreman/
├── main.py                 # CLI entry point
├── gql_client.py          # GraphQL client
├── models/                 # Data models (Customer, Project, etc.)
├── validator.py            # Data validation utilities
├── mapper.py               # Field mapping utilities
├── requirements.txt        # Python dependencies
├── scripts/                # Deployment and utility scripts
│   ├── deploy.sh              # Core AWS deployment script
│   ├── deploy-s3-pipeline-simple.sh  # S3 pipeline deployment
│   ├── deploy-web-simple.sh   # Web interface deployment
│   ├── get-outputs.py         # Stack output retrieval
│   ├── cleanup-nested-failed.sh # S3 cleanup utilities
│   └── list-samples.sh        # List available sample files
├── samples/                # Comprehensive test data files
│   ├── customers_valid.csv        # Valid customer data
│   ├── customers_large.csv        # Large dataset (100+ records)
│   ├── customers_medium.csv       # Medium dataset
│   ├── customers_small.csv        # Small dataset
│   ├── customers_with_duplicates.csv # Dataset with duplicates
│   ├── customers_invalid.csv      # Invalid data for testing
│   └── customers_test_duplicates.csv # Test duplicate detection
├── cloudformation/         # AWS infrastructure templates
│   ├── foreman-core.yaml      # Core AWS infrastructure
│   ├── foreman-s3-pipeline-simple.yaml # S3 processing pipeline
│   └── foreman-web-simple.yaml  # Web interface
├── UPLOAD_GUIDE.md        # Comprehensive upload guide
└── README.md              # This file
```

## 🔧 Features

### Core Functionality
- ✅ CSV ingestion and preview
- ✅ Auto-detection of data types (Customer, Project, etc.)
- ✅ Row-by-row validation
- ✅ GraphQL mutation submission
- ✅ AWS AppSync integration
- ✅ DynamoDB persistence
- ✅ Multiple upload methods (CLI, Web, S3)

### Advanced Features
- ✅ **File Hash Duplicate Prevention** - Prevents duplicate file uploads
- ✅ **Email Uniqueness** - GSI-based email validation with fallback
- ✅ **Real-time Processing** - S3 event-driven automated processing
- ✅ **Web Interface** - User-friendly upload interface with live status
- ✅ **Comprehensive Test Data** - Multiple sample files for testing
- ✅ **Active Visual Feedback** - Spinning indicators and progress dots

### AWS Infrastructure
- ✅ AppSync GraphQL API with API key authentication
- ✅ DynamoDB table with GSI for email uniqueness
- ✅ Lambda resolvers with proper IAM permissions
- ✅ S3 bucket with automated processing pipeline
- ✅ API Gateway web interface with active feedback
- ✅ IAM roles and permissions (AppSync → Lambda → DynamoDB)
- ✅ CloudFormation deployment with exports
- ✅ Environment variable management

## 📊 Data Flow

### Local Processing (with pandas):
1. **CSV Loading**: Reads CSV file and shows preview
2. **Auto-detection**: Identifies data type (Customer, Project, etc.)
3. **Validation**: Validates each row for data quality
4. **GraphQL Submission**: Submits valid data to AppSync
5. **Persistence**: Data stored in DynamoDB

### S3 Automated Processing (native CSV):
1. **File Upload**: CSV uploaded to S3 bucket
2. **Hash Calculation**: MD5 hash computed for duplicate detection
3. **Duplicate Check**: Verifies if file content already processed
4. **Event Trigger**: S3 event triggers Lambda function
5. **Processing**: Validates and processes data with email uniqueness
6. **GraphQL Submission**: Submits to AppSync API
7. **File Management**: Moves processed files to processed/failed folders

### Web Interface Processing:
1. **File Upload**: User uploads CSV through web interface
2. **Real-time Feedback**: Active spinner and progress indicators
3. **Status Polling**: Continuous status checking with visual feedback
4. **Result Display**: Shows processing results or duplicate detection

## 🎯 Usage Examples

### Local CLI Processing
```bash
# Dry run (validation only)
python main.py --file samples/customers_valid.csv --dry-run

# Submit to GraphQL
python main.py --file samples/customers_valid.csv --submit

# List available models
python main.py --list-models
```

### Web Interface
```bash
# Access deployed web interface
# https://u26lyxxmqh.execute-api.us-east-1.amazonaws.com/prod
```

### S3 Automated Processing
```bash
# Upload to S3 (triggers automatic processing)
aws s3 cp samples/customers_valid.csv s3://foreman-dev-csv-uploads/

# Check processed files
aws s3 ls s3://foreman-dev-csv-uploads/processed/
```

### Sample Output
```
📂 Loading file: customers_valid.csv
✅ CSV Loaded.

📊 Preview (first 5 rows):
        name                                    email  ...         phone   signupDate
0  Alice Cooper              alice.cooper@test.com  ...  555-123-4567  2023-01-15
1    Bob Smith                bob.smith@test.com  ...  555-234-5678  2023-02-20

🔁 Mapping fields...
🗺️ Columns after mapping:
Index(['name', 'email', 'phone', 'signupDate'], dtype='object')

🚀 Submit mode: Submitting to GraphQL...
✅ Row 1: Customer created with ID customer_20250720_123456_0
✅ Row 2: Customer created with ID customer_20250720_123456_1

📊 Submission Summary:
  ✅ Successful: 3
  ❌ Failed: 0
  📈 Total: 3
```

## 🔐 AWS Configuration

The deployment creates:
- **AppSync GraphQL API** with API key authentication
- **DynamoDB table** with GSI for email uniqueness
- **Lambda functions** for GraphQL resolvers and S3 processing
- **S3 bucket** with automated processing pipeline
- **API Gateway** web interface with active feedback
- **IAM roles** with minimal required permissions

### Environment Variables
After deployment, your `.env` file will be updated with:
- `GRAPHQL_URL`: AppSync GraphQL endpoint
- `APPSYNC_API_KEY`: API key for authentication
- `AWS_*`: AWS credentials and configuration

## 🧪 Testing

### Comprehensive Test Data
```bash
# List available test files
./scripts/list-samples.sh

# Test with different scenarios
python main.py --file samples/customers_valid.csv --submit
python main.py --file samples/customers_with_duplicates.csv --submit
python main.py --file samples/customers_invalid.csv --submit
```

### Web Interface Testing
1. Upload `samples/customers_valid.csv` - Should process successfully
2. Upload same file again - Should show "Duplicate File Skipped"
3. Upload `samples/customers_large.csv` - Should process 100+ records

### S3 Pipeline Testing
```bash
# Test duplicate prevention
aws s3 cp samples/customers_small.csv s3://foreman-dev-csv-uploads/
aws s3 cp samples/customers_small.csv s3://foreman-dev-csv-uploads/duplicate.csv
# Second upload should be skipped due to same content
```

### AWS Console Access
- **AppSync Console**: View GraphQL API and test queries
- **DynamoDB Console**: View stored customer data with GSI
- **CloudFormation Console**: Monitor infrastructure deployment
- **S3 Console**: Check processed/failed files

## 🔄 Development Workflow

1. **Local Development**: Use `--dry-run` to test validation
2. **Deploy Changes**: Run `./scripts/deploy.sh` to update infrastructure
3. **Test Integration**: Use `--submit` to test GraphQL submission
4. **Monitor**: Check AWS CloudWatch logs for Lambda execution

## 📈 Current Status ✅

### Phase 1 Complete: Core Infrastructure
- ✅ AppSync GraphQL API deployed
- ✅ DynamoDB table with GSI for email uniqueness
- ✅ Lambda resolvers with proper IAM permissions
- ✅ Local CLI processing with pandas

### Phase 2 Complete: S3 Pipeline
- ✅ S3 bucket with automated processing
- ✅ Lambda function for S3 event processing
- ✅ File hash duplicate prevention
- ✅ Email uniqueness checking with GSI
- ✅ Native CSV processing (no pandas dependency)

### Phase 3 Complete: Web Interface
- ✅ API Gateway web interface deployed
- ✅ Active visual feedback with spinners
- ✅ Real-time status polling
- ✅ Duplicate detection messaging
- ✅ Responsive design

### Advanced Features
- ✅ **File Hash Duplicate Prevention** - MD5-based content detection
- ✅ **Email Uniqueness** - GSI with scan fallback
- ✅ **Comprehensive Test Data** - Multiple scenarios covered
- ✅ **Active Visual Feedback** - Spinning indicators and progress dots
- ✅ **Production Ready** - Scalable, reliable, cost-effective

## 🛠️ Troubleshooting

### Common Issues

**ModuleNotFoundError: No module named 'dotenv'**
```bash
pip install python-dotenv
```

**AWS CLI not configured**
```bash
aws configure
```

**File processing fails**
```bash
# Check S3 bucket for failed files
aws s3 ls s3://foreman-dev-csv-uploads/failed/

# Check Lambda logs
aws logs tail /aws/lambda/foreman-dev-s3-processor --follow
```

**Web interface not responding**
```bash
# Check API Gateway logs
aws logs tail /aws/lambda/foreman-dev-web-api --follow
```

## 🏆 Best Practices Implemented

### Serverless Architecture
- **Native CSV Processing**: Fast, lightweight, cost-effective
- **No Pandas Dependency**: Faster cold starts, smaller packages
- **Event-Driven**: S3 triggers for automated processing
- **Scalable**: Auto-scaling Lambda functions

### Data Integrity
- **File Hash Prevention**: Prevents duplicate file processing
- **Email Uniqueness**: GSI-based validation with fallback
- **Comprehensive Validation**: Row-by-row error checking
- **Error Handling**: Graceful failure with detailed messages

### User Experience
- **Active Feedback**: Spinning indicators and progress dots
- **Real-time Status**: Live polling with visual updates
- **Clear Messaging**: Duplicate detection and error reporting
- **Responsive Design**: Works on all devices

## 🚀 Next Steps

### Planned Enhancements
- [ ] **Multi-region deployment** for global availability
- [ ] **CloudWatch monitoring** with custom dashboards
- [ ] **Step Functions orchestration** for complex workflows
- [ ] **Additional data models** (Jobs, Invoices, etc.)
- [ ] **Advanced analytics** and reporting features

### Infrastructure Scaling
- [ ] Auto-scaling configuration
- [ ] Backup and disaster recovery
- [ ] Security hardening and compliance
- [ ] Performance optimization

---

**🎯 Foreman is production-ready with advanced features, comprehensive testing, and scalable architecture!** 