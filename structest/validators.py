import os

import typer
from rich.console import Console

err_console = Console(stderr=True)


def is_eligible_module(file_name: str) -> bool:
    """Check if the file is eligible for testing."""

    if (
        file_name.endswith(".py")
        and not file_name.startswith("__")
        and not file_name.startswith("test_")
        and not file_name.endswith("_test.py")
    ):
        return True
    return False


def check_directory_exists(path: str) -> None:
    if not os.path.isdir(path):
        err_console.print(f"[bold red]Directory '{path}' does not exist.[/]")
        raise typer.Exit(1)
