import streamlit as st

from rag import ingest_file
from agent import study_agent


st.title("Generative AI Study Guide Agent")

st.write(
    "Upload course material and generate summaries, "
    "Q&A, and flashcards."
)

uploaded_file = st.file_uploader(
    "Upload course material",
    type=["pdf", "txt", "csv"]
)

level = st.selectbox(
    "Student level",
    ["beginner", "intermediate", "advanced"]
)

if uploaded_file is not None:

    if st.button("Process Material"):

        count = ingest_file(
            uploaded_file,
            uploaded_file.name
        )

        st.success(
            f"Successfully processed {count} chunks."
        )
    st.divider()

    st.subheader("Generate Study Guide")

    request = st.text_input(
        "What would you like to generate?",
        placeholder="Example: Create a beginner summary"
    )
    
    if st.button("Generate"):
        
        if request:
            result = study_agent(request)
            
            st.write(result)