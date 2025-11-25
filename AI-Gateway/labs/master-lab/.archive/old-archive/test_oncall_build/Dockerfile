FROM python:3.13.2-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 8080

# Run the Python script directly (mcp.run() will start the server)
CMD ["python", "mcp_server.py"]
