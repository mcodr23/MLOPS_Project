# 🧊 MLOps Project - Full Demonstration Launcher
Write-Host "--- MLOps End-to-End Demonstration ---" -ForegroundColor Cyan
Write-Host "This script will launch all 4 Pillars: Training, Serving, Drift, and Monitoring." -ForegroundColor Gray

# 1. AWS Credentials (REQUIRED for S3 and Drift Monitoring)
Write-Host "`n[Action Required] Please enter your AWS credentials for the Sydney region (ap-southeast-2):" -ForegroundColor Yellow
if (-not $env:AWS_ACCESS_KEY_ID) {
    $env:AWS_ACCESS_KEY_ID = Read-Host "Enter AWS Access Key ID"
    $env:AWS_SECRET_ACCESS_KEY = Read-Host "Enter AWS Secret Access Key"
}
$env:AWS_DEFAULT_REGION = "ap-southeast-2"
$env:PYTHONPATH = (Get-Item .).FullName

# 2. Cleanup (Kill existing processes to avoid port conflicts)
Write-Host "`n--- Step 1: Cleaning up existing services ---" -ForegroundColor Green
$ports = @(8005, 9090, 3000, 8501)
foreach ($p in $ports) {
    Get-NetTCPConnection -LocalPort $p -State Listen -ErrorAction SilentlyContinue | ForEach-Object { 
        Stop-Process -Id $_.OwningProcess -Force 
        Write-Host "Stopped process on port $p" -ForegroundColor Gray
    }
}

# 3. Launch Pillar 4: Infrastructure Monitoring (Prometheus & Grafana)
Write-Host "`n--- Step 2: Launching Infrastructure Monitoring ---" -ForegroundColor Green
$promDir = "monitoring\prometheus-2.53.4.windows-amd64"
$grafDir = "monitoring\grafana-v11.6.0\bin"

Start-Process -FilePath "$promDir\prometheus.exe" -ArgumentList "--config.file=monitoring\prometheus.yml" -NoNewWindow
Start-Process -FilePath "$grafDir\grafana-server.exe" -WorkingDirectory "$grafDir" -NoNewWindow
Write-Host "✅ Prometheus (9090) and Grafana (3000) are starting..." -ForegroundColor Gray

# 4. Launch Pillar 2: Model Serving (FastAPI)
Write-Host "`n--- Step 3: Launching Model Serving API ---" -ForegroundColor Green
Start-Process -FilePath ".\venv\Scripts\python.exe" -ArgumentList "main.py" -NoNewWindow
Write-Host "Waiting for API to initialize..." -ForegroundColor Gray
Start-Sleep -Seconds 12
Write-Host "✅ FastAPI Serving (8005) is active." -ForegroundColor Gray

# 5. Launch Pillar 3: Data Drift Initial Seeding
Write-Host "`n--- Step 4: Seeding S3 Monitoring Data ---" -ForegroundColor Green
.\venv\Scripts\python.exe seed_s3_monitoring.py
Write-Host "✅ S3 Baseline and Daily Prediction data seeded." -ForegroundColor Gray

# 6. Launch Pillar 3 UI: Drift Dashboard (Streamlit)
Write-Host "`n--- Step 5: Launching Drift Monitoring Dashboard ---" -ForegroundColor Green
Start-Process -FilePath ".\venv\Scripts\streamlit.exe" -ArgumentList "run", "drift_monitoring/app_v1.py" -NoNewWindow
Write-Host "✅ Data Drift Dashboard (8501) is starting..." -ForegroundColor Gray

Write-Host "`n--- PROJECT READY FOR DEMONSTRATION ---" -ForegroundColor Cyan
Write-Host "1. Model Training: Logs are in /mlruns"
Write-Host "2. Serving: http://localhost:8005/docs"
Write-Host "3. Drift Monitoring: http://localhost:8501"
Write-Host "4. Sys Monitoring: http://localhost:3000"
Write-Host "`nKeep this window open to monitor logs. Press Ctrl+C to stop all (manual)." -ForegroundColor Gray
