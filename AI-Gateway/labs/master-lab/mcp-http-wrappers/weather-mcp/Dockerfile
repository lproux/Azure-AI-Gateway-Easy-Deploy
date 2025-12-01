FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Install Python dependencies
RUN pip install --no-cache-dir \
    fastapi==0.104.1 \
    uvicorn[standard]==0.24.0 \
    starlette==0.27.0 \
    httpx==0.25.2

# Copy the simple weather HTTP server
COPY weather_server.py /app/weather_server.py

# Environment variables (API key should be provided at runtime)
ENV PORT="8080"

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run the weather HTTP server directly (no MCP bridge needed for simple REST API)
CMD ["python", "/app/weather_server.py"]
