from pathlib import Path

from structest.file_discovery import list_all_modules


class TestListAllModules:
    """Tests for the list_all_modules function."""

    def test_empty_directory(self, tmp_path: Path) -> None:
        assert list_all_modules(str(tmp_path)) == []

    def test_single_python_file(self, tmp_path: Path) -> None:
        file = tmp_path / "file.py"
        file.write_text("print('Hello')")
        assert list_all_modules(str(tmp_path)) == [str(file)]

    def test_ignores_non_python_files(self, tmp_path: Path) -> None:
        file = tmp_path / "not_python.txt"
        file.write_text("data")
        assert list_all_modules(str(tmp_path)) == []

    def test_ignores_dunder_files(self, tmp_path: Path) -> None:
        dunder = tmp_path / "__init__.py"
        dunder.write_text("# init")
        assert list_all_modules(str(tmp_path)) == []

    def test_nested_python_files(self, tmp_path: Path) -> None:
        (tmp_path / "dir1" / "dir2").mkdir(parents=True)
        f1 = tmp_path / "file1.py"
        f2 = tmp_path / "dir1" / "file2.py"
        f3 = tmp_path / "dir1" / "dir2" / "file3.py"
        for f in (f1, f2, f3):
            f.write_text("data")

        result = list_all_modules(str(tmp_path))
        expected = sorted([str(f1), str(f2), str(f3)])
        assert sorted(result) == expected

    def test_symlinks_to_python_files_are_included(self, tmp_path: Path) -> None:
        real_file = tmp_path / "real.py"
        real_file.write_text("print('real')")
        symlink = tmp_path / "link.py"
        symlink.symlink_to(real_file)

        result = list_all_modules(str(tmp_path))

        result_paths = {Path(p) for p in result}
        assert real_file in result_paths
        assert symlink.resolve() in result_paths
