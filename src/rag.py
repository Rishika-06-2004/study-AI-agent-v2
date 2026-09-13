import re #Matches and manipulates complex text patterns
import os

import chromadb #This gives us the ChromaDB vector database
from chromadb.utils import embedding_functions #This lets ChromaDB use an embedding model
from dotenv import load_dotenv #Python to load values from your .env file
from google import genai

from loaders import extract_text

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


def ingest_file(source, filename):

    #Gets/opens our ChromaDB collection where we will store the PDF chunks
    collection = get_collection()

    text = extract_text(source, filename)
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
    metadatas = results["metadatas"][0]

    chunks = []

    for document, metadata in zip(documents, metadatas):

        chunks.append(
            {
                "text": document,
                "source": metadata["source_file"]
            }
        )

    return chunks


def _genai_client():
    return genai.Client(api_key=os.environ["GEMINI_API_KEY"])
