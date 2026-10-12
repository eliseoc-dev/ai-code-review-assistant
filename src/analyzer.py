import ast
import re

from .models import CodeIssue


def analyze_python_code(
    code: str,
) -> list[CodeIssue]:
    issues: list[CodeIssue] = []

    issues.extend(
        check_syntax(code)
    )

    if any(
        issue.rule == "syntax-error"
        for issue in issues
    ):
        return issues

    tree = ast.parse(code)

    issues.extend(
        check_eval_usage(tree)
    )

    issues.extend(
        check_exec_usage(tree)
    )

    issues.extend(
        check_bare_except(tree)
    )

    issues.extend(
        check_mutable_defaults(tree)
    )

    issues.extend(
        check_hardcoded_secrets(code)
    )

    issues.extend(
        check_debug_prints(tree)
    )

    return issues


def check_syntax(
    code: str,
) -> list[CodeIssue]:
    try:
        ast.parse(code)

        return []

    except SyntaxError as error:
        return [
            CodeIssue(
                rule="syntax-error",
                message=error.msg,
                severity="critical",
                line=error.lineno,
            )
        ]


def check_eval_usage(
    tree: ast.AST,
) -> list[CodeIssue]:
    issues = []

    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(
                node.func,
                ast.Name,
            )
            and node.func.id == "eval"
        ):
            issues.append(
                CodeIssue(
                    rule="dangerous-eval",
                    message=(
                        "Avoid eval(). It can execute "
                        "arbitrary Python code."
                    ),
                    severity="high",
                    line=node.lineno,
                )
            )

    return issues


def check_exec_usage(
    tree: ast.AST,
) -> list[CodeIssue]:
    issues = []

    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(
                node.func,
                ast.Name,
            )
            and node.func.id == "exec"
        ):
            issues.append(
                CodeIssue(
                    rule="dangerous-exec",
                    message=(
                        "Avoid exec() when processing "
                        "untrusted input."
                    ),
                    severity="high",
                    line=node.lineno,
                )
            )

    return issues


def check_bare_except(
    tree: ast.AST,
) -> list[CodeIssue]:
    issues = []

    for node in ast.walk(tree):
        if isinstance(
            node,
            ast.ExceptHandler,
        ):
            if node.type is None:
                issues.append(
                    CodeIssue(
                        rule="bare-except",
                        message=(
                            "Avoid bare except. Catch "
                            "specific exceptions."
                        ),
                        severity="medium",
                        line=node.lineno,
                    )
                )

    return issues


def check_mutable_defaults(
    tree: ast.AST,
) -> list[CodeIssue]:
    issues = []

    for node in ast.walk(tree):
        if isinstance(
            node,
            ast.FunctionDef,
        ):
            for default in node.args.defaults:
                if isinstance(
                    default,
                    (
                        ast.List,
                        ast.Dict,
                        ast.Set,
                    ),
                ):
                    issues.append(
                        CodeIssue(
                            rule="mutable-default",
                            message=(
                                "Mutable default argument "
                                "can preserve state between calls."
                            ),
                            severity="medium",
                            line=node.lineno,
                        )
                    )

    return issues


def check_debug_prints(
    tree: ast.AST,
) -> list[CodeIssue]:
    issues = []

    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(
                node.func,
                ast.Name,
            )
            and node.func.id == "print"
        ):
            issues.append(
                CodeIssue(
                    rule="debug-print",
                    message=(
                        "Consider replacing print() "
                        "with structured logging."
                    ),
                    severity="low",
                    line=node.lineno,
                )
            )

    return issues


def check_hardcoded_secrets(
    code: str,
) -> list[CodeIssue]:
    issues = []

    pattern = re.compile(
        r"""(?ix)
        \b(
            password
            |passwd
            |api_key
            |secret
            |token
        )
        \s*=\s*
        ["']
        [^"']{6,}
        ["']
        """
    )

    for match in pattern.finditer(code):
        line = (
            code[:match.start()]
            .count("\n")
            + 1
        )

        issues.append(
            CodeIssue(
                rule="hardcoded-secret",
                message=(
                    "Possible hardcoded secret detected. "
                    "Use environment variables."
                ),
                severity="critical",
                line=line,
            )
        )

    return issues