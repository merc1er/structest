from pathlib import Path
from typing import Annotated

import typer
from rich import print

from structest.file_discovery import list_all_modules, resolve_directory
from structest.formatting import print_list_of_files

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
    source_dir_path = resolve_directory(source_directory)
    tests_dir_path = resolve_directory(tests_directory)

    modules = collect_modules(source_dir_path)
    tests = collect_test_modules(tests_dir_path)

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


def collect_test_modules(tests_dir_path: Path) -> set[str]:
    tests = set()
    for path in list_all_modules(str(tests_dir_path)):
        test_path = Path(path)
        if test_path.name.startswith("test_"):
            try:
                relative_path = test_path.relative_to(tests_dir_path)
                stripped_name = test_path.name[len("test_") :]
                test_module_path = (
                    relative_path.with_name(stripped_name).with_suffix("").as_posix()
                )
                tests.add(test_module_path)
            except ValueError:
                continue

    print("Test files found:", tests)
    return tests


def collect_modules(source_dir_path: Path) -> set[str]:
    modules = set()
    for path in list_all_modules(str(source_dir_path)):
        module_path = Path(path)

        # Skip test files
        if module_path.name.startswith("test_") or module_path.name.endswith("_test"):
            continue

        # Convert to relative path without extension
        relative_path = module_path.with_suffix("").relative_to(source_dir_path)
        module_name = relative_path.as_posix()
        modules.add(module_name)

    print("Modules found:", modules)
    return modules


if __name__ == "__main__":
    app()
