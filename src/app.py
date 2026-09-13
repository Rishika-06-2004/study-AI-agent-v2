import streamlit as st

from rag import ingest_file
from agent import study_agent


st.set_page_config(
    page_title="AI Study Guide Agent",
    page_icon="📚",
    layout="wide"
)


st.title("📚 Generative AI Study Guide Agent")

st.write(
    "Upload your course material and use AI to generate "
    "summaries, flashcards, and answers to questions."
)


# --------------------------------------------------
# File Upload
# --------------------------------------------------

st.header("1. Upload Course Material")

uploaded_file = st.file_uploader(
    "Upload a PDF, TXT, or CSV file",
    type=["pdf", "txt", "csv"]
)


if uploaded_file is not None:

    if st.button("Process Material"):

        with st.spinner("Processing course material..."):

            try:
                count = ingest_file(
                    uploaded_file,
                    uploaded_file.name
                )

                st.success(
                    f"Successfully processed {count} chunks."
                )

            except Exception as e:

                st.error(
                    f"Could not process the file: {e}"
                )


# --------------------------------------------------
# Study Guide Generation
# --------------------------------------------------

st.divider()

st.header("2. Generate Study Material")

request = st.text_input(
    "What would you like the AI to do?",
    placeholder=(
        "Example: Create a beginner summary"
    )
)


if st.button("Generate Study Material"):

    if not request.strip():

        st.warning(
            "Please enter a request first."
        )

    elif uploaded_file is None:

        st.warning(
            "Please upload and process course material first."
        )

    else:

        with st.spinner("Generating study material..."):

            try:

                result = study_agent(request)

                st.subheader("Generated Result")

                st.write(result)

            except Exception as e:

                if "429" in str(e):

                    st.error(
                        "The Gemini API quota has been reached. "
                        "Please try again after the quota resets."
                    )

                else:

                    st.error(
                        f"Something went wrong: {e}"
                    )


# --------------------------------------------------
# Examples
# --------------------------------------------------

st.divider()

st.header("Example Requests")

st.markdown(
    """
- **Create a beginner summary**
- **Create an intermediate summary**
- **Create advanced flashcards**
- **What is sampling?**
- **Explain the Nyquist sampling theorem**
"""
)