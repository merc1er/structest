from pathlib import Path

import pytest
from typer.testing import CliRunner

from structest.cli import app

from .assertions import assert_all_tests_mapped

runner = CliRunner()


class TestFolderAtTheRoot:
    path = Path(__file__).parent.parent.parent / "examples" / "test_folder_at_the_root"

    def test_test_folder_at_the_root(self) -> None:
        src = self.path / "src"
        tests = self.path / "tests"

        result = runner.invoke(app, [str(src), str(tests)])

        assert_all_tests_mapped(result)

    @pytest.mark.skip(reason="Feature not implemented yet")
    def test_tests_directory_omitted(self) -> None:
        # TODO: Implement dynamic discovery of the tests directory.
        src = self.path / "src"

        result = runner.invoke(app, [str(src)])

        assert_all_tests_mapped(result)
