from typer.testing import Result


def assert_all_tests_mapped(result: Result) -> None:
    if result.exit_code != 0:
        _print_cli_output(result)

    assert result.exit_code == 0
    assert "All test files are correctly named and mapped." in result.stdout
    assert not result.stderr


def assert_incorrect_structure(result: Result) -> None:
    if result.exit_code != 1:
        _print_cli_output(result)

    assert result.exit_code == 1
    assert "Missing tests for:" in result.stdout
    assert not result.stderr


def _print_cli_output(result: Result) -> None:
    """
    Prints the CLI output for debugging purposes. Makes it trivial to see what went
    wrong.
    """

    print("STDOUT:\n", result.stdout)
    print("STDERR:\n", result.stderr)
    print("EXIT CODE:", result.exit_code)
