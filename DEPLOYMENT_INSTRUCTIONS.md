# Azure Container Apps Deployment Instructions

## 🚀 **Quick Setup**

### **Step 1: Add GitHub Secrets**

1. Go to: https://github.com/georgasa/tbsg-ai-rfp-assistant/settings/secrets/actions
2. Click **"New repository secret"**
3. Add these two secrets:

#### **Secret 1: AZURE_CREDENTIALS**
- **Name**: `AZURE_CREDENTIALS`
- **Value**: Contact the development team for the Azure credentials JSON

#### **Secret 2: TEMENOS_JWT_TOKEN**
- **Name**: `TEMENOS_JWT_TOKEN`
- **Value**: Contact the development team for the Temenos JWT token

### **Step 2: Deploy**

1. **Push any change** to the `main` branch
2. **GitHub Actions** will automatically:
   - Build Docker image
   - Push to GitHub Container Registry
   - Deploy to Azure Container Apps

### **Step 3: Access Your Application**

After successful deployment, your application will be available at:
```
https://tbsg-ai-rfp-assistant.tolis-aca-env.azurecontainerapps.io
```

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

## 📞 **Support**

For credentials or technical support, contact the development team.



