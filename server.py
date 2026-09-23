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
from typing import Annotated

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

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


# All three tools are read-only, have no side effects, and never leave this server.
SAFE_READ_ONLY = dict(readOnlyHint=True, destructiveHint=False, openWorldHint=False)


@mcp.tool(annotations=ToolAnnotations(title="Get a rule of thumb", idempotentHint=False, **SAFE_READ_ONLY))
def get_rule_of_thumb() -> str:
    """Return one random engineering rule of thumb. Takes no input and has no side effects."""
    return random.choice(RULES_OF_THUMB)


@mcp.tool(annotations=ToolAnnotations(title="Add two numbers", idempotentHint=True, **SAFE_READ_ONLY))
def add_numbers(
    a: Annotated[float, Field(description="The first number to add, e.g. 2 or -3.5.")],
    b: Annotated[float, Field(description="The second number to add, e.g. 3 or 10.25.")],
) -> float:
    """Add two numbers and return the sum."""
    return a + b


@mcp.tool(annotations=ToolAnnotations(title="Get server time", idempotentHint=False, **SAFE_READ_ONLY))
def get_server_time() -> str:
    """Return the server's current time in UTC (ISO 8601). Useful for checking the server is alive."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


if __name__ == "__main__":
    transport = os.environ.get("MCP_TRANSPORT", "stdio")
    mcp.run(transport=transport)