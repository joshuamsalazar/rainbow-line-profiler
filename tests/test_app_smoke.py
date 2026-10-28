"""Smoke test to ensure the app script can be imported without syntax errors."""


def test_app_import():
    """Just importing src/simple_app.py should not raise SyntaxError or ImportError (if deps were present)."""
    try:
        # We can't fully run it without Streamlit environment, but we can check syntax
        import ast

        with open("src/simple_app.py", "r") as f:
            code = f.read()
        ast.parse(code)
        assert True
    except SyntaxError:
        assert False, "src/simple_app.py has syntax errors"
