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
# Install dependencies
pip install -r requirements.txt

# Deploy infrastructure
./deploy.sh

# Or manually deploy if needed:
aws cloudformation deploy --template-file cloudformation/foreman-core.yaml --stack-name foreman-dev --region us-east-1 --capabilities CAPABILITY_NAMED_IAM --parameter-overrides Environment=dev ProjectName=foreman
```

3. **Test the deployment:**
```bash
# Dry run (validation only)
python main.py --file sample.csv --dry-run

# Submit to GraphQL
python main.py --file sample.csv --submit
```

## 📁 Project Structure

```
Foreman/
├── main.py                 # CLI entry point
├── mapper.py              # CSV field mapping
├── validator.py           # Data validation
├── gql_client.py          # GraphQL client
├── sample.csv             # Sample data
├── deploy.sh              # AWS deployment script
├── get-outputs.py         # Stack output retrieval
├── requirements.txt        # Python dependencies
├── ROADMAP.md             # Future implementation phases
├── .env                   # Environment variables
├── cloudformation/
│   └── foreman-core.yaml  # AWS infrastructure template
└── README.md              # This file
```

## 🔧 Features

### Core Functionality
- ✅ CSV ingestion and preview
- ✅ Field mapping (CSV → internal schema)
- ✅ Row-by-row validation
- ✅ GraphQL mutation submission
- ✅ AWS AppSync integration
- ✅ DynamoDB persistence

### AWS Infrastructure
- ✅ AppSync GraphQL API with API key authentication
- ✅ DynamoDB table for customers with point-in-time recovery
- ✅ Lambda resolvers with proper IAM permissions
- ✅ IAM roles and permissions (AppSync → Lambda → DynamoDB)
- ✅ CloudFormation deployment with exports
- ✅ Environment variable management

## 📊 Data Flow

1. **CSV Loading**: Reads CSV file and shows preview
2. **Field Mapping**: Maps CSV columns to internal schema
3. **Validation**: Validates each row for data quality
4. **GraphQL Submission**: Submits valid data to AppSync
5. **Persistence**: Data stored in DynamoDB

## 🎯 Usage Examples

### Dry Run (Validation Only)
```bash
python main.py --file sample.csv --dry-run
```

### Submit to GraphQL
```bash
python main.py --file sample.csv --submit
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
python main.py --file sample.csv --dry-run
python main.py --file sample.csv --submit
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
- **10 customers successfully created** with 100% success rate
- **Real-time data processing** from CSV to DynamoDB

### Planned Enhancements (See ROADMAP.md)
- [ ] **Phase 2**: S3 file upload pipeline with automated processing
- [ ] **Phase 3**: ECS containerization for scalable deployment
- [ ] **Phase 4**: Step Functions orchestration for complex workflows
- [ ] **Phase 5**: Web UI for user-friendly file upload
- [ ] **Phase 6**: Advanced features (multi-region, monitoring, security)

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