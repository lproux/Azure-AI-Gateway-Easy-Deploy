FROM node:20-slim

# Install Python and pip
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Install GitHub MCP server globally
RUN npm install -g @modelcontextprotocol/server-github

# Copy bridge script
COPY mcp_http_bridge.py /app/mcp_http_bridge.py
RUN chmod +x /app/mcp_http_bridge.py

# Create Python virtual environment and install dependencies
RUN python3 -m venv /app/venv
RUN /app/venv/bin/pip install --no-cache-dir \
    fastapi==0.104.1 \
    uvicorn[standard]==0.24.0 \
    starlette==0.27.0

# Set environment variables for GitHub MCP
ENV MCP_COMMAND="npx" \
    MCP_ARGS="-y @modelcontextprotocol/server-github" \
    PORT="8080"

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run the bridge
CMD ["/app/venv/bin/python", "/app/mcp_http_bridge.py"]
