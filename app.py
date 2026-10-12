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
    "Analyze Python code for bugs, risky patterns and maintainability issues."
)


code = st.text_area(
    "Paste Python code",
    height=400,
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

            for issue in issues:
                with st.container(
                    border=True
                ):
                    st.markdown(
                        f"### {issue.severity.upper()}"
                    )

                    st.write(
                        f"**Rule:** "
                        f"`{issue.rule}`"
                    )

                    st.write(
                        f"**Line:** "
                        f"{issue.line}"
                    )

                    st.write(
                        issue.message
                    )