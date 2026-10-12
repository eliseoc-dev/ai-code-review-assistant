from collections import Counter

from .models import CodeIssue


def build_summary(
    issues: list[CodeIssue],
) -> dict:
    severity_counts = Counter(
        issue.severity
        for issue in issues
    )

    return {
        "total_issues": len(issues),
        "critical": severity_counts[
            "critical"
        ],
        "high": severity_counts["high"],
        "medium": severity_counts[
            "medium"
        ],
        "low": severity_counts["low"],
    }