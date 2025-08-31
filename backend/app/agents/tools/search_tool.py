# app/agents/tools/vector_search_tool.py

from crewai.tools import BaseTool
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings 

# Use the same configuration as the document processor
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
VECTOR_DB_PATH = "./chroma_db"  

class VectorSearchTool(BaseTool):
    name: str = "Semantic Vector Search"
    description: str = "Performs a semantic search on the insurance policy vector database to find the most relevant information based on the query's meaning."

    def _run(self, search_query: str) -> str:
        """
        Performs a semantic search in the ChromaDB vector store.
        """
        print(f"--- Performing vector search for: '{search_query}' ---")
        
        # Initialize the embedding model
        embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'}
        )
        
        # Load the persisted vector store
        vector_store = Chroma(
            persist_directory=VECTOR_DB_PATH,
            embedding_function=embeddings
        )

        # Perform the similarity search
        results = vector_store.similarity_search(search_query, k=3) # Get top 3 results

        if not results:
            return "No relevant information found in the document."

        # Format the results into a single string
        result_string = ""
        for doc in results:
            result_string += f"Source: {doc.metadata.get('source', 'Unknown')}, Page: {doc.metadata.get('page', 'N/A')}\n"
            result_string += f"Content: {doc.page_content}\n---\n"
            
        return result_string

