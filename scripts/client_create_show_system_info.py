#!/usr/bin/env python
import asyncio
import os
import sys
import subprocess
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client


SCRIPT_NAME = "show-system-info.py"


async def main():
    # Launch the MCP server directly via the console script in this Pixi env
    # This avoids relying on 'pixi' being on PATH inside the spawned shell.
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

            # Optional: list tools for visibility
            tools = await session.list_tools()
            print("TOOLS:")
            for t in tools.tools:
                print("-", t.name)

            # Create the system info script via aider_ai_code (write exact content)
            prompt = (
                "Create or replace the file 'show-system-info.py' with EXACTLY the following content. "
                "Do not include any explanations, diffs, or additional text. Write the file contents verbatim:\n\n"
                "```python\n"
                "#!/usr/bin/env python\n"
                "import sys\n"
                "import os\n"
                "import platform\n"
                "from pprint import pprint\n"
                "\n"
                "def main():\n"
                "    print(\"=== Python Interpreter Information ===\")\n"
                "    print(f\"Python Version: {platform.python_version()} ({sys.version})\")\n"
                "    print(f\"Python Executable: {sys.executable}\")\n"
                "    print(f\"Platform: {platform.platform()}\")\n"
                "    print(f\"System: {platform.system()} {platform.release()}\")\n"
                "    print(f\"Machine: {platform.machine()}\")\n"
                "    print(f\"Processor: {platform.processor()}\")\n"
                "    try:\n"
                "        bits, linkage = platform.architecture()\n"
                "        print(f\"Architecture: {bits}, Linkage: {linkage}\")\n"
                "    except Exception:\n"
                "        pass\n"
                "    print(f\"Current Working Directory: {os.getcwd()}\")\n"
                "\n"
                "    print(\"\\n=== Python Path (sys.path) ===\")\n"
                "    pprint(sys.path)\n"
                "\n"
                "    print(\"\\n=== Python-related Environment Variables (subset) ===\")\n"
                "    env_subset = {k: v for k, v in os.environ.items() if 'PYTHON' in k.upper() or k in ('VIRTUAL_ENV','CONDA_PREFIX')}\n"
                "    if env_subset:\n"
                "        pprint(env_subset)\n"
                "    else:\n"
                "        print(\"(none)\")\n"
                "\n"
                "if __name__ == \"__main__\":\n"
                "    main()\n"
                "```\n"
            )

            edit_args = {
                "ai_coding_prompt": prompt,
                "relative_editable_files": [SCRIPT_NAME],
                "relative_readonly_files": [],
                # Explicitly pass the model; your server will also default this from .project-secrets.json
                "model": "gpt-4o",
            }

            print(f"Requesting aider to create {SCRIPT_NAME} ...")
            try:
                # Give the LLM enough time
                ac = await asyncio.wait_for(session.call_tool("aider_ai_code", edit_args), timeout=300)
            except asyncio.TimeoutError:
                print("aider_ai_code timed out after 300s", file=sys.stderr)
                return

            print("aider_ai_code response:")
            for item in ac:
                if isinstance(item, types.TextContent):
                    print(item.text)

    # After MCP session closes, run the generated script to show the output
    if os.path.exists(SCRIPT_NAME):
        print(f"\nRunning {SCRIPT_NAME}...\n")
        proc = subprocess.run([sys.executable, SCRIPT_NAME], capture_output=True, text=True)
        print(proc.stdout)
        if proc.returncode != 0:
            print(proc.stderr, file=sys.stderr)
            sys.exit(proc.returncode)
    else:
        print(f"{SCRIPT_NAME} was not created.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())