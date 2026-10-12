from pathlib import Path

from src.analyzer import (
    analyze_python_code,
)
from src.report import build_summary


SAMPLE_PATH = Path(
    "samples/bad_code.py"
)


def main() -> None:
    code = SAMPLE_PATH.read_text(
        encoding="utf-8"
    )

    issues = analyze_python_code(
        code
    )

    summary = build_summary(
        issues
    )

    print("=" * 60)
    print("AI CODE REVIEW ASSISTANT")
    print("=" * 60)

    print()
    print("Summary:")
    print(summary)

    print()

    for issue in issues:
        print(
            f"[{issue.severity.upper()}] "
            f"Line {issue.line}: "
            f"{issue.rule}"
        )

        print(
            f"  {issue.message}"
        )


if __name__ == "__main__":
    main()