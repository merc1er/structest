from pathlib import Path

from typer.testing import CliRunner

from structest.cli import app

from .assertions import assert_incorrect_structure

runner = CliRunner()


class TestIncorrectStructure:
    path = Path(__file__).parent.parent.parent / "examples" / "incorrect_structure"

    def test_incorrect_structure(self) -> None:
        src = self.path / "src"
        tests = self.path / "tests"

        result = runner.invoke(app, [str(src), str(tests)])

        assert_incorrect_structure(result)
