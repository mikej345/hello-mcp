# Used by directories that build from source (e.g. Glama "Runs from Source")
# and by hosting platforms that deploy containers (e.g. Render, Fly.io).
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY server.py .
# Default: stdio (what source-based directories expect).
# Hosting platforms override with MCP_TRANSPORT=streamable-http.
ENV MCP_TRANSPORT=stdio
CMD ["python", "server.py"]
