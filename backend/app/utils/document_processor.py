# app/agents/utils/document_processor.py

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# --- Configuration ---
# We use a free, open-source embedding model that runs locally.
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
VECTOR_DB_PATH = "./chroma_db" # Path to store the vector database

def create_vector_store_from_pdf(pdf_path: str):
    """
    Loads a PDF, splits it into chunks, creates embeddings,
    and stores them in a Chroma vector database.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found at: {pdf_path}")

    print(f"--- Loading PDF: {pdf_path} ---")
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    print("--- Splitting document into chunks ---")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)

    if not chunks:
        raise ValueError("Could not create chunks from the document. Is the PDF empty or corrupted?")
    
    print(f"--- Created {len(chunks)} chunks ---")

    print(f"--- Initializing embedding model: {EMBEDDING_MODEL} ---")
    # This model runs locally and is quite powerful for its size.
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={'device': 'cpu'} # Use CPU for broad compatibility
    )

    print(f"--- Creating and persisting vector store at: {VECTOR_DB_PATH} ---")
    # This creates the vector database from the document chunks and embeddings.
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTOR_DB_PATH
    )

    print("--- Vector store created successfully! ---")   
    return vector_store
