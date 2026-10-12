import ast
import re

from .models import CodeIssue


def analyze_python_code(
    code: str,
) -> list[CodeIssue]:
    issues: list[CodeIssue] = []

    syntax_issues = check_syntax(code)
    issues.extend(syntax_issues)

    if syntax_issues:
        return issues

    tree = ast.parse(code)

    checks = [
        check_eval_usage,
        check_exec_usage,
        check_bare_except,
        check_mutable_defaults,
        check_debug_prints,
        check_long_functions,
        check_complex_functions,
        check_unused_imports,
        check_subprocess_shell,
        check_open_without_with,
        check_sql_string_building,
    ]

    for check in checks:
        issues.extend(
            check(tree)
        )

    issues.extend(
        check_hardcoded_secrets(code)
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
                suggestion=(
                    "Fix the Python syntax before "
                    "running additional analysis."
                ),
            )
        ]


def check_eval_usage(
    tree: ast.AST,
) -> list[CodeIssue]:
    issues = []

    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "eval"
        ):
            issues.append(
                CodeIssue(
                    rule="dangerous-eval",
                    message=(
                        "eval() can execute arbitrary "
                        "Python code."
                    ),
                    severity="high",
                    line=node.lineno,
                    suggestion=(
                        "Avoid eval(). If you only need "
                        "Python literals, consider "
                        "ast.literal_eval()."
                    ),
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
            and isinstance(node.func, ast.Name)
            and node.func.id == "exec"
        ):
            issues.append(
                CodeIssue(
                    rule="dangerous-exec",
                    message=(
                        "exec() can execute arbitrary code."
                    ),
                    severity="high",
                    line=node.lineno,
                    suggestion=(
                        "Replace dynamic execution with "
                        "explicit functions or safe parsing."
                    ),
                )
            )

    return issues


def check_bare_except(
    tree: ast.AST,
) -> list[CodeIssue]:
    issues = []

    for node in ast.walk(tree):
        if (
            isinstance(node, ast.ExceptHandler)
            and node.type is None
        ):
            issues.append(
                CodeIssue(
                    rule="bare-except",
                    message=(
                        "Bare except catches every exception."
                    ),
                    severity="medium",
                    line=node.lineno,
                    suggestion=(
                        "Catch specific exception types "
                        "such as ValueError or OSError."
                    ),
                )
            )

    return issues


def check_mutable_defaults(
    tree: ast.AST,
) -> list[CodeIssue]:
    issues = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
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
                                "Mutable default arguments "
                                "can preserve state between calls."
                            ),
                            severity="medium",
                            line=node.lineno,
                            suggestion=(
                                "Use None as the default and "
                                "create the object inside the function."
                            ),
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
            and isinstance(node.func, ast.Name)
            and node.func.id == "print"
        ):
            issues.append(
                CodeIssue(
                    rule="debug-print",
                    message=(
                        "print() may be leftover debugging "
                        "or unsuitable for production logging."
                    ),
                    severity="low",
                    line=node.lineno,
                    suggestion=(
                        "Use Python's logging module for "
                        "structured application logs."
                    ),
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
                    "Possible hardcoded secret detected."
                ),
                severity="critical",
                line=line,
                suggestion=(
                    "Move secrets to environment variables "
                    "or a dedicated secrets manager."
                ),
            )
        )

    return issues


def check_long_functions(
    tree: ast.AST,
) -> list[CodeIssue]:
    issues = []

    for node in ast.walk(tree):
        if isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        ):
            end_line = getattr(
                node,
                "end_lineno",
                node.lineno,
            )

            length = (
                end_line
                - node.lineno
                + 1
            )

            if length > 40:
                issues.append(
                    CodeIssue(
                        rule="long-function",
                        message=(
                            f"Function '{node.name}' "
                            f"is {length} lines long."
                        ),
                        severity="medium",
                        line=node.lineno,
                        suggestion=(
                            "Split the function into smaller "
                            "single-responsibility functions."
                        ),
                    )
                )

    return issues


def check_complex_functions(
    tree: ast.AST,
) -> list[CodeIssue]:
    issues = []

    complexity_nodes = (
        ast.If,
        ast.For,
        ast.While,
        ast.Try,
        ast.BoolOp,
        ast.IfExp,
        ast.comprehension,
        ast.Match,
    )

    for node in ast.walk(tree):
        if isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        ):
            complexity = 1

            for child in ast.walk(node):
                if isinstance(
                    child,
                    complexity_nodes,
                ):
                    complexity += 1

            if complexity > 10:
                issues.append(
                    CodeIssue(
                        rule="high-complexity",
                        message=(
                            f"Function '{node.name}' "
                            f"has estimated complexity "
                            f"{complexity}."
                        ),
                        severity="medium",
                        line=node.lineno,
                        suggestion=(
                            "Reduce branching or extract "
                            "logic into smaller functions."
                        ),
                    )
                )

    return issues


def check_unused_imports(
    tree: ast.AST,
) -> list[CodeIssue]:
    issues = []

    imported_names: dict[
        str,
        int,
    ] = {}

    used_names = {
        node.id
        for node in ast.walk(tree)
        if isinstance(
            node,
            ast.Name,
        )
    }

    for node in ast.walk(tree):
        if isinstance(
            node,
            ast.Import,
        ):
            for alias in node.names:
                name = (
                    alias.asname
                    or alias.name.split(".")[0]
                )

                imported_names[
                    name
                ] = node.lineno

        elif isinstance(
            node,
            ast.ImportFrom,
        ):
            for alias in node.names:
                if alias.name == "*":
                    continue

                name = (
                    alias.asname
                    or alias.name
                )

                imported_names[
                    name
                ] = node.lineno

    for name, line in imported_names.items():
        if name not in used_names:
            issues.append(
                CodeIssue(
                    rule="unused-import",
                    message=(
                        f"Import '{name}' "
                        "does not appear to be used."
                    ),
                    severity="low",
                    line=line,
                    suggestion=(
                        "Remove unused imports to keep "
                        "dependencies and code clean."
                    ),
                )
            )

    return issues


def check_subprocess_shell(
    tree: ast.AST,
) -> list[CodeIssue]:
    issues = []

    for node in ast.walk(tree):
        if not isinstance(
            node,
            ast.Call,
        ):
            continue

        is_subprocess_call = (
            isinstance(
                node.func,
                ast.Attribute,
            )
            and isinstance(
                node.func.value,
                ast.Name,
            )
            and node.func.value.id
            == "subprocess"
        )

        if not is_subprocess_call:
            continue

        for keyword in node.keywords:
            if (
                keyword.arg == "shell"
                and isinstance(
                    keyword.value,
                    ast.Constant,
                )
                and keyword.value.value
                is True
            ):
                issues.append(
                    CodeIssue(
                        rule="subprocess-shell",
                        message=(
                            "subprocess call uses shell=True."
                        ),
                        severity="high",
                        line=node.lineno,
                        suggestion=(
                            "Prefer shell=False and pass "
                            "arguments as a list, especially "
                            "when handling user input."
                        ),
                    )
                )

    return issues


def check_open_without_with(
    tree: ast.AST,
) -> list[CodeIssue]:
    issues = []

    open_calls = []

    protected_calls = set()

    for node in ast.walk(tree):
        if isinstance(
            node,
            ast.With,
        ):
            for item in node.items:
                expression = (
                    item.context_expr
                )

                if (
                    isinstance(
                        expression,
                        ast.Call,
                    )
                    and isinstance(
                        expression.func,
                        ast.Name,
                    )
                    and expression.func.id
                    == "open"
                ):
                    protected_calls.add(
                        id(expression)
                    )

        if (
            isinstance(node, ast.Call)
            and isinstance(
                node.func,
                ast.Name,
            )
            and node.func.id == "open"
        ):
            open_calls.append(node)

    for node in open_calls:
        if id(node) not in protected_calls:
            issues.append(
                CodeIssue(
                    rule="open-without-context",
                    message=(
                        "File opened without a context manager."
                    ),
                    severity="low",
                    line=node.lineno,
                    suggestion=(
                        "Use 'with open(...) as file:' "
                        "to ensure the file is closed."
                    ),
                )
            )

    return issues


def check_sql_string_building(
    tree: ast.AST,
) -> list[CodeIssue]:
    issues = []

    risky_methods = {
        "execute",
        "executemany",
    }

    for node in ast.walk(tree):
        if not isinstance(
            node,
            ast.Call,
        ):
            continue

        if not isinstance(
            node.func,
            ast.Attribute,
        ):
            continue

        if node.func.attr not in risky_methods:
            continue

        if not node.args:
            continue

        query = node.args[0]

        risky = isinstance(
            query,
            (
                ast.JoinedStr,
                ast.BinOp,
            ),
        )

        if risky:
            issues.append(
                CodeIssue(
                    rule="sql-string-building",
                    message=(
                        "SQL query appears to be built "
                        "using string interpolation."
                    ),
                    severity="high",
                    line=node.lineno,
                    suggestion=(
                        "Use parameterized SQL queries "
                        "instead of interpolating values "
                        "directly into SQL."
                    ),
                )
            )

    return issues