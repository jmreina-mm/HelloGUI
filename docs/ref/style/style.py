# ============================================================================
#  Python Development Template v1 (evolved)
#  Copyright (c) 2025 Mercury Marine, a division of Brunswick Corporation
#  All Rights Reserved
#  
#  Purpose : Professional, portfolio-ready starter for scripts/packages
#  License : Proprietary unless otherwise specified in the repository
#  Author  : Justin Reina, Embedded Connectivity Engineer, Mercury Marine
#  Created : 2025-10-27
#  Last Rev: 2025-12-22
# ============================================================================

"""
Python Development Template (v1()

This template gently adapts your disciplined embedded-C style to idiomatic Python
(PEP 8 / GitHub-typical layout) while keeping your signature structure:

Sections
--------
1) Imports & Globals
2) Constants & Types
3) Logging
4) Core Domain (classes/functions)
5) CLI (argparse)
6) Entry Point

Conventions
-----------
- Line width target: 100 chars (soft)
- 4-space indentation, spaces around operators
- Google-style docstrings
- `main()` returns `int` akin to EXIT_SUCCESS/EXIT_FAILURE
- Logging, not prints, for operational output
- `__all__` gate for public API when used as module
"""

from __future__ import annotations

# ============================================================================
# Imports & Globals
# ============================================================================
import argparse
import dataclasses
import enum
import json
import logging
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Iterator, Optional, Sequence

__all__ = [
    "ExitCode",
    "Settings",
    "configure_logging",
    "load_settings",
    "do_work",
    "build_arg_parser",
    "main",
]

# ============================================================================
# Constants & Types
# ============================================================================

class ExitCode(int, enum.Enum):
    """
    ################################################################################################
    @fcn        ExitCode (Enum)
    @brief      Process exit codes.
    @details    Mirrors C-style EXIT_SUCCESS/EXIT_FAILURE semantics while remaining Pythonic.

    @section    Purpose
         Provide clear, typed exit codes for CLI return paths.

    @return     (enum) Exit code values OK, FAIL, BAD_ARGS.

    @note       Extend with additional codes as needed per project.
    ################################################################################################
    """

    OK = 0
    FAIL = 1
    BAD_ARGS = 2


@dataclass(slots=True)
class Settings:
    """
    ################################################################################################
    @fcn        Settings (dataclass)
    @brief      Runtime settings / configuration container.
    @details    Structured holder for inputs, outputs, verbosity, and dry-run.

    @section    Purpose
         Centralize run-time configuration and ease testing.

    @param[in]  input_path    Optional[Path] to read from.
    @param[in]  output_path   Optional[Path] to write to.
    @param[in]  verbosity     int (0=WARNING, 1=INFO, 2=DEBUG).
    @param[in]  dry_run       bool flag to avoid writes.

    @return     (Settings) configured instance.

    @note       Keep strictly serializable fields for easy JSON export.
    ################################################################################################
    """

    input_path: Optional[Path] = None
    output_path: Optional[Path] = None
    verbosity: int = 1
    dry_run: bool = False


# ============================================================================
# Logging
# ============================================================================

def configure_logging(verbosity: int = 1) -> None:
    """
    ################################################################################################
    @fcn        configure_logging
    @brief      Configure root logger formatting and level.
    @details    Sets a UTC-like timestamp and compact format for consistent logs across tools.

    @section    Purpose
         Provide reliable, minimal logging for scripts and packages.

    @param[in]  verbosity     0=WARNING, 1=INFO, 2=DEBUG (values >2 map to DEBUG)

    @return     (None) side-effect: configured logging.

    @pre        Called before operational work begins.
    @post       Root logger set; downstream modules inherit level/format.

    @section    Operation
         Resolve level, set basicConfig, force time.gmtime for UTC-like stamps.

    @note       Consider richer setup (handlers/JSON) in larger repos.
    ################################################################################################
    """
    level = logging.WARNING if verbosity <= 0 else logging.INFO if verbosity == 1 else logging.DEBUG

    logging.basicConfig(
        level=level,
        format="%(asctime)sZ | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )
    logging.Formatter.converter = time.gmtime


logger = logging.getLogger("jr.template")

# ============================================================================
# Utilities
# ============================================================================

def read_text(path: Path) -> str:
    """
    ################################################################################################
    @fcn        read_text
    @brief      Read a UTF-8 text file.
    @details    Thin wrapper over Path.read_text for consistency and typing.

    @param[in]  path     Path to file.
    @return     (str)    File contents as text.

    @pre        File exists and is text-encoded as UTF-8.
    @post       None.

    @note       For binary, prefer path.read_bytes().
    ################################################################################################
    """
    return path.read_text(encoding="utf-8")


def write_text(path: Path, data: str) -> None:
    """
    ################################################################################################
    @fcn        write_text
    @brief      Write a UTF-8 text file, creating parents as needed.
    @details    Ensures parent directories exist for safe writes.

    @param[in]  path     Destination path.
    @param[in]  data     Text payload to write.
    @return     (None)

    @pre        Data is serializable to text; path is writable.
    @post       File created/overwritten on disk.

    @note       For atomic writes, use temporary file + replace in larger projects.
    ################################################################################################
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data, encoding="utf-8")


# ============================================================================
# Core Domain (Example)
# ============================================================================

def load_settings(args: argparse.Namespace) -> Settings:
    """
    ################################################################################################
    @fcn        load_settings
    @brief      Construct a Settings object from parsed CLI args.
    @details    Maps argparse names to Settings fields and performs light type conversions.

    @param[in]  args     argparse.Namespace from build_arg_parser().parse_args()
    @return     (Settings) ready-to-use configuration.

    @pre        CLI already parsed.
    @post       None.

    @note       Expand with environment defaults or config files as needed.
    ################################################################################################
    """
    return Settings(
        input_path=Path(args.input) if args.input else None,
        output_path=Path(args.output) if args.output else None,
        verbosity=args.verbosity,
        dry_run=args.dry_run,
    )


def do_work(cfg: Settings) -> None:
    """
    ################################################################################################
    @fcn        do_work
    @brief      Perform the core work of the script/module.
    @details    Example pipeline stub — replace with project domain logic.

    @param[in]  cfg      Settings instance controlling behavior.
    @return     (None)

    @pre        Logging configured; cfg validated.
    @post       Output optionally written depending on cfg.

    @section    Operation
         - Load input if provided
         - Transform/process
         - Optionally write output

    @note       Raise exceptions for fatal issues; main() handles exit codes.
    ################################################################################################
    """
    logger.info("Starting work")

    if cfg.input_path:
        if not cfg.input_path.exists():
            raise FileNotFoundError(f"Input path not found: {cfg.input_path}")
        text = read_text(cfg.input_path)
        logger.debug("Loaded %d characters from %s", len(text), cfg.input_path)
    else:
        text = ""
        logger.debug("No input provided; proceeding with defaults")

    # Example transformation (identity). Replace with domain logic.
    result = text
    logger.debug("Processed text length=%d", len(result))

    if cfg.output_path:
        if cfg.dry_run:
            logger.info("DRY-RUN | Would write %d chars to %s", len(result), cfg.output_path)
        else:
            write_text(cfg.output_path, result)
            logger.info("Wrote %d chars to %s", len(result), cfg.output_path)

    logger.info("Work complete")


# ============================================================================
# CLI (argparse)
# ============================================================================

def build_arg_parser() -> argparse.ArgumentParser:
    """
    ################################################################################################
    @fcn        build_arg_parser
    @brief      Create and return the top-level CLI parser.
    @details    Defines global flags and subcommands {run, inspect} with defaults.

    @return     (argparse.ArgumentParser) configured parser.

    @pre        None.
    @post       None.

    @note       Extend with additional subcommands per project.
    ################################################################################################
    """
    p = argparse.ArgumentParser(
        prog="jr-template",
        description=(
            "Portfolio-ready Python template that mirrors an embedded-C discipline while "
            "remaining idiomatic to Python."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    p.add_argument("-i", "--input", help="Optional input file path")
    p.add_argument("-o", "--output", help="Optional output file path")
    p.add_argument("-n", "--dry-run", action="store_true", help="Do not write output")
    p.add_argument(
        "-v",
        "--verbosity",
        type=int,
        choices=[0, 1, 2],
        default=1,
        help="0=WARNING, 1=INFO, 2=DEBUG",
    )

    sub = p.add_subparsers(dest="command", metavar="{run,inspect}")

    prun = sub.add_parser("run", help="Run the main workflow")
    prun.set_defaults(command="run")

    pins = sub.add_parser("inspect", help="Print resolved settings and environment")
    pins.set_defaults(command="inspect")

    return p


# ============================================================================
# Entry Point
# ============================================================================

def main(argv: Optional[Sequence[str]] = None) -> int:
    """
    ################################################################################################
    @fcn        main
    @brief      Program entry point.
    @details    Parses CLI, configures logging, dispatches subcommands, manages exit codes.

    @param[in]  argv     Optional sequence of CLI args; None uses sys.argv[1:].
    @return     (int)    ExitCode value compatible with sys.exit().

    @pre        None.
    @post       Logging, side effects may occur depending on command.

    @section    Hazards & Risks
         Unhandled exceptions are caught and reported; returns FAIL.

    @note       Keep lightweight; heavy lifting belongs in separate modules.
    ################################################################################################
    """
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    configure_logging(args.verbosity)

    try:
        cfg = load_settings(args)
        logger.debug("Resolved settings: %s", cfg)

        if args.command in (None, "run"):
            do_work(cfg)
        elif args.command == "inspect":
            print(json.dumps(dataclasses.asdict(cfg), indent=2, default=str))
        else:
            parser.error(f"Unknown command: {args.command}")

        return ExitCode.OK
    except FileNotFoundError as e:
        logger.error(str(e))
        return ExitCode.FAIL
    except KeyboardInterrupt:
        logger.warning("Interrupted by user")
        return ExitCode.FAIL
    except Exception:
        logger.exception("Unhandled exception")
        return ExitCode.FAIL


if __name__ == "__main__":
    sys.exit(main())

# ============================================================================
# Developer Notes (Template)
# ----------------------------------------------------------------------------
# - Add domain modules under a `src/` package for larger projects.
# - Replace `do_work` with proper orchestration and decouple pure functions for testing.
# - Consider `pydantic` or `attrs` for richer config validation when needed.
# - Add `pyproject.toml` with Ruff/Black/mypy for repo-level consistency.
# - Provide a `tests/` directory with `pytest` scaffolding.
# ============================================================================
