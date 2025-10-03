# Azure Container Apps Deployment Guide

## 🚀 **Quick Setup Instructions**

### **Step 1: Add GitHub Secrets**

1. Go to: https://github.com/georgasa/tbsg-ai-rfp-assistant/settings/secrets/actions
2. Add these two secrets:

#### **AZURE_CREDENTIALS**
```json
{
  "clientId": "390bf354-99b6-40b1-87ac-77bef53181a6",
  "clientSecret": "5Mu8Q~GFc~YdZkWMcUs3XidPlkaCvsaXI9dbHdcH",
  "subscriptionId": "58a91cf0-0f39-45fd-a63e-5a9a28c7072b",
  "tenantId": "d5d2540f-f60a-45ad-86a9-e2e792ee6669",
  "activeDirectoryEndpointUrl": "https://login.microsoftonline.com",
  "resourceManagerEndpointUrl": "https://management.azure.com/",
  "activeDirectoryGraphResourceId": "https://graph.windows.net/",
  "sqlManagementEndpointUrl": "https://management.core.windows.net:8443/",
  "galleryEndpointUrl": "https://gallery.azure.com/",
  "managementEndpointUrl": "https://management.core.windows.net/"
}
```

#### **TEMENOS_JWT_TOKEN**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYXBvc3RvbG9zLmdlb3JnYXMiLCJlbWFpbCI6ImFwb3N0b2xvcy5nZW9yZ2FzQHRlbWVub3MuY29tIiwiZXhwIjoxNzYyMDcxNjIzLCJpYXQiOjE3NTk0Nzk2MjMsImlzcyI6InRic2cudGVtZW5vcy5jb20iLCJhdWQiOiJ0ZW1lbm9zLWFwaSJ9.8VuKANbWATjEg24yJU7sxrtilmeJNJEfZ-wUIZ1Y8q0
```

### **Step 2: Deploy**

1. **Push any change** to the `main` branch
2. **GitHub Actions** will automatically deploy to Azure Container Apps
3. **Access your app** at: https://tbsg-ai-rfp-assistant.tolis-aca-env.azurecontainerapps.io

## 📊 **What Happens During Deployment**

1. **Build**: Docker image is created and pushed to GitHub Container Registry
2. **Deploy**: Azure Container Apps pulls the image and deploys the application
3. **Scale**: Application automatically scales based on demand (1-3 replicas)

## 🔧 **Configuration**

- **Resource Group**: `tolis-working-rg`
- **Container App Environment**: `tolis-aca-env`
- **Container App Name**: `tbsg-ai-rfp-assistant`
- **CPU**: 0.5 cores
- **Memory**: 1.0 GiB
- **Min Replicas**: 1
- **Max Replicas**: 3

## 📈 **Monitoring**

- **GitHub Actions**: Monitor build and deployment progress
- **Azure Portal**: View application logs and metrics
- **Health Check**: `/api/test-connection` endpoint

## 🚨 **Troubleshooting**

### If deployment fails:
1. Check GitHub Actions logs
2. Verify secrets are correctly added
3. Ensure Azure resources exist

### If application doesn't start:
1. Check Azure Container Apps logs
2. Verify JWT token is valid
3. Test health endpoint

## 🎯 **Ready for Production**

Once deployed, your RFP Assistant will be:
- ✅ **Scalable**: Auto-scales based on demand
- ✅ **Secure**: HTTPS with proper authentication
- ✅ **Monitored**: Built-in logging and health checks
- ✅ **Reliable**: 99.9% uptime SLA
- ✅ **Global**: Accessible from anywhere
