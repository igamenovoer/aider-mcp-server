#!/usr/bin/env python3
"""
Prints information about the current Python interpreter and runtime environment.

Now uses the standard logging module for output.
"""

import os
import sys
import platform
import logging


def _get_log_level_from_env() -> int:
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    return getattr(logging, level, logging.INFO)


def configure_logging() -> logging.Logger:
    """
    Configure a logger that writes to stdout with a simple message-only format.
    Respects LOG_LEVEL environment variable (defaults to INFO).
    """
    logger = logging.getLogger("print_python_info")

    # Avoid adding multiple handlers if configured more than once.
    if logger.handlers:
        return logger

    logger.setLevel(_get_log_level_from_env())

    handler = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger


def print_python_info() -> None:
    logger = logging.getLogger("print_python_info")

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
    logger.info("Python Interpreter Information")
    logger.info("------------------------------")
    logger.info(f"Implementation:        {impl}")
    logger.info(f"Version:               {version}")
    logger.info(f"Full version string:   {version_full}")
    logger.info(f"Build:                 {build_no} ({build_date})")
    logger.info(f"Compiler:              {compiler}")
    logger.info("")
    logger.info("Executable and Environment")
    logger.info("--------------------------")
    logger.info(f"Executable:            {executable}")
    logger.info(f"Prefix:                {prefix}")
    logger.info(f"Base prefix:           {base_prefix}")
    logger.info(f"In virtual environment:{in_venv}")
    if venv_env:
        logger.info(f"VIRTUAL_ENV:           {venv_env}")
    logger.info("")
    logger.info("Platform")
    logger.info("--------")
    logger.info(f"Platform:              {plat}")
    logger.info(f"System:                {system}")
    logger.info(f"Release:               {release}")
    logger.info(f"Machine:               {machine}")
    logger.info(f"Processor:             {processor}")
    logger.info(f"Architecture:          {arch_bits}, linkage={arch_linkage}")
    logger.info(f"Byte order:            {byteorder}")
    logger.info("")
    logger.info("Encodings")
    logger.info("---------")
    logger.info(f"Filesystem encoding:   {fs_encoding}")
    logger.info(f"Default encoding:      {default_encoding}")


if __name__ == "__main__":
    logger = configure_logging()
    try:
        print_python_info()
    except Exception:
        # Ensure any unexpected error is clearly visible with traceback
        logger.exception("Error while gathering Python interpreter information")
        sys.exit(1)
