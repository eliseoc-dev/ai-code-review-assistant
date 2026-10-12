from dataclasses import dataclass


@dataclass
class CodeIssue:
    rule: str
    message: str
    severity: str
    line: int | None = None
    suggestion: str | None = None