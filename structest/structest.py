from pathlib import Path
from typing import Annotated

import typer
from rich import print

from structest.file_discovery import list_all_modules
from structest.formatting import print_list_of_files
from structest.validators import check_directory_exists

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
    check_directory_exists(tests_directory)

    source_dir_path = Path(source_directory).resolve()
    tests_dir_path = Path(tests_directory).resolve()

    print(f"Source directory: [bold]{source_dir_path}[/]")
    print(f"Tests directory: [bold]{tests_dir_path}[/]")

    modules = {
        str(Path(path).with_suffix("").relative_to(source_dir_path).as_posix())
        for path in list_all_modules(str(source_dir_path))
        if not Path(path).name.startswith("test_")
        and not Path(path).name.endswith("_test")
    }

    print("Modules found:", modules)

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


if __name__ == "__main__":
    app()
