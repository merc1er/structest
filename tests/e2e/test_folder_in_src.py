from pathlib import Path

from typer.testing import CliRunner

from structest.cli import app

from .assertions import assert_all_tests_mapped

runner = CliRunner()


class TestFolderInSrc:
    path = Path(__file__).parent.parent.parent / "examples" / "test_folder_in_src"

    def test_test_folder_in_src(self) -> None:
        src = self.path / "src"
        tests = src / "tests"

        result = runner.invoke(app, [str(src), str(tests)])

        assert_all_tests_mapped(result)
