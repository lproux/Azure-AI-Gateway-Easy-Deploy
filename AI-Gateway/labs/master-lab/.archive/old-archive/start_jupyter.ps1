Write-Host "🚀 Starting Jupyter Notebook (no authentication)" -ForegroundColor Green

# Activate virtual environment
& .\.venv-py311\Scripts\Activate.ps1

# Start Jupyter without token authentication
jupyter notebook --no-browser --NotebookApp.token='' --NotebookApp.password='' --NotebookApp.disable_check_xsrf=True
