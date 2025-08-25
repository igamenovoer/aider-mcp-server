#!/usr/bin/env python3
from pathlib import Path


def list_top_level_tree(root: Path) -> str:
    """
    Return a tree-like string of the entries in the given root directory up to depth=2.
    - The root directory is shown on the first line (with a trailing slash).
    - Its immediate children (directories first, then files; case-insensitive) are listed.
    - For directories, their immediate children are also listed (one more level).
    - Directories are shown with a trailing slash.
    """
    try:
        entries = list(root.iterdir())
    except Exception as e:
        return f"Error reading directory {root}: {e}"

    # Sort: directories first, then files; both alphabetically (case-insensitive)
    entries.sort(key=lambda p: (p.is_file(), p.name.lower()))

    lines = [f"{root.name}/"]
    total = len(entries)

    for idx, entry in enumerate(entries):
        is_last_top = idx == total - 1
        connector = "└── " if is_last_top else "├── "
        name = entry.name + ("/" if entry.is_dir() else "")
        lines.append(f"{connector}{name}")

        # If this is a directory, list its immediate children (second level)
        if entry.is_dir():
            try:
                child_entries = list(entry.iterdir())
            except Exception as e:
                # Indent under the directory with appropriate vertical continuation
                child_prefix = "    " if is_last_top else "│   "
                lines.append(f"{child_prefix}[Error reading directory {entry.name}: {e}]")
                continue

            # Sort children: directories first, then files; case-insensitive
            child_entries.sort(key=lambda p: (p.is_file(), p.name.lower()))
            child_total = len(child_entries)

            # Prefix for all children lines depends on whether the parent is last
            child_prefix = "    " if is_last_top else "│   "

            for cidx, child in enumerate(child_entries):
                child_connector = "└── " if cidx == child_total - 1 else "├── "
                child_name = child.name + ("/" if child.is_dir() else "")
                lines.append(f"{child_prefix}{child_connector}{child_name}")

    return "\n".join(lines)


def main():
    # Use the directory where this script resides as the repository root
    root = Path(__file__).resolve().parent
    print(list_top_level_tree(root))


if __name__ == "__main__":
    main()
