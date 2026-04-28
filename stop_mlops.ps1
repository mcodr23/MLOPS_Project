# 🛑 MLOps Project - Stop All Services
Write-Host "--- Stopping all MLOps Services ---" -ForegroundColor Red

$ports = @(8005, 9090, 3000, 8501)
foreach ($p in $ports) {
    Get-NetTCPConnection -LocalPort $p -State Listen -ErrorAction SilentlyContinue | ForEach-Object { 
        Stop-Process -Id $_.OwningProcess -Force 
        Write-Host "Closed service on port $p" -ForegroundColor Gray
    }
}

Write-Host "`nAll services have been shut down cleanly." -ForegroundColor Green
