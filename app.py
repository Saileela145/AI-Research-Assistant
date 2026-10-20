import streamlit as st

from agent import research


# ==========================================
# Configuration
# ==========================================

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔎",
    layout="wide",
)


# ==========================================
# UI
# ==========================================

st.title("🔎 AI Research Assistant")

st.write(
    "Ask a question and let the AI research it using "
    "web search, webpage analysis, and calculations."
)


user_query = st.text_area(
    "What would you like me to research?",
    placeholder=(
        "Example: What is the latest stable version "
        "of Python? Find the official page and explain "
        "how you know."
    ),
    height=120,
)


research_button = st.button(
    "🔍 Research",
    type="primary",
    use_container_width=True,
)


# ==========================================
# Research
# ==========================================

if research_button:

    if not user_query.strip():

        st.warning(
            "Please enter a research question."
        )

    else:

        with st.status(
            "Starting research...",
            expanded=True,
        ) as status:

            def update_status(message):

                status.update(
                    label=message,
                    state="running",
                )

            try:

                answer, sources = research(
                    user_query,
                    status_callback=update_status,
                )

                status.update(
                    label="Research complete",
                    state="complete",
                )

            except Exception as e:

                status.update(
                    label="Research failed",
                    state="error",
                )

                st.error(
                    f"An error occurred: {str(e)}"
                )

                st.stop()

        # ==================================
        # Answer
        # ==================================

        st.markdown("## Answer")

        st.markdown(answer)

        # ==================================
        # Sources
        # ==================================

        if sources:

            st.markdown("## Sources Used")

            for i, source in enumerate(
                sources,
                start=1,
            ):

                title = source.get(
                    "title",
                    "Untitled source",
                )

                url = source.get(
                    "url",
                    "",
                )

                st.markdown(
                    f"**{i}. [{title}]({url})**"
                )

        else:

            st.info(
                "No web sources were used for this answer."
            )