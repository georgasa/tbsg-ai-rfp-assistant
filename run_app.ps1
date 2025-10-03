# Temenos RAG AI System Startup Script
Write-Host "🚀 Starting Temenos RAG AI System..." -ForegroundColor Green

# Set environment variables
$env:TEMENOS_JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYXBvc3RvbG9zLmdlb3JnYXMiLCJlbWFpbCI6ImFwb3N0b2xvcy5nZW9yZ2FzQHRlbWVub3MuY29tIiwiZXhwIjoxNzYyMDcxNjIzLCJpYXQiOjE3NTk0Nzk2MjMsImlzcyI6InRic2cudGVtZW5vcy5jb20iLCJhdWQiOiJ0ZW1lbm9zLWFwaSJ9.8VuKANbWATjEg24yJU7sxrtilmeJNJEfZ-wUIZ1Y8q0"
$env:FLASK_ENV = "development"

Write-Host "✅ Environment variables set" -ForegroundColor Yellow
Write-Host "🌐 Starting web application..." -ForegroundColor Cyan
Write-Host "📱 Access the application at: http://localhost:5000" -ForegroundColor Magenta
Write-Host ""

# Start the application
python app.py
