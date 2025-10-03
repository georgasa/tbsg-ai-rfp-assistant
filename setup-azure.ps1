# Azure Container Apps Setup Script for Windows
# This script sets up the necessary Azure resources and GitHub secrets

param(
    [string]$SubscriptionId = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    [string]$ResourceGroup = "tolis-working-rg",
    [string]$ContainerAppEnv = "tolis-aca-env",
    [string]$ContainerAppName = "tbsg-ai-rfp-assistant",
    [string]$Location = "West Europe"
)

Write-Host "🚀 Setting up Azure Container Apps for TBSG AI RFP Assistant" -ForegroundColor Blue

# Check if Azure CLI is installed
try {
    $azVersion = az version --output json | ConvertFrom-Json
    Write-Host "✅ Azure CLI version: $($azVersion.'azure-cli')" -ForegroundColor Green
} catch {
    Write-Host "❌ Azure CLI is not installed. Please install it first." -ForegroundColor Red
    Write-Host "Visit: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
}

# Check if user is logged in
try {
    $account = az account show --output json | ConvertFrom-Json
    Write-Host "✅ Logged in as: $($account.user.name)" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Please login to Azure CLI first:" -ForegroundColor Yellow
    Write-Host "az login"
    exit 1
}

Write-Host "📋 Configuration:" -ForegroundColor Blue
Write-Host "Subscription ID: $SubscriptionId"
Write-Host "Resource Group: $ResourceGroup"
Write-Host "Container App Environment: $ContainerAppEnv"
Write-Host "Container App Name: $ContainerAppName"
Write-Host "Location: $Location"
Write-Host ""

# Set subscription
Write-Host "🔧 Setting Azure subscription..." -ForegroundColor Yellow
az account set --subscription $SubscriptionId

# Check if resource group exists
try {
    $rg = az group show --name $ResourceGroup --output json | ConvertFrom-Json
    Write-Host "✅ Resource group already exists" -ForegroundColor Green
} catch {
    Write-Host "📦 Creating resource group..." -ForegroundColor Yellow
    az group create --name $ResourceGroup --location $Location
}

# Check if container app environment exists
try {
    $env = az containerapp env show --name $ContainerAppEnv --resource-group $ResourceGroup --output json | ConvertFrom-Json
    Write-Host "✅ Container App Environment already exists" -ForegroundColor Green
} catch {
    Write-Host "🏗️  Creating Container App Environment..." -ForegroundColor Yellow
    az containerapp env create --name $ContainerAppEnv --resource-group $ResourceGroup --location $Location
}

# Create service principal for GitHub Actions
Write-Host "🔐 Creating service principal for GitHub Actions..." -ForegroundColor Yellow
$spName = "github-actions-tbsg-ai"
$spOutput = az ad sp create-for-rbac --name $spName --role contributor --scopes "/subscriptions/$SubscriptionId/resourceGroups/$ResourceGroup" --sdk-auth

Write-Host "✅ Service principal created successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Blue
Write-Host "1. Copy the JSON output below and add it as a GitHub secret named 'AZURE_CREDENTIALS'"
Write-Host "2. Add your Temenos JWT token as a GitHub secret named 'TEMENOS_JWT_TOKEN'"
Write-Host "3. Push your code to trigger the deployment"
Write-Host ""
Write-Host "🔑 Service Principal JSON (add as AZURE_CREDENTIALS secret):" -ForegroundColor Yellow
Write-Host $spOutput
Write-Host ""
Write-Host "🌐 After deployment, your app will be available at:" -ForegroundColor Blue
Write-Host "https://$ContainerAppName.$ContainerAppEnv.azurecontainerapps.io"
Write-Host ""
Write-Host "🎉 Setup complete! Ready for deployment." -ForegroundColor Green


