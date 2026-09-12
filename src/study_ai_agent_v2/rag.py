import functools #Enhances functions (like caching data)
import os #Interacts with your operating system (like reading file paths or API keys)
import re #Matches and manipulates complex text patterns

import chromadb #This gives us the ChromaDB vector database
from chromadb.utils import embedding_functions #This lets ChromaDB use an embedding model
from dotenv import load_dotenv #Python to load values from your .env file
from google import genai
from pypdf import PdfReader #we'll use to extract text from the uploaded PDF

#load_dotenv()

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


if __name__ == "__main__":
    collection = get_collection()

    print("ChromaDB connected successfully.")
    print("Collection:", collection.name)