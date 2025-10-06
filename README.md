# TBSG AI RFP Assistant

A comprehensive AI-powered RFP (Request for Proposal) assistant that generates detailed technical analysis documents for Temenos banking solutions.

## 🚀 Features

- **AI-Powered Analysis**: Uses RAG (Retrieval-Augmented Generation) to analyze technology pillars
- **3-API Call Strategy**: Comprehensive overview + detailed technical insights + gap coverage
- **Professional Word Documents**: Generates structured reports with key points and detailed analysis
- **Multi-Pillar Support**: Architecture, Extensibility, DevOps, Security, Observability, Integration
- **Real-time Processing**: Fast analysis and document generation
- **Azure Deployment**: Cloud-native containerized application

## 📁 Project Structure

```
tbsg-ai/
├── app.py                 # Main Flask application
├── rag_client.py          # RAG API client for AI analysis
├── word_generator.py      # Word document generation
├── shared_config.py       # Shared configuration
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container configuration
├── docker-compose.yml    # Local development setup
├── static/               # Web assets
│   ├── css/
│   └── js/
├── templates/            # HTML templates
├── docs/                 # Documentation
│   ├── README.md
│   ├── AZURE_DEPLOYMENT.md
│   ├── DEPLOYMENT_GUIDE.md
│   ├── DEPLOYMENT_INSTRUCTIONS.md
│   └── GITHUB_SECRETS_SETUP.md
└── scripts/              # Deployment scripts
    ├── setup-azure.ps1
    └── setup-azure.sh
```

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **AI/ML**: RAG API integration
- **Document Generation**: python-docx
- **Frontend**: HTML, CSS, JavaScript
- **Containerization**: Docker
- **Cloud**: Azure Container Apps
- **CI/CD**: GitHub Actions

## 🚀 Quick Start

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

3. **Set environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Open http://localhost:5000 in your browser

### Docker Development

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

## 📋 API Endpoints

### POST /api/analyze
Analyze technology pillars and generate comprehensive reports.

**Request Body:**
```json
{
  "region": "GLOBAL",
  "model_id": "TechnologyOverview",
  "products": ["Transact"],
  "pillar": "Integration"
}
```

**Response:**
- Combined analysis with key points and detailed insights
- API call count tracking
- Structured data for document generation

### GET /api/reports
List available generated reports.

### GET /api/download/{filename}
Download generated Word documents.

## 🔧 Configuration

### Environment Variables

- `DEMO_MODE`: Enable/disable demo mode
- `PORT`: Application port (default: 5000)
- `TEMENOS_JWT_TOKEN`: JWT token for RAG API access

### RAG API Configuration

The application integrates with Temenos RAG API for AI-powered analysis:
- **Region**: GLOBAL
- **Model**: TechnologyOverview
- **API Limit**: 2000 characters per question

## 📊 Document Structure

Generated Word documents include:

1. **Product Title**: Main heading (e.g., "Transact")
2. **Key-points Section**: 
   - 6 bullet points with bold keywords
   - Descriptive paragraphs for each point
3. **Details Section**:
   - Comprehensive technical analysis
   - Performance metrics and benchmarks
   - Competitive advantages
   - Business value propositions
4. **Document Information**:
   - API calls made counter
   - Generation timestamp
   - Product and pillar information

## 🚀 Deployment

### Azure Container Apps

The application is deployed on Azure Container Apps with:
- **Automatic scaling**: 1-3 replicas based on demand
- **CI/CD**: GitHub Actions for automated deployment
- **Secrets management**: Secure JWT token storage
- **Monitoring**: Application logs and metrics
- **Health checks**: `/api/health` endpoint for liveness and readiness probes

### Deployment Process

1. **Push to main branch** triggers automatic deployment
2. **GitHub Actions** builds Docker image
3. **Azure Container Apps** deploys new revision
4. **Health checks** ensure successful deployment

### Local Development with Docker Compose

For local development with nginx reverse proxy:

```bash
# Start the full stack (app + nginx)
docker-compose up --build

# Access the application
# HTTP: http://localhost
# HTTPS: https://localhost (if SSL certificates are configured)
```

### Configuration Files

- **`azure-container-app.yaml`**: Kubernetes deployment for Azure Container Apps
- **`containerapp.yaml`**: Alternative Azure Container Apps configuration
- **`docker-compose.yml`**: Local development with nginx reverse proxy
- **`nginx.conf`**: Nginx configuration with security headers and SSL support

## 🧪 Testing

The application includes comprehensive error handling and validation:
- Input validation for API requests
- Error handling for RAG API failures
- Document generation validation
- Azure deployment health checks

## 📈 Performance

- **API Calls**: 3 calls per analysis (optimized for 100% key-point coverage)
- **Response Time**: < 30 seconds for complete analysis
- **Document Size**: 30KB+ comprehensive reports
- **Scalability**: Auto-scaling based on demand

## 🔒 Security

- **JWT Authentication**: Secure API access
- **Environment Variables**: Sensitive data protection
- **Azure Secrets**: Secure credential management
- **HTTPS**: Encrypted communication

## 📚 Documentation

- [Azure Deployment Guide](docs/AZURE_DEPLOYMENT.md)
- [Deployment Instructions](docs/DEPLOYMENT_INSTRUCTIONS.md)
- [GitHub Secrets Setup](docs/GITHUB_SECRETS_SETUP.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is proprietary to Temenos.

## 🆘 Support

For support and questions, contact the development team.

---

**Version**: 2.1.0  
**Last Updated**: October 2025