import streamlit as st

from src.analyzer import (
    analyze_python_code,
)
from src.report import build_summary


st.set_page_config(
    page_title="AI Code Review Assistant",
    page_icon="🧠",
    layout="wide",
)


st.title(
    "🧠 AI Code Review & Debugging Assistant"
)

st.caption(
    "Static Python code analysis for bugs, "
    "security risks and maintainability issues."
)


code = st.text_area(
    "Paste Python code",
    height=450,
    placeholder=(
        "def example():\n"
        "    print('Hello')"
    ),
)


if st.button(
    "Analyze Code",
    type="primary",
):
    if not code.strip():
        st.warning(
            "Paste some Python code first."
        )

    else:
        issues = analyze_python_code(
            code
        )

        summary = build_summary(
            issues
        )


        st.divider()

        score = summary[
            "quality_score"
        ]

        st.subheader(
            "Code Quality Score"
        )

        st.progress(
            score / 100
        )

        st.metric(
            "Quality Score",
            f"{score}/100",
        )


        col1, col2, col3, col4, col5 = (
            st.columns(5)
        )

        col1.metric(
            "Issues",
            summary["total_issues"],
        )

        col2.metric(
            "Critical",
            summary["critical"],
        )

        col3.metric(
            "High",
            summary["high"],
        )

        col4.metric(
            "Medium",
            summary["medium"],
        )

        col5.metric(
            "Low",
            summary["low"],
        )


        if not issues:
            st.success(
                "No issues detected."
            )

        else:
            st.subheader(
                "Code Review"
            )

            ordered_issues = sorted(
                issues,
                key=lambda issue: {
                    "critical": 0,
                    "high": 1,
                    "medium": 2,
                    "low": 3,
                }.get(
                    issue.severity,
                    4,
                ),
            )


            for issue in ordered_issues:
                with st.container(
                    border=True
                ):
                    st.markdown(
                        f"### "
                        f"{issue.severity.upper()} "
                        f"— {issue.rule}"
                    )

                    st.write(
                        f"**Line:** "
                        f"{issue.line}"
                    )

                    st.write(
                        issue.message
                    )

                    if issue.suggestion:
                        st.info(
                            "Suggestion: "
                            + issue.suggestion
                        )

        report_lines = [
            "# Code Review Report",
            "",
            f"Quality Score: {score}/100",
            "",
        ]


        for issue in ordered_issues:
            report_lines.extend(
                [
                    (
                        f"## "
                        f"{issue.severity.upper()} "
                        f"— {issue.rule}"
                    ),
                    "",
                    f"Line: {issue.line}",
                    "",
                    issue.message,
                    "",
                    (
                        "Suggestion: "
                        f"{issue.suggestion}"
                    ),
                    "",
                ]
            )


        report_text = "\n".join(
            report_lines
        )


        st.download_button(
            label="Download Review Report",
            data=report_text,
            file_name="code_review_report.md",
            mime="text/markdown",
        )