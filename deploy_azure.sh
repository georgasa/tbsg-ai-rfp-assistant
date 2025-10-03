#!/bin/bash

# Azure Deployment Script for Temenos RAG AI System
# This script deploys the application to Azure Web App

set -e

# Configuration
RESOURCE_GROUP="temenos-rag-ai-rg"
APP_SERVICE_PLAN="temenos-rag-ai-plan"
WEB_APP_NAME="temenos-rag-ai-app"
LOCATION="westeurope"
RUNTIME="PYTHON|3.9"

echo "🚀 Starting Azure deployment for Temenos RAG AI System..."

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI is not installed. Please install it first."
    exit 1
fi

# Check if user is logged in
if ! az account show &> /dev/null; then
    echo "❌ Please login to Azure CLI first: az login"
    exit 1
fi

echo "✅ Azure CLI is ready"

# Create resource group
echo "📦 Creating resource group..."
az group create \
    --name $RESOURCE_GROUP \
    --location $LOCATION \
    --output table

# Create App Service Plan
echo "📋 Creating App Service Plan..."
az appservice plan create \
    --name $APP_SERVICE_PLAN \
    --resource-group $RESOURCE_GROUP \
    --location $LOCATION \
    --sku B1 \
    --is-linux \
    --output table

# Create Web App
echo "🌐 Creating Web App..."
az webapp create \
    --name $WEB_APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --plan $APP_SERVICE_PLAN \
    --runtime $RUNTIME \
    --output table

# Configure app settings
echo "⚙️ Configuring app settings..."
az webapp config appsettings set \
    --resource-group $RESOURCE_GROUP \
    --name $WEB_APP_NAME \
    --settings \
        TEMENOS_JWT_TOKEN="your_jwt_token_here" \
        FLASK_ENV="production" \
        WEBSITES_ENABLE_APP_SERVICE_STORAGE="true" \
    --output table

# Configure startup command
echo "🚀 Configuring startup command..."
az webapp config set \
    --resource-group $RESOURCE_GROUP \
    --name $WEB_APP_NAME \
    --startup-file "gunicorn --bind=0.0.0.0 --timeout 600 app:app" \
    --output table

# Enable CORS
echo "🔗 Enabling CORS..."
az webapp cors add \
    --resource-group $RESOURCE_GROUP \
    --name $WEB_APP_NAME \
    --allowed-origins "*" \
    --output table

# Deploy from local directory
echo "📤 Deploying application..."
az webapp deployment source config-zip \
    --resource-group $RESOURCE_GROUP \
    --name $WEB_APP_NAME \
    --src deployment.zip \
    --output table

# Get the web app URL
WEB_APP_URL=$(az webapp show \
    --resource-group $RESOURCE_GROUP \
    --name $WEB_APP_NAME \
    --query defaultHostName \
    --output tsv)

echo ""
echo "🎉 Deployment completed successfully!"
echo ""
echo "📋 Deployment Summary:"
echo "  Resource Group: $RESOURCE_GROUP"
echo "  Web App Name: $WEB_APP_NAME"
echo "  URL: https://$WEB_APP_URL"
echo ""
echo "🔧 Next Steps:"
echo "  1. Update TEMENOS_JWT_TOKEN in app settings with your actual token"
echo "  2. Test the application at https://$WEB_APP_URL"
echo "  3. Check the health endpoint: https://$WEB_APP_URL/api/health"
echo ""
echo "📚 Useful Commands:"
echo "  View logs: az webapp log tail --resource-group $RESOURCE_GROUP --name $WEB_APP_NAME"
echo "  Restart app: az webapp restart --resource-group $RESOURCE_GROUP --name $WEB_APP_NAME"
echo "  Delete resources: az group delete --name $RESOURCE_GROUP --yes"
echo ""
