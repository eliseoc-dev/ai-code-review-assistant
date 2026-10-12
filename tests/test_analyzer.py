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