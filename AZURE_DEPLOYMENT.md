# Azure Container Apps Deployment Guide

This guide explains how to deploy the TBSG AI RFP Assistant to Azure Container Apps using GitHub Actions CI/CD.

## 🏗️ Architecture

```
GitHub Repository → GitHub Actions → GitHub Container Registry → Azure Container Apps
```

## 📋 Prerequisites

1. **Azure Subscription**: Owner access to subscription `58a91cf0-0f39-45fd-a63e-5a9a28c7072b`
2. **Azure CLI**: Installed and configured
3. **GitHub Repository**: With admin access to configure secrets
4. **Existing Resources**:
   - Resource Group: `tolis-working-rg`
   - Container App Environment: `tolis-aca-env`

## 🚀 Quick Setup

### Option 1: Windows PowerShell
```powershell
.\setup-azure.ps1
```

### Option 2: Linux/Mac Bash
```bash
chmod +x setup-azure.sh
./setup-azure.sh
```

### Option 3: Manual Setup

1. **Login to Azure**:
   ```bash
   az login
   az account set --subscription 58a91cf0-0f39-45fd-a63e-5a9a28c7072b
   ```

2. **Create Service Principal**:
   ```bash
   az ad sp create-for-rbac \
     --name github-actions-tbsg-ai \
     --role contributor \
     --scopes /subscriptions/58a91cf0-0f39-45fd-a63e-5a9a28c7072b/resourceGroups/tolis-working-rg \
     --sdk-auth
   ```

## 🔐 GitHub Secrets Configuration

Add these secrets to your GitHub repository:

### 1. AZURE_CREDENTIALS
The JSON output from the service principal creation:
```json
{
  "clientId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "clientSecret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "subscriptionId": "58a91cf0-0f39-45fd-a63e-5a9a28c7072b",
  "tenantId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "activeDirectoryEndpointUrl": "https://login.microsoftonline.com",
  "resourceManagerEndpointUrl": "https://management.azure.com/",
  "activeDirectoryGraphResourceId": "https://graph.windows.net/",
  "sqlManagementEndpointUrl": "https://management.core.windows.net:8443/",
  "galleryEndpointUrl": "https://gallery.azure.com/",
  "managementEndpointUrl": "https://management.core.windows.net/"
}
```

### 2. TEMENOS_JWT_TOKEN
Your Temenos JWT token:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYXBvc3RvbG9zLmdlb3JnYXMiLCJlbWFpbCI6ImFwb3N0b2xvcy5nZW9yZ2FzQHRlbWVub3MuY29tIiwiZXhwIjoxNzYyMDcxNjIzLCJpYXQiOjE3NTk0Nzk2MjMsImlzcyI6InRic2cudGVtZW5vcy5jb20iLCJhdWQiOiJ0ZW1lbm9zLWFwaSJ9.8VuKANbWATjEg24yJU7sxrtilmeJNJEfZ-wUIZ1Y8q0
```

## 🔄 Deployment Process

### Automatic Deployment
1. **Push to main branch** triggers the CI/CD pipeline
2. **GitHub Actions** builds and pushes Docker image to GitHub Container Registry
3. **Azure Container Apps** pulls the image and deploys the application

### Manual Deployment
```bash
# Build and push image
docker build -t ghcr.io/georgasa/tbsg-ai-rfp-assistant:latest .
docker push ghcr.io/georgasa/tbsg-ai-rfp-assistant:latest

# Deploy to Azure Container Apps
az containerapp update \
  --name tbsg-ai-rfp-assistant \
  --resource-group tolis-working-rg \
  --image ghcr.io/georgasa/tbsg-ai-rfp-assistant:latest
```

## 🌐 Accessing the Application

After deployment, your application will be available at:
```
https://tbsg-ai-rfp-assistant.tolis-aca-env.azurecontainerapps.io
```

## 📊 Monitoring and Logs

### View Logs
```bash
az containerapp logs show \
  --name tbsg-ai-rfp-assistant \
  --resource-group tolis-working-rg \
  --follow
```

### Check Status
```bash
az containerapp show \
  --name tbsg-ai-rfp-assistant \
  --resource-group tolis-working-rg \
  --query properties.configuration.ingress.fqdn
```

## 🔧 Configuration

### Environment Variables
- `TEMENOS_JWT_TOKEN`: Temenos API authentication token
- `DEMO_MODE`: Set to "false" for production
- `PORT`: Application port (default: 5000)

### Resource Limits
- **CPU**: 0.5 cores
- **Memory**: 1.0 GiB
- **Min Replicas**: 1
- **Max Replicas**: 3

## 🚨 Troubleshooting

### Common Issues

1. **Authentication Failed**:
   - Verify `AZURE_CREDENTIALS` secret is correctly formatted
   - Check service principal permissions

2. **Image Pull Failed**:
   - Verify GitHub Container Registry permissions
   - Check image name and tag

3. **Application Not Starting**:
   - Check application logs
   - Verify environment variables
   - Check health endpoint: `/api/test-connection`

### Debug Commands
```bash
# Check container app status
az containerapp show --name tbsg-ai-rfp-assistant --resource-group tolis-working-rg

# View recent logs
az containerapp logs show --name tbsg-ai-rfp-assistant --resource-group tolis-working-rg --tail 100

# Test health endpoint
curl https://tbsg-ai-rfp-assistant.tolis-aca-env.azurecontainerapps.io/api/test-connection
```

## 🔄 CI/CD Pipeline

The GitHub Actions workflow includes:

1. **Test**: Python linting and testing
2. **Build**: Docker image creation and push to GitHub Container Registry
3. **Deploy**: Automatic deployment to Azure Container Apps

### Workflow Triggers
- Push to `main` branch
- Pull requests to `main` branch (test only)

## 📈 Scaling

The application automatically scales based on:
- CPU usage
- Memory usage
- HTTP requests

Configure scaling in the Azure portal or via CLI:
```bash
az containerapp update \
  --name tbsg-ai-rfp-assistant \
  --resource-group tolis-working-rg \
  --min-replicas 2 \
  --max-replicas 10
```

## 🔒 Security

- **Secrets**: Stored in Azure Key Vault (via Container Apps)
- **Network**: External ingress with HTTPS
- **Authentication**: JWT token for Temenos API
- **Container**: Non-root user, minimal base image

## 📞 Support

For issues or questions:
1. Check GitHub Actions logs
2. Review Azure Container Apps logs
3. Verify configuration and secrets
4. Contact the development team


