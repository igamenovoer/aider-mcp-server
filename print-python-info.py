#!/usr/bin/env python3
"""
Prints information about the current Python interpreter and runtime environment.
"""

import os
import sys
import platform


def print_python_info() -> None:
    # Basic Python interpreter details
    impl = platform.python_implementation()
    version = platform.python_version()
    version_full = sys.version.splitlines()[0]
    build_no, build_date = platform.python_build()
    compiler = platform.python_compiler()

    # Executable and environment
    executable = sys.executable or "<unknown>"
    prefix = getattr(sys, "prefix", "")
    base_prefix = getattr(sys, "base_prefix", "")
    in_venv = bool(prefix and base_prefix and prefix != base_prefix)
    venv_env = os.environ.get("VIRTUAL_ENV")

    # Platform and system details
    plat = platform.platform()
    system = platform.system()
    release = platform.release()
    machine = platform.machine()
    processor = platform.processor() or "<unknown>"
    arch_bits, arch_linkage = platform.architecture()
    byteorder = sys.byteorder

    # Encodings
    fs_encoding = sys.getfilesystemencoding() or "<unknown>"
    default_encoding = sys.getdefaultencoding() or "<unknown>"

    # Output
    print("Python Interpreter Information")
    print("------------------------------")
    print(f"Implementation:        {impl}")
    print(f"Version:               {version}")
    print(f"Full version string:   {version_full}")
    print(f"Build:                 {build_no} ({build_date})")
    print(f"Compiler:              {compiler}")
    print()
    print("Executable and Environment")
    print("--------------------------")
    print(f"Executable:            {executable}")
    print(f"Prefix:                {prefix}")
    print(f"Base prefix:           {base_prefix}")
    print(f"In virtual environment:{in_venv}")
    if venv_env:
        print(f"VIRTUAL_ENV:           {venv_env}")
    print()
    print("Platform")
    print("--------")
    print(f"Platform:              {plat}")
    print(f"System:                {system}")
    print(f"Release:               {release}")
    print(f"Machine:               {machine}")
    print(f"Processor:             {processor}")
    print(f"Architecture:          {arch_bits}, linkage={arch_linkage}")
    print(f"Byte order:            {byteorder}")
    print()
    print("Encodings")
    print("---------")
    print(f"Filesystem encoding:   {fs_encoding}")
    print(f"Default encoding:      {default_encoding}")


if __name__ == "__main__":
    try:
        print_python_info()
    except Exception as exc:
        # Ensure any unexpected error is clearly visible
        print(f"Error while gathering Python interpreter information: {exc}", file=sys.stderr)
        sys.exit(1)
