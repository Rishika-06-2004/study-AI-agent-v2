import functools #Enhances functions (like caching data)
import os #Interacts with your operating system (like reading file paths or API keys)
import re #Matches and manipulates complex text patterns

import chromadb #This gives us the ChromaDB vector database
from chromadb.utils import embedding_functions #This lets ChromaDB use an embedding model
from dotenv import load_dotenv #Python to load values from your .env file
from google import genai
from pypdf import PdfReader #we'll use to extract text from the uploaded PDF

load_dotenv()

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

CHROMA_DIR = "./chroma_db"
COLLECTION_NAME = "study_materials"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = [] #chunk1, chunk2,...chunkN

    step = chunk_size - overlap #the next chunk starts 800 characters later
    start = 0 

    while start < len(text):
        #.strip() removes unnecessary spaces/newlines at the beginning and end
        piece = text[start:start + chunk_size].strip()

        if piece:
            chunks.append(piece)

        start += step #Move forward by 800 characters

    return chunks


def extract_pdf_text(source):
    reader = PdfReader(source)

    pages = []

    for page in reader.pages:  #Go through every page of the PDF
        text = page.extract_text() or ""
        pages.append(text)

    return "\n\n".join(pages)  #Combine all pages into one large text string


def get_collection():
    client = chromadb.PersistentClient(path=CHROMA_DIR) #creates a ChromaDB client

    #creates our embedding function using :
    #sentence-transformers/all-MiniLM-L6-v2

    embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBED_MODEL
    )

    #get_or_create_collection: If the collection already exists, 
    # it opens it. 
    # If it doesn't exist, it creates a new one
    #embedding_function=embed_fn: 
    #It attaches your embedding tool so the database can automatically 
    # convert your text into math vectors whenever 
    # you save or search data

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embed_fn
    )

    return collection


def ingest_pdf(source, filename):

    #Gets/opens our ChromaDB collection where we will store the PDF chunks
    collection = get_collection()

    text = extract_pdf_text(source)
    chunks = chunk_text(text)

    if not chunks:
        return 0
    
    #Starts creating a list of unique IDs for every chunk
    ids = [
        f"{filename}::{i}"
        for i in range(len(chunks))
    ]

    #create meta data using dictionary
    #[{"source_file": "dsp.pdf", "chunk_index": 0},
    #{"source_file": "dsp.pdf", "chunk_index": 1},
    #{"source_file": "dsp.pdf", "chunk_index": 2}]

    metadatas = [
        {
            "source_file": filename,
            "chunk_index": i
        }
        for i in range(len(chunks))
    ]

    #sends those chunks to ChromaDB
    collection.upsert(
        ids=ids,
        documents=chunks,
        metadatas=metadatas
    )

    return len(chunks)


 #k=4 means we want the 4 most relevant chunks
def retrieve_chunks(question, k=4):
    collection = get_collection() #Connects to your ChromaDB collection

    #ChromaDB searches your stored embeddings 
    #and finds the chunks most similar to the question
    #Chunk 7 → "Sampling is the process..."
    #Chunk 8 → "Sampling frequency..."
    #Chunk 9 → "Nyquist sampling theorem..."
    #Chunk 10 → "Aliasing occurs when..."

    results = collection.query(
        query_texts=[question],
        n_results=k
    )
    
    #results["documents"] show : 
    #[
    # [
    #    "Sampling is the process...",
    #    "Sampling frequency...",
    #    "Nyquist theorem...",
    #    "Aliasing occurs..."
    # ]
    #]
    #The [0] gets the first query's results
    documents = results["documents"][0]

    return documents



def ask_gemini(question):
    chunks = retrieve_chunks(question)  #Retrieve relevant chunks

    context = "\n\n".join(chunks)

    #Use the retrieved information from my PDF to answer the question.
    #This is the important part that makes it RAG,
    #rather than simply asking Gemini a general question

    prompt = f"""You are a study assistant.
    Answer the question using only the information provided in the context.Context:
    {context}
    Question:
    {question}
    Answer clearly and concisely."""

    client = _genai_client()

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text


def generate_summary():
    chunks = retrieve_chunks("main topics and important concepts")

    context = "\n\n".join(chunks)

    prompt = f"""You are an educational study-guide assistant.
    Create a concise study summary using only the information
    provided in the context.
    Context:
    {context}
    Organize the summary with:
    - Main topics
    - Important concepts
    - Key definitions
    - Important points
    Do not add information that is not present in the context."""

    client = _genai_client()

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text

def _genai_client():
    return genai.Client(api_key=os.environ["GEMINI_API_KEY"])


if __name__ == "__main__":
    pdf_path = "data/DSP-1.pdf"

    with open(pdf_path, "rb") as f:
        count = ingest_pdf(f, "DSP-1.pdf")

    print("ChromaDB connected successfully.")
    print("Ingested chunks:", count)

    question = "What is sampling?"

    answer = ask_gemini(question)

    print("\nQuestion:")
    print(question)

    print("\nGemini answer:")
    print(answer)