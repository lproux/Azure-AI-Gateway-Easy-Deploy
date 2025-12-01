FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy server code
COPY mcp_server.py .

# Environment variables
ENV PORT="8000"

# Expose port (Excel MCP uses 8000 to match original)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/excel/mcp/ || exit 1

# Run the MCP server
CMD ["python", "mcp_server.py", "--host", "0.0.0.0", "--port", "8000"]
