# Data Drift Monitoring Repair Script
Write-Host "--- Data Drift Monitoring Repair Tool ---" -ForegroundColor Cyan

# 1. Collect Credentials
Write-Host "Please enter your AWS Credentials to connect to S3 Monitoring:" -ForegroundColor Yellow
$accessKey = Read-Host "AWS_ACCESS_KEY_ID"
$secretKey = Read-Host "AWS_SECRET_ACCESS_KEY"
$region = Read-Host "AWS_DEFAULT_REGION (press enter for us-east-1)"
if ([string]::IsNullOrWhiteSpace($region)) { $region = "us-east-1" }

# Set Environment Variables for this session
$env:AWS_ACCESS_KEY_ID = $accessKey.Trim()
$env:AWS_SECRET_ACCESS_KEY = $secretKey.Trim()
$env:AWS_DEFAULT_REGION = $region.Trim()
$env:PYTHONPATH = (Get-Item .).FullName

Write-Host "`n--- Step 1: Seeding S3 Baseline ---" -ForegroundColor Green
.\venv\Scripts\python.exe repair_drift_setup.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to seed baseline to S3. Please check your credentials and try again." -ForegroundColor Red
    exit
}

Write-Host "`n--- Step 2: Ensuring FastAPI is running ---" -ForegroundColor Green
$apiCheck = Get-NetTCPConnection -LocalPort 8005 -State Listen -ErrorAction SilentlyContinue
if (-not $apiCheck) {
    Write-Host "FastAPI is not running. Starting it now..." -ForegroundColor Yellow
    Start-Process -FilePath ".\venv\Scripts\python.exe" -ArgumentList "main.py" -NoNewWindow
    Start-Sleep -Seconds 10
}

Write-Host "`n--- Step 3: Generating Today's Monitoring Data ---" -ForegroundColor Green
# Trigger a batch prediction
curl.exe -X POST "http://localhost:8005/batch_prediction" `
     -H "accept: application/json" `
     -H "Content-Type: multipart/form-data" `
     -F "file=@prediction_model/datasets/test.csv"
Write-Host "`nData push complete." -ForegroundColor Green

Write-Host "`n--- Step 4: Starting Drift Monitoring Dashboard ---" -ForegroundColor Green
Write-Host "The dashboard will open at http://localhost:8501" -ForegroundColor Cyan
streamlit run drift_monitoring/app_v1.py --server.port 8501
