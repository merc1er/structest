from pathlib import Path

from typer.testing import CliRunner

from structest.cli import app

runner = CliRunner()


class TestFolderAtTheRoot:
    path = Path(__file__).parent.parent.parent / "examples" / "test_folder_at_the_root"

    def test_test_folder_at_the_root(self) -> None:
        src = self.path / "src"
        tests = self.path / "tests"

        result = runner.invoke(app, [str(src), str(tests)])

        # The expected behavior: no output to stderr, green message saying all tests
        # are mapped.
        assert result.exit_code == 0
        assert "All test files are correctly named and mapped." in result.output
