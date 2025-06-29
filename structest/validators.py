def is_eligible_module(file_name: str) -> bool:
    """Check if the file is eligible for testing."""

    if (
        file_name.endswith(".py")
        and not file_name.startswith("__")
        and not file_name.startswith("test_")
        and not file_name.endswith("_test.py")
    ):
        return True
    return False
