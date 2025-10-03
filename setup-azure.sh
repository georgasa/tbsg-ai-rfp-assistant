#!/bin/bash

# Azure Container Apps Setup Script
# This script sets up the necessary Azure resources and GitHub secrets

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Setting up Azure Container Apps for TBSG AI RFP Assistant${NC}"

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo -e "${RED}❌ Azure CLI is not installed. Please install it first.${NC}"
    echo "Visit: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
fi

# Check if user is logged in
if ! az account show &> /dev/null; then
    echo -e "${YELLOW}⚠️  Please login to Azure CLI first:${NC}"
    echo "az login"
    exit 1
fi

# Set variables
SUBSCRIPTION_ID="58a91cf0-0f39-45fd-a63e-5a9a28c7072b"
RESOURCE_GROUP="tolis-working-rg"
CONTAINER_APP_ENV="tolis-aca-env"
CONTAINER_APP_NAME="tbsg-ai-rfp-assistant"
LOCATION="West Europe"

echo -e "${BLUE}📋 Configuration:${NC}"
echo "Subscription ID: $SUBSCRIPTION_ID"
echo "Resource Group: $RESOURCE_GROUP"
echo "Container App Environment: $CONTAINER_APP_ENV"
echo "Container App Name: $CONTAINER_APP_NAME"
echo "Location: $LOCATION"
echo ""

# Set subscription
echo -e "${YELLOW}🔧 Setting Azure subscription...${NC}"
az account set --subscription $SUBSCRIPTION_ID

# Check if resource group exists
if ! az group show --name $RESOURCE_GROUP &> /dev/null; then
    echo -e "${YELLOW}📦 Creating resource group...${NC}"
    az group create --name $RESOURCE_GROUP --location "$LOCATION"
else
    echo -e "${GREEN}✅ Resource group already exists${NC}"
fi

# Check if container app environment exists
if ! az containerapp env show --name $CONTAINER_APP_ENV --resource-group $RESOURCE_GROUP &> /dev/null; then
    echo -e "${YELLOW}🏗️  Creating Container App Environment...${NC}"
    az containerapp env create \
        --name $CONTAINER_APP_ENV \
        --resource-group $RESOURCE_GROUP \
        --location "$LOCATION"
else
    echo -e "${GREEN}✅ Container App Environment already exists${NC}"
fi

# Create service principal for GitHub Actions
echo -e "${YELLOW}🔐 Creating service principal for GitHub Actions...${NC}"
SP_NAME="github-actions-tbsg-ai"
SP_OUTPUT=$(az ad sp create-for-rbac --name $SP_NAME --role contributor --scopes /subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP --sdk-auth)

echo -e "${GREEN}✅ Service principal created successfully!${NC}"
echo ""
echo -e "${BLUE}📋 Next steps:${NC}"
echo "1. Copy the JSON output below and add it as a GitHub secret named 'AZURE_CREDENTIALS'"
echo "2. Add your Temenos JWT token as a GitHub secret named 'TEMENOS_JWT_TOKEN'"
echo "3. Push your code to trigger the deployment"
echo ""
echo -e "${YELLOW}🔑 Service Principal JSON (add as AZURE_CREDENTIALS secret):${NC}"
echo "$SP_OUTPUT"
echo ""
echo -e "${BLUE}🌐 After deployment, your app will be available at:${NC}"
echo "https://$CONTAINER_APP_NAME.$CONTAINER_APP_ENV.azurecontainerapps.io"
echo ""
echo -e "${GREEN}🎉 Setup complete! Ready for deployment.${NC}"


