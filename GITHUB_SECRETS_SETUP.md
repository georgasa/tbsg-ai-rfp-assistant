# GitHub Secrets Setup Guide

## 🔐 **Required GitHub Secrets**

To enable automatic deployment to Azure Container Apps, you need to add these secrets to your GitHub repository.

### **Step 1: Go to GitHub Repository Settings**

1. Navigate to: https://github.com/georgasa/tbsg-ai-rfp-assistant
2. Click **Settings** (top menu)
3. Click **Secrets and variables** → **Actions** (left sidebar)

### **Step 2: Add AZURE_CREDENTIALS Secret**

1. Click **"New repository secret"**
2. **Name**: `AZURE_CREDENTIALS`
3. **Value**: Copy and paste this JSON exactly:

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

4. Click **"Add secret"**

### **Step 3: Add TEMENOS_JWT_TOKEN Secret**

1. Click **"New repository secret"** again
2. **Name**: `TEMENOS_JWT_TOKEN`
3. **Value**: Copy and paste this token exactly:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYXBvc3RvbG9zLmdlb3JnYXMiLCJlbWFpbCI6ImFwb3N0b2xvcy5nZW9yZ2FzQHRlbWVub3MuY29tIiwiZXhwIjoxNzYyMDcxNjIzLCJpYXQiOjE3NTk0Nzk2MjMsImlzcyI6InRic2cudGVtZW5vcy5jb20iLCJhdWQiOiJ0ZW1lbm9zLWFwaSJ9.8VuKANbWATjEg24yJU7sxrtilmeJNJEfZ-wUIZ1Y8q0
```

4. Click **"Add secret"**

## ✅ **Verification**

After adding both secrets, you should see:
- `AZURE_CREDENTIALS` in your secrets list
- `TEMENOS_JWT_TOKEN` in your secrets list

## 🚀 **Trigger Deployment**

Once the secrets are added:

1. **Push any change** to the `main` branch
2. **GitHub Actions** will automatically:
   - Build the Docker image
   - Push to GitHub Container Registry
   - Deploy to Azure Container Apps

## 🌐 **Access Your Application**

After successful deployment, your application will be available at:
```
https://tbsg-ai-rfp-assistant.tolis-aca-env.azurecontainerapps.io
```

## 📊 **Monitor Deployment**

1. Go to **Actions** tab in your GitHub repository
2. Click on the latest workflow run
3. Monitor the build and deployment progress

## 🔧 **Troubleshooting**

### If deployment fails:
1. Check the **Actions** logs for error details
2. Verify both secrets are correctly added
3. Ensure the Azure resources exist:
   - Resource Group: `tolis-working-rg`
   - Container App Environment: `tolis-aca-env`

### If application doesn't start:
1. Check Azure Container Apps logs
2. Verify the JWT token is valid
3. Test the health endpoint: `/api/test-connection`

## 📞 **Support**

If you encounter issues:
1. Check GitHub Actions logs
2. Review Azure Container Apps logs
3. Verify configuration and secrets
4. Contact the development team
