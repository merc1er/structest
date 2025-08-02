import os
from pathlib import Path

IGNORED_DIRS = {
    "__pycache__",
    "venv",
    ".venv",
    ".git",
    ".mypy_cache",
    ".pytest_cache",
}


def list_all_modules(path: str) -> list[str]:
    base_path = Path(path).resolve()
    all_files = []

    for root, dirs, files in os.walk(base_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                full_path = Path(root) / file
                all_files.append(str(full_path.resolve()))

    return all_files
