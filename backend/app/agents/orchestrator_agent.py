

import os
import json
from crewai import Agent, Task, Crew, Process 
from langchain_groq import ChatGroq 

from ..config.settings import GROQ_API_KEY
from ..socket_setup import emit_agent_update
from ..utils.document_processor import create_vector_store_from_pdf
from .tools.search_tool import VectorSearchTool

# --- 1. Initialize the LLM ---
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="groq/llama-3.3-70b-versatile",
    temperature=0.0
)

# --- 2. Initialize the Vector Search Tool ---
search_tool = VectorSearchTool()

# --- 3. Enhanced RAG Pipeline Initialization ---
def initialize_rag_pipeline(pdf_path: str = "policy_document.pdf") -> bool:
    """
    Initialize the RAG pipeline with better error handling.
    """
    try:
        print("--- Initializing RAG Pipeline... ---")
        
        # Create dummy PDF if it doesn't exist
        if not os.path.exists(pdf_path):
            print(f"Creating dummy PDF at: {pdf_path}")
            _create_dummy_pdf(pdf_path)
        
        # Create vector store
        create_vector_store_from_pdf(pdf_path)
        print("--- RAG Pipeline Initialized Successfully! ---")
        return True
        
    except Exception as e:
        print(f"--- ERROR Initializing RAG Pipeline: {e} ---")
        return False

def _create_dummy_pdf(pdf_path: str) -> None:
    """Create a dummy insurance policy PDF."""
    try:
        from fpdf import FPDF
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        dummy_document_text = """
        Insurance Policy Document - HealthPlus Plan
        
        Section 1: General Coverage
        - All standard procedures are covered after a 30-day waiting period.
        - Emergency procedures covered immediately.
        
        Section 2: Special Procedures
        - Coverage for specialized surgeries, including knee surgery, requires a 6-month waiting period from the policy start date.
        - Cardiac procedures have a 12-month waiting period.
        - Dental procedures require 3-month waiting period.
        
        Section 3: Exclusions
        - Pre-existing conditions are not covered for the first 24 months.
        - Cosmetic procedures are not covered unless medically necessary.
        """
        
        pdf.multi_cell(0, 10, dummy_document_text)
        pdf.output(pdf_path)
        
    except Exception as e:
        print(f"Error creating dummy PDF: {str(e)}")
        raise

# --- 4. Improved Agent Definitions ---

query_understanding_agent = Agent(
    role="Insurance Query Analyst",
    goal="""Extract the core medical procedure or coverage question from user queries and create effective search terms.""",
    backstory="""You are an experienced insurance analyst who specializes in understanding customer queries. 
    You have deep knowledge of medical terminology and insurance language. Your job is to identify exactly what 
    the customer is asking about and convert it into search terms that will find the right policy information.""",
    llm=llm,
    verbose=True,
    allow_delegation=False
)

document_retrieval_agent = Agent(
    role="Document Retrieval Specialist",
    goal="""Use semantic vector search to find all relevant policy information that relates to the user's query.""",
    backstory="""You are a skilled document search specialist with expertise in insurance policies. 
    You use advanced semantic search to find not just exact matches, but related concepts and clauses 
    that might affect coverage decisions. You always ensure comprehensive information retrieval.""",
    llm=llm,
    tools=[search_tool],
    verbose=True,
    allow_delegation=False
)

decision_making_agent = Agent(
    role="Insurance Coverage Adjudicator",
    goal="""Make clear coverage decisions based on policy analysis and provide detailed explanations with specific reasoning.""",
    backstory="""You are an experienced insurance adjudicator with extensive knowledge of policy interpretation. 
    You make fair, consistent decisions based on policy terms and always explain your reasoning clearly. 
    You consider all relevant factors including waiting periods, exclusions, and policy age to make accurate determinations.""",
    llm=llm,
    verbose=True,
    allow_delegation=False
)

# --- 5. Improved Task Definitions ---

query_analysis_task = Task(
    description="""Analyze the user query: '{query}'. 
    
    Extract the main medical procedure or coverage question and create an effective search query.
    Consider synonyms and related terms that might appear in policy documents.""",
    expected_output="""A focused search query that will find relevant policy information. 
    Examples: 'knee surgery coverage', 'cardiac procedure waiting period', 'dental treatment eligibility'""",
    agent=query_understanding_agent
)

document_search_task = Task(
    description="""Use the 'Semantic Vector Search' tool with the refined query from the previous step.
    
    Find all relevant policy sections including:
    - Coverage rules and requirements
    - Waiting periods
    - Exclusions or limitations
    - Any related provisions""",
    expected_output="""Complete policy information relevant to the query, including coverage rules, 
    waiting periods, exclusions, and any other applicable terms.""",
    agent=document_retrieval_agent,
    context=[query_analysis_task]
)

decision_making_task = Task(
    description="""Based on the user query: '{query}' and the retrieved policy information, 
    make a coverage determination.
    
    Provide:
    1. Clear decision (APPROVED/DENIED/CONDITIONAL)
    2. Specific reasoning based on policy terms
    3. Next steps for the user
    4. Timeline information if applicable""",
    expected_output="""A comprehensive coverage decision with:
    - Clear APPROVED/DENIED/CONDITIONAL status
    - Detailed reasoning based on specific policy provisions
    - Actionable next steps for the policyholder
    - Any relevant timeline or waiting period information""",
    agent=decision_making_agent,
    context=[query_analysis_task, document_search_task]
)

# --- 6. Create the Crew (Fixed) ---
query_crew = Crew(
    agents=[query_understanding_agent, document_retrieval_agent, decision_making_agent],
    tasks=[query_analysis_task, document_search_task, decision_making_task],
    process=Process.sequential,
    verbose=True
    # Removed embedder config that was causing the error
)

# --- 7. Enhanced Main Orchestrator Function ---
def run_orchestrator(query: str):
    """Execute the insurance query processing workflow."""
    
    # Basic input validation
    if not query or not query.strip():
        error_msg = "Empty query provided"
        print(error_msg)
        return {"error": error_msg, "final_answer": "Please provide a valid insurance query."}
    
    query = query.strip()
    print(f"Orchestrator starting workflow for query: {query}")
    emit_agent_update("Orchestrator", "processing", "Query received. Starting multi-agent RAG workflow...")

    try:
        # Execute workflow
        crew_result = query_crew.kickoff(inputs={'query': query})
        final_answer = crew_result.raw

        # Validate result
        if not final_answer or not final_answer.strip():
            raise ValueError("Empty result from workflow")

        emit_agent_update("Workflow Complete", "complete", str(final_answer))
        print(f"Orchestrator finished with result: {final_answer}")
        
        return {
            "final_answer": final_answer,
            "status": "success"
        } 
         
    except Exception as e:
        error_msg = f"Error in orchestrator workflow: {str(e)}"
        print(error_msg)
        emit_agent_update("Orchestrator", "error", error_msg)
        return {
            "error": error_msg, 
            "final_answer": "An error occurred while processing your query. Please try again."
        }