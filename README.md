# Temenos RAG AI System

A comprehensive web application for generating RFP responses using Temenos RAG API with a modern, Temenos Explorer-inspired interface.

## 🚀 Features

- **Technology Pillar Analysis**: Analyze 6 key technology pillars (Architecture, Extensibility, DevOps, Security, Observability, Integration)
- **RFP-Ready Output**: Generate professional Word documents suitable for RFP responses
- **Modern UI**: Temenos Explorer-inspired interface with dark blue sidebar and clean design
- **RESTful APIs**: Full API access for external integrations
- **Batch Processing**: Analyze multiple pillars simultaneously
- **Azure Ready**: Deployable as Azure Web App or Azure Functions

## 🏗️ Architecture

### Technology Pillars
- **Architecture**: Overall system architecture, deployment options, cloud capabilities
- **Extensibility**: Customization capabilities, development tools, frameworks
- **DevOps**: Deployment automation, CI/CD, operational tools
- **Security**: Security features, compliance, authentication, authorization
- **Observability**: Monitoring, logging, metrics, dashboards
- **Integration**: APIs, connectivity, data streaming

### Components
- **Web Application**: Flask-based UI with Temenos Explorer look & feel
- **RAG Client**: Core functionality for Temenos RAG API interaction
- **Word Generator**: Convert analysis to professional Word documents
- **API Layer**: RESTful endpoints for external access
- **Azure Functions**: Serverless deployment option

## 📋 Prerequisites

- Python 3.8+
- Temenos RAG API access
- JWT token for authentication

## 🛠️ Installation

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd tbsg-ai
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   # Set your JWT token
   export TEMENOS_JWT_TOKEN="your_jwt_token_here"
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Open browser to `http://localhost:5000`
   - Use the Temenos Explorer-inspired interface

### Azure Deployment

#### Option 1: Azure Web App

1. **Create Azure Web App**
   ```bash
   az webapp create --resource-group myResourceGroup --plan myAppServicePlan --name myWebApp --runtime "PYTHON|3.9"
   ```

2. **Configure environment variables**
   ```bash
   az webapp config appsettings set --resource-group myResourceGroup --name myWebApp --settings TEMENOS_JWT_TOKEN="your_jwt_token"
   ```

3. **Deploy the application**
   ```bash
   az webapp deployment source config --resource-group myResourceGroup --name myWebApp --repo-url <your-repo-url> --branch main --manual-integration
   ```

#### Option 2: Azure Functions

1. **Create Function App**
   ```bash
   az functionapp create --resource-group myResourceGroup --consumption-plan-location westeurope --runtime python --runtime-version 3.9 --functions-version 4 --name myFunctionApp --storage-account mystorageaccount
   ```

2. **Deploy functions**
   ```bash
   func azure functionapp publish myFunctionApp
   ```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `TEMENOS_JWT_TOKEN` | JWT token for Temenos RAG API | Yes |
| `FLASK_ENV` | Flask environment (development/production) | No |
| `AZURE_STORAGE_CONNECTION_STRING` | Azure Storage connection string | No |

### API Configuration

The system uses the following default configuration:

```python
API_CONFIG = {
    "base_url": "https://rag.temenos.com/api/v1",
    "timeout": 30,
    "max_retries": 3
}
```

## 📚 API Reference

### Endpoints

#### Health Check
```http
GET /api/health
```

#### Test Connection
```http
GET /api/test-connection
```

#### Get Pillars
```http
GET /api/pillars
```

#### Analyze Pillar
```http
POST /api/analyze
Content-Type: application/json

{
    "region": "GLOBAL",
    "model_id": "TechnologyOverview",
    "product_name": "Temenos Transact",
    "pillar": "Architecture"
}
```

#### Batch Analyze
```http
POST /api/batch-analyze
Content-Type: application/json

{
    "region": "GLOBAL",
    "model_id": "TechnologyOverview",
    "product_name": "Temenos Transact",
    "pillars": ["Architecture", "Security", "Integration"]
}
```

#### Generate Word Document
```http
POST /api/generate-word
Content-Type: application/json

{
    "analysis": { /* analysis data */ }
}
```

#### Download File
```http
GET /api/download/{filename}
```

#### List Reports
```http
GET /api/reports
```

#### List Word Documents
```http
GET /api/word-documents
```

## 🎨 UI Features

### Temenos Explorer Design
- **Dark Blue Sidebar**: Navigation with Temenos branding
- **Clean Interface**: Light blue background with white content boxes
- **Professional Typography**: Segoe UI font family
- **Responsive Design**: Works on desktop and mobile devices
- **Interactive Elements**: Hover effects and smooth transitions

### Key UI Components
- **Pillar Selection**: Grid-based selection with visual feedback
- **Progress Tracking**: Real-time progress bars for analysis
- **Results Display**: Professional table layout for results
- **File Management**: Download and manage generated documents
- **Status Indicators**: Connection status and system health

## 📊 Usage Examples

### Single Pillar Analysis

1. **Select Region**: Choose from Global, EMEA, Americas, APAC
2. **Select Product**: Choose Temenos product (Transact, Wealth, Digital)
3. **Select Pillar**: Choose technology pillar to analyze
4. **Start Analysis**: Click "Start Analysis" button
5. **Download Results**: Download Word document when complete

### Batch Analysis

1. **Select Multiple Pillars**: Choose multiple technology pillars
2. **Start Batch Analysis**: Click "Batch Analyze All" button
3. **Monitor Progress**: Watch real-time progress updates
4. **Download All**: Download all generated documents

### API Integration

```python
import requests

# Test connection
response = requests.get('https://your-app.azurewebsites.net/api/test-connection')
print(response.json())

# Analyze pillar
analysis_data = {
    "region": "GLOBAL",
    "model_id": "TechnologyOverview",
    "product_name": "Temenos Transact",
    "pillar": "Architecture"
}

response = requests.post(
    'https://your-app.azurewebsites.net/api/analyze',
    json=analysis_data
)
result = response.json()
```

## 🔒 Security

- **JWT Authentication**: Secure API access with JWT tokens
- **Input Validation**: All inputs are validated and sanitized
- **File Security**: Generated files are stored securely
- **HTTPS Only**: All communications use HTTPS in production
- **Environment Variables**: Sensitive data stored in environment variables

## 📈 Performance

- **Optimized API Calls**: Reduced from 108 to 48 API calls per analysis
- **Efficient Processing**: Streamlined analysis workflow
- **Caching**: Intelligent caching of frequently accessed data
- **Async Processing**: Non-blocking operations for better UX

## 🐛 Troubleshooting

### Common Issues

1. **Connection Failed**
   - Check JWT token validity
   - Verify network connectivity
   - Check API endpoint availability

2. **Analysis Failed**
   - Verify pillar selection
   - Check product/model compatibility
   - Review error logs

3. **Word Generation Failed**
   - Ensure python-docx is installed
   - Check file permissions
   - Verify analysis data format

### Logs

- **Application Logs**: Check console output for errors
- **Azure Logs**: Use Azure portal for production logs
- **API Logs**: Monitor API response codes and errors

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🔄 Version History

### v2.0.0 (Current)
- Complete UI redesign with Temenos Explorer look & feel
- RESTful API implementation
- Azure deployment support
- Optimized analysis workflow
- Professional Word document generation

### v1.0.0
- Initial release
- Basic pillar analysis
- Command-line interface
- JSON output only

---

**Built with ❤️ for Temenos RFP Excellence**
