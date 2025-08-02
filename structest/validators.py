import os

import typer
from rich.console import Console

err_console = Console(stderr=True)


def check_directory_exists(path: str) -> None:
    if not os.path.isdir(path):
        err_console.print(f"[bold red]Directory '{path}' does not exist.[/]")
        raise typer.Exit(1)
