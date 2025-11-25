#!/usr/bin/env python3
"""
MCP HTTP/SSE Bridge
Wraps stdio-based MCP servers with HTTP/SSE transport
"""
import asyncio
import json
import os
import sys
from typing import Optional
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from starlette.background import BackgroundTask
import uvicorn

app = FastAPI(title="MCP HTTP Bridge")

# Global subprocess reference
mcp_process: Optional[asyncio.subprocess.Process] = None
request_queue = asyncio.Queue()
response_queues = {}


async def start_mcp_server():
    """Start the stdio MCP server as a subprocess"""
    global mcp_process

    # Get command from environment
    command = os.getenv("MCP_COMMAND", "npx")
    args = os.getenv("MCP_ARGS", "").split()

    print(f"Starting MCP server: {command} {' '.join(args)}", file=sys.stderr)

    mcp_process = await asyncio.create_subprocess_exec(
        command,
        *args,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=os.environ
    )

    # Start reading responses
    asyncio.create_task(read_responses())
    asyncio.create_task(read_stderr())


async def read_responses():
    """Read JSON-RPC responses from MCP server stdout"""
    global mcp_process

    while mcp_process and mcp_process.stdout:
        try:
            line = await mcp_process.stdout.readline()
            if not line:
                break

            try:
                response = json.loads(line.decode().strip())
                response_id = response.get("id")

                if response_id and response_id in response_queues:
                    await response_queues[response_id].put(response)
                else:
                    # Notification or unsolicited message
                    print(f"MCP notification: {response}", file=sys.stderr)
            except json.JSONDecodeError:
                print(f"Invalid JSON from MCP server: {line}", file=sys.stderr)
        except Exception as e:
            print(f"Error reading MCP responses: {e}", file=sys.stderr)
            break


async def read_stderr():
    """Read stderr from MCP server for logging"""
    global mcp_process

    while mcp_process and mcp_process.stderr:
        try:
            line = await mcp_process.stderr.readline()
            if not line:
                break
            print(f"MCP stderr: {line.decode().strip()}", file=sys.stderr)
        except Exception as e:
            print(f"Error reading MCP stderr: {e}", file=sys.stderr)
            break


async def send_request(request_data: dict) -> dict:
    """Send JSON-RPC request to MCP server and wait for response"""
    global mcp_process

    if not mcp_process or not mcp_process.stdin:
        raise RuntimeError("MCP server not running")

    request_id = request_data.get("id")
    if request_id:
        response_queues[request_id] = asyncio.Queue()

    try:
        # Send request to MCP server
        request_json = json.dumps(request_data) + "\n"
        mcp_process.stdin.write(request_json.encode())
        await mcp_process.stdin.drain()

        if request_id:
            # Wait for response
            response = await asyncio.wait_for(
                response_queues[request_id].get(),
                timeout=30.0
            )
            return response
        else:
            # No response expected for notifications
            return {"jsonrpc": "2.0", "result": None}
    finally:
        if request_id and request_id in response_queues:
            del response_queues[request_id]


@app.on_event("startup")
async def startup_event():
    """Start MCP server on application startup"""
    await start_mcp_server()


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup MCP server on shutdown"""
    global mcp_process
    if mcp_process:
        mcp_process.terminate()
        await mcp_process.wait()


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "mcp-http-bridge",
        "mcp_running": mcp_process is not None and mcp_process.returncode is None
    }


@app.post("/messages")
async def messages(request: Request):
    """Handle MCP JSON-RPC messages"""
    try:
        request_data = await request.json()
        response = await send_request(request_data)
        return response
    except Exception as e:
        return {
            "jsonrpc": "2.0",
            "id": request_data.get("id") if request_data else None,
            "error": {
                "code": -32603,
                "message": f"Internal error: {str(e)}"
            }
        }


@app.get("/sse")
async def sse_endpoint(request: Request):
    """Server-Sent Events endpoint for MCP protocol"""

    async def event_generator():
        # Send initial connection event
        yield f"data: {json.dumps({'type': 'connected'})}\n\n"

        # Keep connection alive
        try:
            while True:
                await asyncio.sleep(15)
                yield f": keepalive\n\n"
        except asyncio.CancelledError:
            pass

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Mcp-Session-Id": "mcp-session-1"
        }
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port)
