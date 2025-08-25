import argparse
import asyncio
import os
import json
from aider_mcp_server.server import serve
from aider_mcp_server.atoms.utils import DEFAULT_EDITOR_MODEL


def load_project_secrets(path: str) -> str | None:
    """
    Load project-level secrets and set environment variables for OpenAI-compatible backends.

    Returns a suggested editor model override exactly as provided (e.g., "gpt-5" or "openai/gpt-5") if present,
    otherwise returns None.

    Expected JSON shape (example):
    {
        "llm": {
            "type": "OpenAI-Compatible",
            "base_url": "https://api.example.com/v1",
            "model_name": "gpt-5",
            "api_key": "sk-...redacted...",
            "reasoning_effort": "medium",
            "verbosity": "medium"
        }
    }
    """
    if not path:
        return None

    try:
        if not os.path.isfile(path):
            return None

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        llm = data.get("llm", {}) or {}
        llm_type = (llm.get("type") or "").lower()
        base_url = llm.get("base_url")
        api_key = llm.get("api_key")
        model_name = llm.get("model_name")

        # Map secrets to env for OpenAI-compatible stacks
        if "openai" in llm_type or "compatible" in llm_type:
            if api_key and not os.environ.get("OPENAI_API_KEY"):
                os.environ["OPENAI_API_KEY"] = api_key
            if base_url:
                # Support both common env var names
                os.environ.setdefault("OPENAI_BASE_URL", base_url)
                os.environ.setdefault("OPENAI_API_BASE", base_url)

        # Suggest a default editor model if provided in secrets
        if model_name:
            # Use the model name exactly as provided, without adding a provider prefix
            return model_name

    except Exception:
        # Intentionally silent to avoid blocking startup on secrets parsing errors
        pass

    return None


def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Aider MCP Server - Offload AI coding tasks to Aider")

    # Add arguments
    parser.add_argument(
        "--editor-model",
        type=str,
        default=DEFAULT_EDITOR_MODEL,
        help=f"Editor model to use (default: {DEFAULT_EDITOR_MODEL})",
    )
    parser.add_argument(
        "--current-working-dir",
        type=str,
        required=True,
        help="Current working directory (must be a valid git repository)",
    )
    parser.add_argument(
        "--project-secrets",
        type=str,
        default=".project-secrets.json",
        help="Path to project secrets JSON (default: .project-secrets.json). "
             "If present, will set OPENAI_* env vars and may suggest a default model.",
    )

    args = parser.parse_args()

    # Load secrets (if present) and compute the editor model to use
    suggested_model = load_project_secrets(args.project_secrets)
    editor_model_to_use = args.editor_model
    if suggested_model and (args.editor_model == DEFAULT_EDITOR_MODEL or not args.editor_model):
        editor_model_to_use = suggested_model

    # Run the server asynchronously
    asyncio.run(
        serve(
            editor_model=editor_model_to_use,
            current_working_dir=args.current_working_dir,
        )
    )


if __name__ == "__main__":
    main()