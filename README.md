# 🛠️ Foreman - Data Onboarding Platform

A robust data onboarding platform that ingests CSV files, validates data, and submits to AWS AppSync GraphQL API with DynamoDB backend. Features automated S3 processing, web interface, enhanced real-time progress tracking, and advanced duplicate prevention.

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
- ✅ **Enhanced Real-time Progress Tracking** - Live AWS Glue job monitoring with detailed metrics

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

## 🏭 AWS Glue Processing Tradeoffs

### Overview
Foreman uses AWS Glue for serverless ETL processing of CSV files, providing full pandas and numpy support. This section details the tradeoffs between cost, performance, and functionality.

### 💰 Cost Analysis

#### AWS Glue Costs (us-east-1)
- **DPU (Data Processing Unit)**: $0.44 per DPU-hour
- **Worker Type**: G.1X (1 DPU per worker)
- **Workers**: 2 workers = 2 DPUs
- **Processing Time**: ~30-60 seconds per file
- **Cost per File**: ~$0.007 - $0.015 per CSV file

#### Comparison with Lambda Processing
| Service | Cost per File | Processing Time | Pandas Support |
|---------|---------------|-----------------|----------------|
| **AWS Lambda** | ~$0.0001 | 5-15 seconds | ❌ Limited (timeout issues) |
| **AWS Glue** | ~$0.007-0.015 | 30-60 seconds | ✅ Full support |

### ⏱️ Performance Characteristics

#### Processing Time Breakdown
1. **Job Startup**: 15-30 seconds (cold start)
2. **CSV Reading**: 2-5 seconds (pandas)
3. **Data Processing**: 5-10 seconds (validation, transformation)
4. **DynamoDB Writes**: 5-15 seconds (batch operations)
5. **Total Time**: 30-60 seconds per file

#### Scalability
- **Concurrent Jobs**: Up to 5 concurrent runs (configurable)
- **File Size**: Handles files up to 1GB+ efficiently
- **Records**: Processes 10,000+ records per file
- **Auto-scaling**: Automatically scales based on data volume

### 🔧 Technical Tradeoffs

#### ✅ Advantages of AWS Glue
- **Full Pandas Support**: Complete numpy/pandas ecosystem
- **No Timeout Issues**: 15-minute job timeout vs Lambda's 15-minute limit
- **Large File Handling**: Efficient processing of large datasets
- **Memory**: 4GB+ memory vs Lambda's 3GB limit
- **Concurrent Processing**: Multiple files processed simultaneously
- **Error Handling**: Robust error recovery and retry mechanisms
- **Monitoring**: Comprehensive CloudWatch logging and metrics

#### ❌ Disadvantages of AWS Glue
- **Higher Cost**: 10-100x more expensive than Lambda

## 🚀 Enhanced Real-Time Progress Tracking

### Overview
The web interface now includes comprehensive real-time progress tracking for AWS Glue job processing, providing detailed insights into job execution and data processing metrics.

### ✨ Key Features

#### Real-Time Job Monitoring
- **Live Status Updates**: Real-time polling of Glue job status every 3 seconds
- **Stage Progression**: Visual progress through 6 processing stages:
  - 📤 Upload: File uploaded to S3
  - ⚡ Trigger: Glue job started
  - 🔄 Processing: Reading CSV data
  - ✅ Validation: Data validation
  - 💾 Database: Writing to DynamoDB
  - 🎉 Complete: Processing finished

#### Detailed Metrics Display
- **Job Duration**: Real-time calculation from Glue job start/end times
- **DPU Usage**: Actual Data Processing Unit consumption
- **Memory Usage**: Memory allocation and utilization
- **Processing Speed**: Records per second calculation
- **Record Counters**: Total, processed, successful, and error counts

#### Interactive Controls
- **Start Real-Time Updates**: Begin live monitoring
- **Pause Updates**: Temporarily stop polling
- **Check Job Status**: Manual status refresh
- **Auto-Stop**: Polling automatically stops when job completes

### 🔧 Technical Implementation

#### AWS Glue Integration
```python
# Real-time job status checking
glue = boto3.client('glue', region_name='us-east-1')
response = glue.get_job_runs(JobName=job_name, MaxResults=10)

# Timezone-aware duration calculation
now = datetime.now(timezone.utc)
duration = (now - job_run['StartedOn']).total_seconds()
```

#### DynamoDB Record Tracking
- **File-specific filtering**: Only counts records from current upload
- **Real-time counting**: Live updates as records are processed
- **Success/error tracking**: Separate counters for successful and failed records

#### UI Components
- **Progress Stages**: Visual stage progression with icons and colors
- **Progress Bar**: Overall completion percentage
- **Record Counters**: Large numerical displays for key metrics
- **Activity Log**: Timestamped status updates and events
- **Job Details Panel**: AWS Glue metrics and performance data

### 📊 Metrics Accuracy

#### Real-Time Calculations
- **Duration**: Calculated from actual Glue job start/end timestamps
- **Processing Speed**: Records processed ÷ actual duration
- **DPU Usage**: Real MaxCapacity from Glue job run
- **Memory**: Actual memory allocation (4GB+ for G.1X workers)

#### Error Handling
- **Timezone Management**: Proper handling of timezone-aware vs naive datetimes
- **Job Run Matching**: Accurate matching of job runs to specific file uploads
- **Fallback Values**: Graceful degradation when metrics unavailable

### 🎯 User Experience

#### Visual Feedback
- **Color-coded Stages**: Green (completed), Blue (active), Gray (pending)
- **Animated Progress**: Smooth progress bar updates
- **Status Messages**: Clear, descriptive status updates
- **Error Indicators**: Visual error states with detailed messages

#### Responsive Design
- **Mobile-friendly**: Works on all device sizes
- **Real-time Updates**: No page refresh required
- **Intuitive Controls**: Easy-to-use buttons and controls
- **Accessibility**: Clear visual hierarchy and contrast

### 🔍 Debugging Features

#### Development Tools
- **Debug Information**: Detailed API response data
- **Job Run Tracking**: Complete job run history
- **Error Logging**: Comprehensive error messages
- **Performance Metrics**: Detailed timing and resource usage

#### Monitoring
- **CloudWatch Integration**: Full logging and monitoring
- **Lambda Logs**: Detailed function execution logs
- **API Gateway Logs**: Request/response tracking
- **Glue Job Logs**: Complete job execution history
- **Slower Startup**: 15-30 second cold start vs Lambda's 1-2 seconds
- **Complexity**: More complex infrastructure and monitoring
- **Overhead**: Full Spark environment vs lightweight Lambda
- **Resource Usage**: Higher memory and CPU allocation

### 📊 Cost Optimization Strategies

#### 1. Batch Processing
```bash
# Process multiple files together
aws s3 cp samples/ s3://foreman-dev-csv-uploads/batch/
```

#### 2. Worker Configuration
```yaml
# Optimize for cost vs performance
WorkerType: G.1X  # Cost-effective
NumberOfWorkers: 2  # Balance performance/cost
```

#### 3. Job Scheduling
```yaml
# Process during off-peak hours
MaxConcurrentRuns: 3  # Reduce concurrent costs
```

### 🎯 When to Use AWS Glue vs Lambda

#### Use AWS Glue When:
- ✅ **Large files** (>1MB, >1000 records)
- ✅ **Complex data processing** (pandas operations, data transformation)
- ✅ **Batch processing** (multiple files)
- ✅ **Production workloads** (reliability over cost)
- ✅ **Data quality requirements** (validation, cleaning)

#### Use Lambda When:
- ✅ **Small files** (<1MB, <100 records)
- ✅ **Simple processing** (basic validation, format conversion)
- ✅ **Cost-sensitive** (budget constraints)
- ✅ **Real-time requirements** (sub-second response)
- ✅ **Development/testing** (quick iterations)

### 📈 Performance Monitoring

#### CloudWatch Metrics
- **Job Duration**: Track processing time trends
- **DPU Utilization**: Monitor resource efficiency
- **Error Rates**: Identify processing issues
- **Concurrent Jobs**: Optimize job scheduling

#### Cost Monitoring
```bash
# Monitor Glue costs
aws ce get-cost-and-usage \
  --time-period Start=2025-07-01,End=2025-07-31 \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --group-by Type=DIMENSION,Key=SERVICE \
  --filter '{"Dimensions":{"Key":"SERVICE","Values":["AWS Glue"]}}'
```

### 🔄 Migration Path

#### From Lambda to Glue
1. **Identify large files** (>1MB or >1000 records)
2. **Update processing logic** to use pandas
3. **Deploy Glue infrastructure** (CloudFormation)
4. **Update web interface** to use Glue API
5. **Monitor costs** and optimize configuration

#### Hybrid Approach
- **Small files**: Lambda processing (fast, cheap)
- **Large files**: Glue processing (reliable, powerful)
- **Auto-routing**: Based on file size/record count

### 📋 Best Practices

#### 1. File Size Optimization
```bash
# Compress large files before upload
gzip customers_large.csv
aws s3 cp customers_large.csv.gz s3://foreman-dev-csv-uploads/
```

#### 2. Batch Processing
```bash
# Process multiple files together
aws s3 sync samples/ s3://foreman-dev-csv-uploads/batch/
```

#### 3. Cost Monitoring
```bash
# Set up billing alerts
aws cloudwatch put-metric-alarm \
  --alarm-name "GlueCostAlert" \
  --alarm-description "Alert when Glue costs exceed threshold" \
  --metric-name BlendedCost \
  --namespace AWS/Billing \
  --statistic Average \
  --period 86400 \
  --threshold 10.0 \
  --comparison-operator GreaterThanThreshold
```

### 🎯 Summary

AWS Glue provides **reliable, scalable CSV processing** with full pandas support, but at a **higher cost** than Lambda. For production workloads with large files and complex data processing requirements, Glue offers the best balance of **functionality, reliability, and scalability**.

**Recommended**: Use Glue for production workloads with files >1MB or >1000 records, and Lambda for development/testing or small files.
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

### Planned Enhancement: Serverless Pandas Integration
- **Complex Data Transformations**: Advanced analytics and ML preprocessing
- **Statistical Analysis**: Aggregations, correlations, data profiling
- **Data Quality Scoring**: Automated data quality assessment
- **Multi-format Support**: Excel, JSON, Parquet processing

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

### 🐼 Serverless Pandas Migration Strategy

#### Current State vs Target State
| Feature | Current (Native CSV) | Target (Pandas) | Trade-off |
|---------|---------------------|-----------------|-----------|
| **Cold Start Time** | 1-3 seconds | 10-30 seconds | ⚠️ Slower but acceptable |
| **Memory Usage** | 128MB | 512MB+ | ⚠️ Higher cost but more powerful |
| **Package Size** | 1-5MB | 50-100MB | ⚠️ Larger but manageable |
| **Data Processing** | Basic validation | Complex transformations | ✅ Significant capability gain |
| **Analytics** | None | Statistical analysis | ✅ New capability |
| **ML Support** | None | Preprocessing pipelines | ✅ New capability |

#### Migration Phases
1. **Phase 1: Research & Documentation** ✅ (Current)
   - Document trade-offs and requirements
   - Plan implementation strategy
   - Update documentation

2. **Phase 2: Infrastructure Preparation**
   - [ ] Create Lambda layer with pandas
   - [ ] Update CloudFormation templates
   - [ ] Implement hybrid processing (simple = native, complex = pandas)
   - [ ] Add configuration flags for pandas usage

3. **Phase 3: Feature Implementation**
   - [ ] **Data Quality Scoring**: Automated assessment with pandas
   - [ ] **Statistical Analysis**: Aggregations, correlations, profiling
   - [ ] **Data Transformations**: Cleaning, enrichment, normalization
   - [ ] **ML Preprocessing**: Feature engineering, scaling, encoding

4. **Phase 4: Advanced Analytics**
   - [ ] **Business Intelligence**: Automated reporting and dashboards
   - [ ] **Anomaly Detection**: Statistical outlier detection
   - [ ] **Data Profiling**: Comprehensive data quality reports
   - [ ] **Predictive Analytics**: ML model integration

#### Implementation Options
1. **Lambda Layers** (Recommended)
   - Package pandas as separate layer
   - Conditional loading based on complexity
   - Maintains current simple processing

2. **Container Images**
   - Custom Docker with pandas pre-installed
   - Larger but more predictable environment
   - Better for complex dependencies

3. **Hybrid Approach** (Best of Both)
   - Simple operations: Native CSV processing
   - Complex operations: Pandas processing
   - Configuration-driven selection

#### Cost Impact Analysis
- **Current**: ~$0.0001 per 1000 requests
- **With Pandas**: ~$0.0005 per 1000 requests (5x increase)
- **Benefit**: 100x more processing capability
- **ROI**: Acceptable for complex data operations

### Infrastructure Scaling
- [ ] Auto-scaling configuration
- [ ] Backup and disaster recovery
- [ ] Security hardening and compliance
- [ ] Performance optimization

---

**🎯 Foreman is production-ready with advanced features, comprehensive testing, and scalable architecture!** 