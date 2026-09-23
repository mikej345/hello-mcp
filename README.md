# hello-mcp

A deliberately tiny, risk-free MCP server for learning how MCP directory listings work.

Repository: https://github.com/mikej345/hello-mcp

- **No network calls, no API keys, no user data.** Every tool is read-only and pure.
- **Runs over both MCP transports**: `stdio` (for "runs from source" listings) and Streamable HTTP (for "hosted endpoint" listings).

## Tools

| Tool | Input | Returns |
| --- | --- | --- |
| `get_rule_of_thumb` | none | A random engineering rule of thumb |
| `add_numbers` | `a`, `b` (numbers) | Their sum |
| `get_server_time` | none | Current UTC time (a liveness check) |

## Run it locally

```bash
pip install -r requirements.txt

# stdio (an AI app launches it as a local program)
python server.py

# Streamable HTTP (serves http://localhost:8000/mcp)
MCP_TRANSPORT=streamable-http python server.py
```

Inspect it with the official MCP Inspector (needs Node.js):

```bash
npx @modelcontextprotocol/inspector python server.py
```

## Configuration

| Env var | Default | Purpose |
| --- | --- | --- |
| `MCP_TRANSPORT` | `stdio` | `stdio` or `streamable-http` |
| `HOST` | `0.0.0.0` | Bind address for HTTP |
| `PORT` | `8000` | Port for HTTP (most hosts set this for you) |

## License

MIT
