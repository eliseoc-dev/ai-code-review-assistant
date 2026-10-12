from src.analyzer import (
    analyze_python_code,
)


def get_rules(code: str):
    issues = analyze_python_code(code)

    return {
        issue.rule
        for issue in issues
    }


def test_detects_eval():
    code = """
value = eval(user_input)
"""

    assert (
        "dangerous-eval"
        in get_rules(code)
    )


def test_detects_exec():
    code = """
exec(user_input)
"""

    assert (
        "dangerous-exec"
        in get_rules(code)
    )


def test_detects_mutable_default():
    code = """
def test(values=[]):
    return values
"""

    assert (
        "mutable-default"
        in get_rules(code)
    )


def test_detects_bare_except():
    code = """
try:
    do_something()
except:
    pass
"""

    assert (
        "bare-except"
        in get_rules(code)
    )


def test_detects_secret():
    code = '''
api_key = "abcdef123456"
'''

    assert (
        "hardcoded-secret"
        in get_rules(code)
    )


def test_detects_syntax_error():
    code = """
def broken(
"""

    assert (
        "syntax-error"
        in get_rules(code)
    )


def test_clean_code():
    code = """
def add(a, b):
    return a + b
"""

    assert len(
        analyze_python_code(code)
    ) == 0


def test_detects_subprocess_shell():
    code = """
import subprocess
subprocess.run(command, shell=True)
"""

    assert (
        "subprocess-shell"
        in get_rules(code)
    )


def test_detects_open_without_context():
    code = """
file = open("data.txt")
content = file.read()
"""

    assert (
        "open-without-context"
        in get_rules(code)
    )


def test_safe_open_with_context():
    code = """
with open("data.txt") as file:
    content = file.read()
"""

    assert (
        "open-without-context"
        not in get_rules(code)
    )


def test_detects_sql_interpolation():
    code = """
cursor.execute(
    f"SELECT * FROM users WHERE id = {user_id}"
)
"""

    assert (
        "sql-string-building"
        in get_rules(code)
    )


def test_detects_unused_import():
    code = """
import os

value = 10
"""

    assert (
        "unused-import"
        in get_rules(code)
    )