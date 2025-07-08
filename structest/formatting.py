def print_list_of_files(files: set[str]) -> None:
    """Prints a list of files in a formatted way."""

    if not files:
        print("No files found.")
        return

    for file in sorted(files):
        print(file)
