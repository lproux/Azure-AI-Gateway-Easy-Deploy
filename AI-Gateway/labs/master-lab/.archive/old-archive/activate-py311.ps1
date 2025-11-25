# Activate Python 3.11 Virtual Environment
# Usage: .\activate-py311.ps1

Write-Host "Activating Python 3.11 environment..." -ForegroundColor Green
.\.venv-py311\Scripts\Activate.ps1
Write-Host "✓ Python 3.11 environment activated!" -ForegroundColor Green
Write-Host ""
python --version
Write-Host ""
Write-Host "To verify autogen:" -ForegroundColor Yellow
Write-Host '  python -c "import autogen; print(autogen.__version__)"' -ForegroundColor Cyan
