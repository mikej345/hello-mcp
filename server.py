"""
hello-mcp: a deliberately tiny, risk-free MCP server for testing directory listings.

- No network calls, no API keys, no user data. Every tool is pure and read-only.
- Runs over either transport:
    stdio            (default)  -> for "runs from source" / repo-based listings
    streamable-http             -> for "hosted endpoint" / remote listings, served at /mcp

Run locally:
    python server.py                                  # stdio
    MCP_TRANSPORT=streamable-http python server.py    # http://localhost:8000/mcp
"""

import os
import random
from datetime import datetime, timezone

from mcp.server.fastmcp import FastMCP

RULES_OF_THUMB = [
    "Measure twice, cut once.",
    "If you do something three times, automate it.",
    "Fix it at the source, not downstream.",
    "Make it work, make it right, make it fast, in that order.",
    "When in doubt, leave it out.",
    "The best time to add logging is before you need it.",
]

mcp = FastMCP(
    name="hello-mcp",
    instructions=(
        "A tiny demo server with three harmless tools. "
        "Nothing here touches the network or any user data."
    ),
    # Bind to all interfaces and honor $PORT so hosting platforms can reach it.
    host=os.environ.get("HOST", "0.0.0.0"),
    port=int(os.environ.get("PORT", "8000")),
    # Stateless + JSON responses keep the hosted version simple and easy to inspect.
    stateless_http=True,
    json_response=True,
)


@mcp.tool()
def get_rule_of_thumb() -> str:
    """Return one random engineering rule of thumb. Takes no input and has no side effects."""
    return random.choice(RULES_OF_THUMB)


@mcp.tool()
def add_numbers(a: float, b: float) -> float:
    """Add two numbers and return the sum.

    Args:
        a: The first number.
        b: The second number.
    """
    return a + b


@mcp.tool()
def get_server_time() -> str:
    """Return the server's current time in UTC (ISO 8601). Useful for checking the server is alive."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


if __name__ == "__main__":
    transport = os.environ.get("MCP_TRANSPORT", "stdio")
    mcp.run(transport=transport)
