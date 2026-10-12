from collections import Counter

from .models import CodeIssue


PENALTIES = {
    "critical": 25,
    "high": 15,
    "medium": 8,
    "low": 3,
}


def calculate_quality_score(
    issues: list[CodeIssue],
) -> int:
    penalty = sum(
        PENALTIES.get(
            issue.severity,
            0,
        )
        for issue in issues
    )

    return max(
        0,
        100 - penalty,
    )


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
        "high": severity_counts[
            "high"
        ],
        "medium": severity_counts[
            "medium"
        ],
        "low": severity_counts[
            "low"
        ],
        "quality_score":
            calculate_quality_score(
                issues
            ),
    }