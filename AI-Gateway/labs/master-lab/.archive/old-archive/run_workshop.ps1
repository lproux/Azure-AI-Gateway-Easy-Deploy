Write-Host "🚀 AI Gateway Workshop - One-Click Deploy" -ForegroundColor Green

if ($env:CODESPACE_NAME) {
    Write-Host "📍 Running in GitHub Codespace" -ForegroundColor Cyan
} else {
    Write-Host "📍 Running in local environment" -ForegroundColor Cyan
}

if (-not (Test-Path "bootstrap.env")) {
    Copy-Item "bootstrap.env.template" "bootstrap.env"
    Write-Host "⚠️  Created bootstrap.env - please fill in required values" -ForegroundColor Yellow
    exit 1
}

Write-Host "📦 Installing dependencies..." -ForegroundColor Green
pip install -q -r requirements.txt

Write-Host "🔧 Running deployment notebook..." -ForegroundColor Green
jupyter nbconvert --to notebook --execute master-ai-gateway-fix-MCP-clean.ipynb `
    --output output/deployed.ipynb `
    --ExecutePreprocessor.timeout=1800

Write-Host "✅ Deployment complete!" -ForegroundColor Green
