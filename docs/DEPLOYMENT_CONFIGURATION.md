# Deployment Configuration Guide

## 📋 Configuration Files Overview

This document provides a comprehensive overview of all deployment configuration files and their purposes.

## 🐳 Docker Configuration

### `Dockerfile`
- **Purpose**: Container image definition for the Flask application
- **Base Image**: Python 3.11-slim
- **Port**: 5000
- **Environment**: Production-ready with security best practices

### `docker-compose.yml`
- **Purpose**: Local development with nginx reverse proxy
- **Services**:
  - `tbsg-ai-app`: Main Flask application
  - `nginx`: Reverse proxy with SSL support
- **Ports**: 
  - HTTP: 80
  - HTTPS: 443
- **Features**: Health checks, volume mounts, restart policies

### `nginx.conf`
- **Purpose**: Nginx configuration for reverse proxy
- **Features**:
  - Security headers (X-Frame-Options, CSP, HSTS)
  - SSL/TLS termination
  - Load balancing
  - Health check endpoints
  - Static file caching

## ☁️ Azure Container Apps Configuration

### `azure-container-app.yaml`
- **Purpose**: Kubernetes deployment for Azure Container Apps
- **API Version**: apps/v1
- **Resources**:
  - CPU: 250m-500m
  - Memory: 512Mi-1Gi
- **Health Checks**: `/api/health` endpoint
- **Secrets**: JWT token from Kubernetes secrets

### `containerapp.yaml`
- **Purpose**: Alternative Azure Container Apps configuration
- **API Version**: apps/v1
- **Resources**:
  - CPU: 0.25-0.5 cores
  - Memory: 0.5Gi-1Gi
- **Health Checks**: `/api/health` endpoint
- **Secrets**: JWT token from Container Apps secrets

## 🔧 Environment Configuration

### `env.example`
- **Purpose**: Template for environment variables
- **Sections**:
  - Temenos RAG API Configuration
  - Flask Configuration
  - Azure Configuration
  - Docker Configuration
  - Logging Configuration

### Key Environment Variables

| Variable | Purpose | Default | Required |
|----------|---------|---------|----------|
| `TEMENOS_JWT_TOKEN` | RAG API authentication | - | Yes |
| `DEMO_MODE` | Enable demo mode | false | No |
| `PORT` | Application port | 5000 | No |
| `FLASK_ENV` | Flask environment | development | No |
| `AZURE_WEBAPP_NAME` | Azure app name | tbsg-ai-rfp-assistant | No |

## 🚀 Deployment Options

### 1. Local Development
```bash
# Option A: Direct Python
python app.py

# Option B: Docker Compose (with nginx)
docker-compose up --build
```

### 2. Azure Container Apps
```bash
# Deploy using Azure CLI
az containerapp create --file azure-container-app.yaml

# Or using the alternative configuration
az containerapp create --file containerapp.yaml
```

### 3. Kubernetes
```bash
# Deploy to any Kubernetes cluster
kubectl apply -f azure-container-app.yaml
```

## 🔒 Security Configuration

### Security Headers (nginx.conf)
- `X-Frame-Options: SAMEORIGIN`
- `X-XSS-Protection: 1; mode=block`
- `X-Content-Type-Options: nosniff`
- `Content-Security-Policy: default-src 'self'`
- `Strict-Transport-Security: max-age=31536000`

### Container Security
- Non-root user execution
- Minimal base image (Python slim)
- No unnecessary packages
- Health check endpoints

### Secrets Management
- **Local**: Environment variables in `.env`
- **Azure**: Container Apps secrets
- **Kubernetes**: Secret objects
- **Docker**: Environment variables

## 📊 Monitoring & Health Checks

### Health Check Endpoints
- **Application**: `/api/health`
- **Connection Test**: `/api/test-connection`

### Monitoring Configuration
- **Liveness Probe**: 30s initial delay, 10s period
- **Readiness Probe**: 5s initial delay, 5s period
- **Health Check Timeout**: 10s
- **Retry Attempts**: 3

### Logging
- **Level**: INFO
- **Format**: Structured JSON
- **Output**: Console + File
- **Rotation**: Daily

## 🔄 CI/CD Integration

### GitHub Actions
- **Trigger**: Push to main branch
- **Steps**:
  1. Test and lint
  2. Build Docker image
  3. Push to GitHub Container Registry
  4. Deploy to Azure Container Apps

### Docker Registry
- **Registry**: GitHub Container Registry
- **Image**: `ghcr.io/georgasa/tbsg-ai-rfp-assistant`
- **Tag**: `latest`

## 🛠️ Troubleshooting

### Common Issues

1. **Health Check Failures**
   - Verify `/api/health` endpoint is accessible
   - Check application logs
   - Ensure proper port configuration

2. **Secret Management**
   - Verify JWT token is valid
   - Check secret references in deployment files
   - Ensure proper permissions

3. **Resource Limits**
   - Monitor CPU and memory usage
   - Adjust limits based on actual usage
   - Check for memory leaks

### Debug Commands

```bash
# Check container status
docker-compose ps

# View application logs
docker-compose logs tbsg-ai-app

# Test health endpoint
curl http://localhost/api/health

# Check nginx configuration
docker-compose exec nginx nginx -t
```

## 📈 Scaling Configuration

### Azure Container Apps
- **Min Replicas**: 1
- **Max Replicas**: 3
- **Scaling Metrics**: CPU, Memory, HTTP requests

### Kubernetes
- **Horizontal Pod Autoscaler**: Based on CPU/Memory
- **Vertical Pod Autoscaler**: Resource optimization
- **Cluster Autoscaler**: Node scaling

## 🔧 Customization

### Adding New Environment Variables
1. Update `env.example`
2. Add to deployment files
3. Update application code
4. Test configuration

### Modifying Resource Limits
1. Update deployment files
2. Consider application requirements
3. Monitor performance
4. Adjust as needed

### SSL Configuration
1. Add SSL certificates to `ssl/` directory
2. Update nginx configuration
3. Test HTTPS endpoints
4. Update health checks

---

**Last Updated**: October 2025  
**Version**: 2.1.0
