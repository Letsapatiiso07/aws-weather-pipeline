# 🌤️ AWS Real-Time Weather Analytics Pipeline

**Live automated weather data collection and processing system for South African cities**

[![AWS](https://img.shields.io/badge/AWS-Cloud-orange)](https://aws.amazon.com/)
[![Python](https://img.shields.io/badge/Python-3.9-blue)](https://python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Live-brightgreen)](README.md)

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   EventBridge   │───▶│   AWS Lambda    │───▶│   Amazon S3     │
│  (Every 15min)  │    │  Data Ingestion │    │   Raw Storage   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   DynamoDB      │    │   CloudWatch    │
                       │  Structured DB  │    │   Monitoring    │
                       └─────────────────┘    └─────────────────┘
```

## 📊 Real-Time Data Collection

**Cities Monitored**: Pretoria, Cape Town, Johannesburg, Durban  
**Collection Frequency**: Every 15 minutes (96 data points/day per city)  
**Data Metrics**: Temperature, Humidity, Pressure, Weather Conditions, Wind Speed  

## ⚡ Key Features

✅ **Fully Automated ETL Pipeline** - Zero manual intervention  
✅ **Real-Time Processing** - Live data ingestion and storage  
✅ **Dual Storage Strategy** - Raw JSON (S3) + Structured data (DynamoDB)  
✅ **Error Handling & Logging** - Comprehensive monitoring via CloudWatch  
✅ **Scalable Architecture** - Serverless, auto-scaling components  
✅ **Cost Optimized** - Runs entirely within AWS Free Tier  

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Compute** | AWS Lambda (Python 3.9) | Data processing & ETL |
| **Storage** | Amazon S3 | Raw data lake |
| **Database** | DynamoDB | Real-time querying |
| **Scheduler** | EventBridge | Automated triggers |
| **Monitoring** | CloudWatch | Logs & metrics |
| **API** | OpenWeatherMap | Weather data source |

## 📁 Project Structure

```
aws-weather-pipeline/
├── README.md
├── lambda_functions/
│   └── weather_ingestion/
│       ├── lambda_function.py
│       └── requirements.txt
├── architecture/
│   ├── architecture_diagram.png
│   └── aws_services.md
├── data_samples/
│   ├── sample_s3_data.json
│   └── sample_dynamodb_record.json
├── monitoring/
│   └── cloudwatch_metrics.md
├── deployment/
│   └── setup_guide.md
└── docs/
    ├── API_documentation.md
    └── troubleshooting.md
```

## 🚀 Quick Start

### Prerequisites
- AWS Account (Free Tier)
- OpenWeatherMap API Key
- Basic Python knowledge

### 1. Clone Repository
```bash
git clone https://github.com/Letsapatiiso07/aws-weather-pipeline.git
cd aws-weather-pipeline
```

### 2. AWS Resources Setup
- Create S3 bucket: `weather-data-pipeline-[your-initials]-2025`
- Create DynamoDB table: `WeatherData`
- Set up Lambda function with proper IAM roles
- Configure EventBridge scheduler

### 3. Deploy Lambda Function
- Upload `lambda_function.py` to AWS Lambda
- Set environment variables:
  - `WEATHER_API_KEY`: Your OpenWeatherMap API key
  - `S3_BUCKET_NAME`: Your S3 bucket name

### 4. Verify Pipeline
- Check CloudWatch logs for successful execution
- Verify data in S3 and DynamoDB
- Monitor EventBridge trigger schedule

## 📈 Data Flow

1. **EventBridge** triggers Lambda function every 15 minutes
2. **Lambda** fetches weather data from OpenWeatherMap API
3. **Raw JSON data** stored in S3 with timestamp partitioning
4. **Structured data** stored in DynamoDB for real-time queries
5. **CloudWatch** logs all operations for monitoring

## 🔧 Configuration

### Environment Variables
```python
WEATHER_API_KEY = "your_openweathermap_api_key"
S3_BUCKET_NAME = "your-s3-bucket-name"
```

### S3 Structure
```
weather-data-pipeline-bucket/
├── raw-data/
│   ├── Pretoria/2025/08/17/timestamp.json
│   ├── Cape_Town/2025/08/17/timestamp.json
│   ├── Johannesburg/2025/08/17/timestamp.json
│   └── Durban/2025/08/17/timestamp.json
├── processed-data/
└── archived-data/
```

### DynamoDB Schema
```json
{
  "city": "Pretoria",
  "timestamp": "2025-08-17T16:40:41.346533",
  "temperature": 17.44,
  "humidity": 65,
  "pressure": 1013.25,
  "weather_condition": "Clear",
  "wind_speed": 3.2
}
```

## 📊 Sample Data

### S3 Raw Data (JSON)
```json
{
  "coord": {"lon": 28.1881, "lat": -25.7463},
  "weather": [{"main": "Clear", "description": "clear sky"}],
  "main": {
    "temp": 17.44,
    "humidity": 65,
    "pressure": 1013.25
  },
  "wind": {"speed": 3.2},
  "name": "Pretoria",
  "timestamp": "2025-08-17T16:40:41.346533",
  "city": "Pretoria"
}
```

## 📋 Monitoring & Logging

- **CloudWatch Logs**: Real-time function execution logs
- **Success Rate**: 100% successful data collection
- **Average Execution Time**: ~4.7 seconds
- **Error Handling**: Comprehensive try-catch with detailed logging

## 💰 Cost Analysis

**Monthly AWS Costs (Free Tier)**:
- Lambda: 1M requests/month (FREE)
- S3: 5GB storage (FREE)
- DynamoDB: 25GB + 25 RCU/WCU (FREE)
- CloudWatch: Basic monitoring (FREE)

**Total Cost**: $0.00 (within free tier limits)

## 🔄 Future Enhancements

- [ ] Machine learning weather prediction models
- [ ] Real-time dashboard with AWS QuickSight
- [ ] Email alerts for extreme weather conditions
- [ ] Data quality validation pipeline
- [ ] Historical data analysis and trends
- [ ] API Gateway for external data access

## 🧪 Testing

### Manual Testing
```bash
# Test Lambda function directly in AWS Console
# Check CloudWatch logs for execution details
# Verify data appears in both S3 and DynamoDB
```

### Automated Testing
- EventBridge triggers every 15 minutes
- Lambda execution monitoring via CloudWatch
- Data validation checks in processing logic

## 📚 Documentation

- [Setup Guide](deployment/setup_guide.md)
- [Architecture Details](architecture/aws_services.md)
- [API Documentation](docs/API_documentation.md)
- [Troubleshooting](docs/troubleshooting.md)

## 🏆 Skills Demonstrated

### Data Engineering
- ✅ Real-time ETL pipeline design
- ✅ Data modeling and storage strategies
- ✅ API integration and data collection
- ✅ Error handling and data quality

### Cloud Architecture
- ✅ AWS serverless computing (Lambda)
- ✅ Event-driven architecture (EventBridge)
- ✅ Multi-tier storage (S3 + DynamoDB)
- ✅ Monitoring and logging (CloudWatch)

### Development Best Practices
- ✅ Infrastructure as Code principles
- ✅ Environment configuration management
- ✅ Comprehensive logging and monitoring
- ✅ Cost-optimized cloud resource usage

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Tiiso Letsapa**
- LinkedIn: [linkedin.com/in/tiiso-letsapa-664990209](https://linkedin.com/in/tiiso-letsapa-664990209)
- GitHub: [github.com/Letsapatiiso07](https://github.com/Letsapatiiso07)
- Email: Letsapamyron07@gmail.com

---

⭐ **Star this repository if you found it helpful!**

**Status**: 🟢 **LIVE & COLLECTING DATA** - Pipeline currently running and collecting weather data every 15 minutes from 4 South African cities.
