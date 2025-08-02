import os
from typing import Annotated

import typer
from rich import print

from structest.formatting import print_list_of_files
from structest.validators import check_directory_exists, is_eligible_module

app = typer.Typer()


@app.command()
def main(
    source_directory: Annotated[
        str,
        typer.Argument(help="Path to the project's source directory (e.g. 'src/')."),
    ],
    tests_directory: Annotated[
        str,
        typer.Argument(
            help="Path to the project's tests directory. This is usually 'tests/'."
        ),
    ] = "tests/",
) -> None:
    check_directory_exists(source_directory)

    source_dirs = get_dirs(source_directory)
    modules = find_modules(source_dirs)
    tests = find_test_files(tests_directory)

    missing_tests = modules - tests
    extra_tests = tests - modules

    if missing_tests:
        print("[bold red]Missing tests for:[/]")
        print_list_of_files(missing_tests)
    if extra_tests:
        print("[bold red]Test files without matching modules:[/]")
        print_list_of_files(extra_tests)
    if not missing_tests and not extra_tests:
        print("[bold green]All test files are correctly named and mapped.[/]")

    if missing_tests or extra_tests:
        raise typer.Exit(1)


def get_dirs(base_path: str) -> list[str]:
    ignore = {"tests", "__pycache__", ".git", ".venv", "venv", ".mypy_cache"}
    result = []
    for directory in os.listdir(base_path):
        full_path = os.path.join(base_path, directory)
        if os.path.isdir(full_path) and directory not in ignore:
            result.append(directory)
    print("Directories found:", result)
    return result


def find_modules(base_dirs: list[str]) -> set[str]:
    modules = set()
    for base_dir in base_dirs:
        for root, _, file_names in os.walk(base_dir):
            for file_name in file_names:
                if is_eligible_module(file_name):
                    modules.add(file_name)
    print("Modules found:", modules)
    return modules


def find_test_files(test_dir: str) -> set[str]:
    tests = set()
    for root, _, files in os.walk(test_dir):
        for file in files:
            if file.startswith("test_") and file.endswith(".py"):
                module_name = file[len("test_") :]  # Keep .py extension
                tests.add(module_name)
    print("Test files found:", tests)
    return tests


if __name__ == "__main__":
    app()
