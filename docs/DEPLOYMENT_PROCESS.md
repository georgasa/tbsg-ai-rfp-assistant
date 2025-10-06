# TBSG AI RFP Assistant - Complete Deployment Process

## 📁 Project Structure Overview

### Core Application Files
- **`app.py`** - Main Flask application with API endpoints
- **`rag_client.py`** - RAG API client for AI analysis
- **`word_generator.py`** - Word document generation
- **`shared_config.py`** - Shared configuration management
- **`requirements.txt`** - Python dependencies

### Infrastructure Files
- **`Dockerfile`** - Container configuration
- **`docker-compose.yml`** - Local development setup
- **`azure-container-app.yaml`** - Azure Container Apps configuration
- **`containerapp.yaml`** - Alternative container configuration

### Frontend Files
- **`static/`** - Web assets (CSS, JavaScript)
- **`templates/`** - HTML templates
- **`swagger.json`** - API documentation

### Documentation & Scripts
- **`docs/`** - All documentation files
- **`scripts/`** - Deployment automation scripts
- **`tests/`** - Unit tests
- **`reports/`** - Generated analysis reports
- **`word_documents/`** - Generated Word documents

## 🛠️ Scripts Folder Contents

### `scripts/setup-azure.ps1` (Windows PowerShell)
**Purpose**: Automated Azure infrastructure setup for Windows users

**What it does**:
1. **Prerequisites Check**: Verifies Azure CLI installation and login
2. **Resource Creation**: Creates Azure resources if they don't exist:
   - Resource Group: `tolis-working-rg`
   - Container App Environment: `tolis-aca-env`
3. **Service Principal**: Creates GitHub Actions service principal
4. **Output**: Provides JSON credentials for GitHub secrets

**Usage**:
```powershell
.\scripts\setup-azure.ps1
```

**Parameters** (optional):
- `SubscriptionId`: Azure subscription ID
- `ResourceGroup`: Resource group name
- `ContainerAppEnv`: Container app environment name
- `ContainerAppName`: Container app name
- `Location`: Azure region

### `scripts/setup-azure.sh` (Linux/macOS)
**Purpose**: Automated Azure infrastructure setup for Unix systems

**What it does**: Same as PowerShell version but for Unix systems

**Usage**:
```bash
chmod +x scripts/setup-azure.sh
./scripts/setup-azure.sh
```

## 🔄 Complete Deployment Process

### Phase 1: Initial Setup (One-time)

#### 1.1 Prerequisites
```bash
# Install Azure CLI
# Windows: Download from Microsoft
# Linux: curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
# macOS: brew install azure-cli

# Login to Azure
az login

# Verify installation
az version
```

#### 1.2 Run Setup Script
```bash
# Windows
.\scripts\setup-azure.ps1

# Linux/macOS
./scripts/setup-azure.sh
```

#### 1.3 Configure GitHub Secrets
After running the setup script, add these secrets to your GitHub repository:

**`AZURE_CREDENTIALS`** (from script output):
```json
{
  "clientId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "clientSecret": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "subscriptionId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "tenantId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "activeDirectoryEndpointUrl": "https://login.microsoftonline.com",
  "resourceManagerEndpointUrl": "https://management.azure.com/",
  "activeDirectoryGraphResourceId": "https://graph.windows.net/",
  "sqlManagementEndpointUrl": "https://management.core.windows.net:8443/",
  "galleryEndpointUrl": "https://gallery.azure.com/",
  "managementEndpointUrl": "https://management.core.windows.net/"
}
```

**`TEMENOS_JWT_TOKEN`**:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Phase 2: Development Workflow

#### 2.1 Code Development
```bash
# Make changes to your code
# Test locally
python app.py

# Run tests
python -m pytest tests/

# Check code quality
flake8 .
```

#### 2.2 Git Workflow
```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "Add new feature: enhanced document generation"

# Push to trigger deployment
git push origin main
```

#### 2.3 Manual Deployment (Alternative)
```bash
# Build and push Docker image manually
docker build -t ghcr.io/georgasa/tbsg-ai-rfp-assistant:latest .
docker push ghcr.io/georgasa/tbsg-ai-rfp-assistant:latest

# Update Azure Container App
az containerapp update \
  --name tbsg-ai-rfp-assistant \
  --resource-group tolis-working-rg \
  --image ghcr.io/georgasa/tbsg-ai-rfp-assistant:latest
```

### Phase 3: CI/CD Pipeline (GitHub Actions)

#### 3.1 Pipeline Triggers
- **Push to main branch**: Automatic deployment
- **Pull request**: Testing only
- **Manual trigger**: Via GitHub Actions UI

#### 3.2 Pipeline Steps
```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Lint with flake8
        run: flake8 .
      - name: Test with pytest
        run: pytest tests/

  build-and-deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      - name: Login to GitHub Container Registry
        uses: docker/login-action@v2
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - name: Build and push Docker image
        run: |
          docker build -t ghcr.io/georgasa/tbsg-ai-rfp-assistant:latest .
          docker push ghcr.io/georgasa/tbsg-ai-rfp-assistant:latest
      - name: Deploy to Azure Container Apps
        uses: azure/container-apps-deploy-action@v1
        with:
          acrName: ghcr.io
          containerAppName: tbsg-ai-rfp-assistant
          resourceGroup: tolis-working-rg
          imageToDeploy: ghcr.io/georgasa/tbsg-ai-rfp-assistant:latest
```

#### 3.3 Deployment Process
1. **Code Push** → GitHub receives changes
2. **Pipeline Trigger** → GitHub Actions starts
3. **Testing** → Lint + Unit tests
4. **Build** → Docker image creation
5. **Push** → Image to GitHub Container Registry
6. **Deploy** → Azure Container Apps update
7. **Health Check** → Application availability verification

### Phase 4: Monitoring & Maintenance

#### 4.1 Application Monitoring
```bash
# Check container app status
az containerapp show \
  --name tbsg-ai-rfp-assistant \
  --resource-group tolis-working-rg

# View logs
az containerapp logs show \
  --name tbsg-ai-rfp-assistant \
  --resource-group tolis-working-rg \
  --tail 50

# Scale application
az containerapp update \
  --name tbsg-ai-rfp-assistant \
  --resource-group tolis-working-rg \
  --min-replicas 1 \
  --max-replicas 3
```

#### 4.2 Application URL
After successful deployment:
```
https://tbsg-ai-rfp-assistant.politeforest-ce794c6c.westeurope.azurecontainerapps.io
```

## 🔧 Configuration Files

### `azure-container-app.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tbsg-ai-rfp-assistant
spec:
  replicas: 1
  selector:
    matchLabels:
      app: tbsg-ai-rfp-assistant
  template:
    metadata:
      labels:
        app: tbsg-ai-rfp-assistant
    spec:
      containers:
      - name: tbsg-ai-rfp-assistant
        image: ghcr.io/georgasa/tbsg-ai-rfp-assistant:latest
        ports:
        - containerPort: 5000
        env:
        - name: DEMO_MODE
          value: "false"
        - name: PORT
          value: "5000"
        - name: TEMENOS_JWT_TOKEN
          valueFrom:
            secretKeyRef:
              name: temenos-jwt-token
              key: token
```

### `docker-compose.yml`
```yaml
version: '3.8'
services:
  tbsg-ai-rfp-assistant:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DEMO_MODE=false
      - PORT=5000
      - TEMENOS_JWT_TOKEN=${TEMENOS_JWT_TOKEN}
    volumes:
      - ./word_documents:/app/word_documents
      - ./reports:/app/reports
```

## 🚀 Quick Commands Reference

### Development
```bash
# Local development
python app.py

# Docker development
docker-compose up --build

# Run tests
python -m pytest tests/

# Code quality
flake8 .
```

### Deployment
```bash
# Manual deployment
git add .
git commit -m "Your changes"
git push

# Force deployment
git commit --allow-empty -m "Trigger deployment"
git push

# Manual Azure update
az containerapp update \
  --name tbsg-ai-rfp-assistant \
  --resource-group tolis-working-rg \
  --image ghcr.io/georgasa/tbsg-ai-rfp-assistant:latest
```

### Monitoring
```bash
# Check status
az containerapp show --name tbsg-ai-rfp-assistant --resource-group tolis-working-rg

# View logs
az containerapp logs show --name tbsg-ai-rfp-assistant --resource-group tolis-working-rg --tail 20

# Scale
az containerapp update --name tbsg-ai-rfp-assistant --resource-group tolis-working-rg --min-replicas 0 --max-replicas 3
```

## 📊 Deployment Timeline

| Phase | Duration | Description |
|-------|----------|-------------|
| Code Push | ~10s | Git push to GitHub |
| Pipeline Start | ~30s | GitHub Actions initialization |
| Testing | ~2min | Lint + Unit tests |
| Build | ~3min | Docker image creation |
| Push | ~1min | Image to registry |
| Deploy | ~2min | Azure Container Apps update |
| Health Check | ~30s | Application availability |
| **Total** | **~9min** | **Complete deployment** |

## 🔍 Troubleshooting

### Common Issues
1. **Pipeline Fails**: Check GitHub secrets configuration
2. **Build Fails**: Verify Dockerfile and dependencies
3. **Deploy Fails**: Check Azure credentials and permissions
4. **App Not Accessible**: Verify container app status and ingress

### Debug Commands
```bash
# Check Azure login
az account show

# Check resource group
az group show --name tolis-working-rg

# Check container app environment
az containerapp env show --name tolis-aca-env --resource-group tolis-working-rg

# Check container app
az containerapp show --name tbsg-ai-rfp-assistant --resource-group tolis-working-rg
```

---

**🎉 Your TBSG AI RFP Assistant is now ready for production deployment!**
