from pathlib import Path

import pytest
from typer.testing import CliRunner, Result

from structest.cli import app

runner = CliRunner()


class TestFolderAtTheRoot:
    path = Path(__file__).parent.parent.parent / "examples" / "test_folder_at_the_root"

    def test_test_folder_at_the_root(self) -> None:
        src = self.path / "src"
        tests = self.path / "tests"

        result = runner.invoke(app, [str(src), str(tests)])

        self._assert_correct_result(result)

    @pytest.mark.skip(reason="Feature not implemented yet")
    def test_tests_directory_omitted(self) -> None:
        # TODO: Implement dynamic discovery of the tests directory.
        src = self.path / "src"

        result = runner.invoke(app, [str(src)])

        self._assert_correct_result(result)

    @staticmethod
    def _assert_correct_result(result: Result) -> None:
        # The expected behavior: no output to stderr, green message saying all tests
        # are mapped.
        assert result.exit_code == 0
        assert "All test files are correctly named and mapped." in result.stdout
        assert not result.stderr
