# 🛠️ Foreman - Data Onboarding Platform

A robust data onboarding platform that ingests CSV files, validates data, and submits to AWS AppSync GraphQL API with DynamoDB backend.

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
./deploy.sh

# Deploy S3 pipeline (optional)
./deploy-s3-pipeline.sh

# Deploy web interface (optional)
./deploy-web-simple.sh
```

3. **Access the platform:**
```bash
# Local CLI processing
python main.py --file sample.csv --submit

# Web interface (if deployed)
# Open: https://u26lyxxmqh.execute-api.us-east-1.amazonaws.com/prod

# S3 automated processing (if deployed)
aws s3 cp sample.csv s3://foreman-dev-csv-uploads/
```

## 📁 Project Structure

```
Foreman/
├── main.py                 # CLI entry point
├── gql_client.py          # GraphQL client
├── models/                 # Data models (Customer, Project, etc.)
├── web_upload.py          # Local Flask web interface
├── validator.py            # Data validation utilities
├── mapper.py               # Field mapping utilities
├── requirements.txt        # Python dependencies
├── scripts/                # Deployment and utility scripts
│   ├── deploy.sh              # Core AWS deployment script
│   ├── deploy-s3-pipeline.sh  # S3 pipeline deployment
│   ├── deploy-web-simple.sh   # Web interface deployment
│   ├── get-outputs.py         # Stack output retrieval
│   └── cleanup-nested-failed.sh # S3 cleanup utilities
├── samples/                # Sample data files
│   ├── sample.csv             # Sample customer data
│   ├── sample_projects.csv    # Sample project data
│   └── test_*.csv             # Test data files
├── cloudformation/         # AWS infrastructure templates
│   ├── foreman-core.yaml      # Core AWS infrastructure
│   ├── foreman-s3-pipeline.yaml # S3 processing pipeline
│   └── foreman-web-simple.yaml  # Web interface
├── UPLOAD_GUIDE.md        # Comprehensive upload guide
├── ROADMAP.md             # Future implementation phases
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

### AWS Infrastructure
- ✅ AppSync GraphQL API with API key authentication
- ✅ DynamoDB table for customers with point-in-time recovery
- ✅ Lambda resolvers with proper IAM permissions
- ✅ S3 bucket with automated processing pipeline
- ✅ API Gateway web interface
- ✅ IAM roles and permissions (AppSync → Lambda → DynamoDB)
- ✅ CloudFormation deployment with exports
- ✅ Environment variable management

## 📊 Data Flow

### Local Processing:
1. **CSV Loading**: Reads CSV file and shows preview
2. **Auto-detection**: Identifies data type (Customer, Project, etc.)
3. **Validation**: Validates each row for data quality
4. **GraphQL Submission**: Submits valid data to AppSync
5. **Persistence**: Data stored in DynamoDB

### S3 Automated Processing:
1. **File Upload**: CSV uploaded to S3 bucket
2. **Event Trigger**: S3 event triggers Lambda function
3. **Auto-detection**: Lambda identifies data type
4. **Processing**: Validates and processes data
5. **GraphQL Submission**: Submits to AppSync API
6. **File Management**: Moves processed files to processed/failed folders

## 🎯 Usage Examples

### Local CLI Processing
```bash
# Dry run (validation only)
python main.py --file samples/sample.csv --dry-run

# Submit to GraphQL
python main.py --file samples/sample.csv --submit

# List available models
python main.py --list-models
```

### Web Interface
```bash
# Start local web server
python web_upload.py

# Or access deployed web interface
# https://u26lyxxmqh.execute-api.us-east-1.amazonaws.com/prod
```

### S3 Automated Processing
```bash
# Upload to S3 (triggers automatic processing)
aws s3 cp samples/sample.csv s3://foreman-dev-csv-uploads/
```

### Sample Output
```
📂 Loading file: sample.csv
✅ CSV Loaded.

📊 Preview (first 5 rows):
        full_name                                  email  ...         phone   joined_on
0  David Harrison  david.harrison@turnerconstruction.com  ...  212-555-0101  2022-11-03
1   Sarah Bennett              sarah.bennett@bechtel.com  ...  415-555-0134  2023-01-14

🔁 Mapping fields...
🗺️ Columns after mapping:
Index(['name', 'customerEmail', 'companyName', 'phone', 'signupDate'], dtype='object')

🚀 Submit mode: Submitting to GraphQL...
✅ Row 1: Customer created with ID dd8b43b6-2705-4f66-a4ad-d97313556a51
✅ Row 2: Customer created with ID 91aaad65-2a9a-4f2e-8622-880f8853a0d3

📊 Submission Summary:
  ✅ Successful: 10
  ❌ Failed: 0
  📈 Total: 10
```

## 🔐 AWS Configuration

The deployment creates:
- **AppSync GraphQL API** with API key authentication
- **DynamoDB table** for customer data
- **Lambda functions** for GraphQL resolvers
- **IAM roles** with minimal required permissions

### Environment Variables
After deployment, your `.env` file will be updated with:
- `GRAPHQL_URL`: AppSync GraphQL endpoint
- `APPSYNC_API_KEY`: API key for authentication
- `AWS_*`: AWS credentials and configuration

## 🧪 Testing

### Local Testing
```bash
# Test with sample data
python main.py --file samples/sample.csv --dry-run
python main.py --file samples/sample.csv --submit
```

### AWS Console Access
- **AppSync Console**: View GraphQL API and test queries
- **DynamoDB Console**: View stored customer data
- **CloudFormation Console**: Monitor infrastructure deployment

## 🔄 Development Workflow

1. **Local Development**: Use `--dry-run` to test validation
2. **Deploy Changes**: Run `./deploy.sh` to update infrastructure
3. **Test Integration**: Use `--submit` to test GraphQL submission
4. **Monitor**: Check AWS CloudWatch logs for Lambda execution

## 📈 Next Steps

### Current Status ✅
- **Phase 1 Complete**: Core infrastructure deployed and working
- **Phase 2 Complete**: S3 pipeline with automated processing
- **Phase 3 Complete**: Web interface deployed to AWS
- **Multiple upload methods** available (CLI, Web, S3)
- **Auto-detection** of data types (Customer, Project)
- **Scalable architecture** ready for production

### Planned Enhancements (See ROADMAP.md)
- [ ] **Phase 4**: ECS containerization for scalable deployment
- [ ] **Phase 5**: Step Functions orchestration for complex workflows
- [ ] **Phase 6**: Advanced features (multi-region, monitoring, security)
- [ ] **Phase 7**: Additional data models (Jobs, Invoices, etc.)

### Infrastructure Scaling
- [ ] Multi-region deployment
- [ ] CloudWatch monitoring and alerting
- [ ] Auto-scaling configuration
- [ ] Backup and disaster recovery

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

**CloudFormation deployment fails**
- Check AWS credentials
- Verify region is `us-east-1`
- Ensure sufficient IAM permissions

### Debug Commands
```bash
# Check AWS credentials
aws sts get-caller-identity

# List CloudFormation stacks
aws cloudformation list-stacks --region us-east-1

# Get stack outputs and update .env
python get-outputs.py

# Test AppSync endpoint
curl -X POST \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{"query":"query { getCustomer(id: \"test\") { id name email } }"}' \
  YOUR_APPSYNC_URL
```

## 📄 License

This project is for demonstration purposes.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**Built with ❤️ for AWS infrastructure demonstration** 