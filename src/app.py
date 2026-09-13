# Import Streamlit
# Streamlit is used to create the web interface for our AI Study Guide Agent
import streamlit as st

import os
import json

from rag import ingest_file
from agent import study_agent


# Configure the Streamlit webpage
st.set_page_config(
    page_title="AI Study Guide Agent",  # Browser tab title
    page_icon="📚",  # Browser tab icon
    layout="wide"  # Use the full width of the screen
)


# --------------------------------------------------
# History Functions
# --------------------------------------------------

# File where we permanently store the history
HISTORY_FILE = "history.json"


# Load previous history from history.json
def load_history():

    # Check whether the history file exists
    if os.path.exists(HISTORY_FILE):

        try:

            # Open the history file in read mode
            with open(HISTORY_FILE, "r", encoding="utf-8") as file:

                # Convert JSON data into a Python list
                return json.load(file)

        except (json.JSONDecodeError, OSError):

            # If the file is empty or damaged,
            # start with an empty history
            return []

    # If the file does not exist yet,
    # return an empty history
    return []


# Save history to history.json
def save_history(history):

    # Open the history file in write mode
    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        # Convert the Python list into JSON
        # and save it to the file
        json.dump(
            history,
            file,
            indent=4,
            ensure_ascii=False
        )


# --------------------------------------------------
# Load History
# --------------------------------------------------

# Load history only when the Streamlit session starts
if "history" not in st.session_state:

    st.session_state.history = load_history()


# --------------------------------------------------
# Sidebar - History
# --------------------------------------------------

# Display the History heading in the sidebar
st.sidebar.title("📜 History")


# Check whether there is any previous history
if not st.session_state.history:

    # Show this message when there are no previous requests
    st.sidebar.write("No history yet.")


else:

    # Display newest requests first
    for i, item in enumerate(
        reversed(st.session_state.history),1
    ):

        # Create an expandable section for each history item
        with st.sidebar.expander(
            f"{i}. {item['request']}"
        ):

            # Display the previous AI result
            st.write(item["result"])



# Display the main title of our application
st.title("📚 Generative AI Study Guide Agent")

# Display a short description below the title
st.write(
    "Upload your course material and use AI to generate "
    "summaries, flashcards, and answers to questions."
)


# --------------------------------------------------
# File Upload
# --------------------------------------------------

# Display section heading
st.header("Upload Course Material")

# Create a file upload box
uploaded_file = st.file_uploader(
    "Upload a PDF, TXT, or CSV file",
    type=["pdf", "txt", "csv"]
)


if uploaded_file is not None:

    # This block runs only when the user clicks this button
    if st.button("Process Material"):

        # Show a loading message while the file is being processed
        with st.spinner("Processing course material..."):

            try:
                # Send the uploaded file to ingest_file(
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

# Create a horizontal divider between sections
st.divider()

st.header("Generate Study Material")

# Create a text input box
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
                
                # Save the user's request and AI result in session history
                st.session_state.history.append({
                    "request": request,"result": result
                })
                
                # Permanently save the updated history to history.json
                save_history(st.session_state.history)

                # Store the latest result
                st.session_state.latest_result = result

                # Refresh the Streamlit page so the sidebar shows the new history
                st.rerun()

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
# Display Latest Result
# --------------------------------------------------

if "latest_result" in st.session_state:

    st.subheader("Generated Result")

    st.write(
        st.session_state.latest_result
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