# 📚 Generative AI Agent for Automated Study Guide Creation

An AI-powered study guide generation system that uses **Retrieval-Augmented Generation (RAG)** to analyze educational course materials and generate personalized study content.

The system supports **PDF, TXT, and CSV** files and can generate **summaries, Q&A responses, and flashcards** for beginner, intermediate, and advanced students.

---

## 📌 Project Overview

The system helps students and professors convert course material into useful study resources.

It:

- Extracts text from PDF, TXT, and CSV files
- Splits text into chunks
- Creates embeddings using Sentence Transformers
- Stores embeddings in ChromaDB
- Retrieves relevant content using semantic search
- Uses Gemini to generate study material
- Supports different student levels
- Provides a Streamlit web interface

---

## 🎯 Objectives

1. Automate study guide creation.
2. Reduce time spent reviewing course materials.
3. Use RAG to ground AI responses in uploaded material.
4. Provide personalized learning levels.
5. Generate summaries, Q&A, and flashcards.
6. Demonstrate Generative AI, embeddings, vector databases, and agent workflows.

---

## 🏗️ Architecture

```text
              Course Material
             PDF / TXT / CSV
                    │
                    ▼
              Text Extraction
                    │
                    ▼
                 Chunking
                    │
                    ▼
                Embeddings
                    │
                    ▼
                ChromaDB
                    │
                    ▼
              Semantic Retrieval
                    │
                    ▼
                Study Agent
                    │
          ┌─────────┼─────────┐
          ▼         ▼         ▼
       Summary     Q&A    Flashcards
          │         │         │
          └─────────┼─────────┘
                    ▼
                  Gemini
                    │
                    ▼
              Streamlit UI
```

---

## 🧠 How It Works

### 1. Upload

The user uploads a:

- PDF
- TXT
- CSV

### 2. Process

The system:

```text
File
 ↓
Text Extraction
 ↓
Chunking
 ↓
Embeddings
 ↓
ChromaDB
```

### 3. Retrieve

When the user asks a question or requests study material, relevant chunks are retrieved from ChromaDB.

### 4. Generate

The retrieved context is provided to Gemini to generate the requested study material.

---

## 🤖 Study Agent

The study agent identifies the requested task and difficulty level.

Examples:

```text
Create a beginner summary
```

```text
Create an intermediate summary
```

```text
Create advanced flashcards
```

For normal questions, a level is not required:

```text
What is sampling?
```

If no level is specified for a summary or flashcard request, **intermediate** is used by default.

---

## 📖 Features

### Summary

Supports:

- Beginner
- Intermediate
- Advanced

Examples:

```text
Create a beginner summary
Create an intermediate summary
Create an advanced summary
```

### Q&A

Ask questions about the uploaded material.

Examples:

```text
What is sampling?
```

```text
Explain the Nyquist sampling theorem.
```

### Flashcards

Generates five flashcards based on the course material.

Examples:

```text
Create beginner flashcards
Create intermediate flashcards
Create advanced flashcards
```

---

## 📁 Project Structure

```text
study-AI-agent-v2/
│
├── data/
│   └── DSP-1.pdf
│
├── src/
│   ├── agent.py
│   ├── app.py
│   ├── loaders.py
│   ├── prompts.py
│   ├── rag.py
│   └── tools.py
│
├── chroma_db/
├── .env
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

| File | Purpose |
|---|---|
| `loaders.py` | Reads PDF, TXT and CSV |
| `rag.py` | Chunking, embeddings, ChromaDB and retrieval |
| `prompts.py` | AI prompts |
| `tools.py` | Summary, Q&A and flashcard generation |
| `agent.py` | Task and level detection |
| `app.py` | Streamlit interface |

---

## 🛠️ Technologies

- **Python**
- **Streamlit**
- **Google Gemini**
- **ChromaDB**
- **Sentence Transformers**
- **PyPDF**
- **uv**
- **Retrieval-Augmented Generation (RAG)**

---

## 📦 Installation

From the project directory:

```bash
uv sync
```

Create a `.env` file:

```text
GEMINI_API_KEY=your_api_key_here
```

Do not commit the `.env` file to GitHub.

---

## ▶️ Running the Application

From the project root:

```bash
uv run streamlit run src/app.py
```

Open the URL shown by Streamlit, usually:

```text
http://localhost:8501
```

---

## 📝 Using the Application

### Step 1

Upload your course material.

Example:

```text
DSP-1.pdf
```

### Step 2

Click:

```text
Process Material
```

The system extracts the text, creates chunks and stores embeddings in ChromaDB.

### Step 3

Enter a request.

Examples:

```text
Create a beginner summary
```

```text
Create advanced flashcards
```

```text
What is sampling?
```

### Step 4

Click:

```text
Generate Study Material
```

The generated result will appear in the Streamlit interface.

---

## 🧪 Testing

Test the main components with:

```bash
uv run python -c "from loaders import extract_text; print('Loaders work')"
```

```bash
uv run python -c "from rag import get_collection; print('RAG works')"
```

```bash
uv run python -c "from tools import ask_gemini; print('Tools work')"
```

Test the agent:

```bash
uv run python -c "from agent import detect_level, detect_task; print(detect_level('Create a beginner summary')); print(detect_task('Create a beginner summary'))"
```

Expected:

```text
beginner
summary
```

---

## 🔄 Example Workflow

```text
Professor uploads DSP-1.pdf
            ↓
      Process Material
            ↓
       Text Extraction
            ↓
          Chunking
            ↓
        Embeddings
            ↓
         ChromaDB
            ↓
Student enters request
            ↓
       Study Agent
            ↓
     Relevant Retrieval
            ↓
          Gemini
            ↓
     Generated Study Guide
```

---

## ⚠️ Limitations

- Gemini API usage is subject to quotas and rate limits.
- The application processes files uploaded through the Streamlit interface.
- Scanned/image-only PDFs may require OCR.
- Retrieval quality depends on the uploaded material and embedding model.
- The current agent uses request-based task and difficulty detection rather than fully autonomous LLM tool selection.

---

## 🚀 Future Improvements

- Multiple file upload
- OCR for scanned PDFs
- Source citations
- Quiz generation
- Multiple-choice questions
- Practice exams
- Downloadable study guides
- Improved agent tool selection
- More advanced Streamlit UI

---

## 🎓 Educational Value

This project demonstrates practical applications of:

- Generative AI
- RAG
- Prompt Engineering
- Text Embeddings
- Semantic Search
- Vector Databases
- AI Agents
- Streamlit

---

## 📜 License

This project was developed as an academic project for educational purposes.