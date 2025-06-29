# Structest

Lightweight Python library that ensures your test files follow standard naming
conventions and match the structure of your source code.

# Installation

You can install Structest using pip:

```bash
pip install structest
```

# Usage

Structest assumes your project follows the standard project structure:

```
project/
  project/   # your main package
  tests/     # tests directory
  README.md  # any other files
```

```bash
structest .
```

# FAQ

> What source files does structest check?

Any regular Python module. It does **not** check files that start with an underscore,
such as `__init__.py`, or files that start with `test_` or end with `_test.py`.

Look at the `is_eligible_module()` function in the source code for the exact criteria.

> What test files does structest check?

Test files should be located in a `tests/` directory and should follow the naming
convention `test_<module_name>.py` or `<module_name>_test.py`.
