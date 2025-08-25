#!/usr/bin/env python
import asyncio
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client


async def main():
    server_params = StdioServerParameters(
        command="aider-mcp-server",
        args=[
            "--current-working-dir", "d:\\code\\aider-mcp-server",
            "--project-secrets", ".project-secrets.json",
        ],
        env=None,
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            init = await session.initialize()
            print("Initialized:", init)

            tools = await session.list_tools()
            print("TOOLS:")
            for t in tools.tools:
                print("-", t.name)

            # Call list_models tool
            lm = await session.call_tool("list_models", {"substring": "gpt"})
            print("list_models response:")
            for item in lm:
                if isinstance(item, types.TextContent):
                    print(item.text)

            # aider_ai_code meaningful edit to satisfy change detector
            edit_args = {
                "ai_coding_prompt": (
                    "Create or update greeting.py to have:\n"
                    "def greet(name: str) -> str:\n"
                    "    return f\"Hello, {name}!\"\n"
                    "\n"
                    "Also add:\n"
                    "if __name__ == \"__main__\":\n"
                    "    print(greet(\"MCP\"))\n"
                ),
                "relative_editable_files": ["greeting.py"],
                "relative_readonly_files": [],
                "model": "gpt-4o"
            }
            # Wrap with timeout to avoid hanging if the remote LLM is slow/unreachable
            try:
                ac = await asyncio.wait_for(
                    session.call_tool("aider_ai_code", edit_args),
                    timeout=240
                )
                print("aider_ai_code response:")
                for item in ac:
                    if isinstance(item, types.TextContent):
                        print(item.text)
            except asyncio.TimeoutError:
                print("aider_ai_code timed out after 240s")

            # Context manager handles shutdown; explicit shutdown() not needed


if __name__ == "__main__":
    asyncio.run(main())