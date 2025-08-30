# # app/agents/orchestrator_agent.py

# import os
# import json
# from crewai import Agent, Task, Crew, Process
# from langchain_groq import ChatGroq

# from ..config.settings import GROQ_API_KEY
# from ..socket_setup import emit_agent_update
# from .tools.search_tools import SimpleSearchTool

# # --- 1. Initialize the LLM ---
# llm = ChatGroq(
#     api_key=GROQ_API_KEY,
#     model="groq/llama-3.3-70b-versatile", 
#     temperature=0.0
# )

# # --- 2. Initialize the Tool ---
# search_tool = SimpleSearchTool()

# # --- 3. Define the Agents ---

# query_understanding_agent = Agent(
#     role="Insurance Query Analyst",
#     goal="""Accurately extract key entities from a user's insurance query and format them into a strict JSON object.""",
#     backstory="""You are an expert NLP agent specialized in insurance domain analysis. You are meticulous and precise and ONLY output valid JSON.""",
#     llm=llm,
#     verbose=True,
#     allow_delegation=False
# )

# document_retrieval_agent = Agent(
#     role="Document Retrieval Specialist",
#     goal="""Search insurance policy documents to find relevant information using the Simple Search Tool.""",
#     backstory="""You are a document search specialist. You must use the Simple Search Tool with proper string inputs to find relevant policy information.""",
#     llm=llm,
#     tools=[search_tool],
#     verbose=True,
#     allow_delegation=False
# )

# # --- 4. Define the Tasks ---

# query_analysis_task = Task(
#     description="""Analyze the following user query: '{query}'. 
    
#     Extract all relevant entities and return them as a JSON object with these fields:
#     - age: user's age (if mentioned)
#     - location: user's location (if mentioned) 
#     - medical_procedure: the medical procedure needed
#     - policy_age: how long they've had the policy
#     - additional_context: any other relevant information
    
#     Example output:
#     {
#         "age": 46,
#         "location": "Pune",
#         "medical_procedure": "knee surgery",
#         "policy_age": "3 months",
#         "additional_context": "User needs surgery coverage"
#     }""",
#     expected_output="""A valid JSON object containing the extracted entities. ONLY return the JSON, no additional text.""",
#     agent=query_understanding_agent
# )

# document_search_task = Task(
#     description="""You must search the insurance policy document using the Simple Search Tool.
    
#     IMPORTANT INSTRUCTIONS:
#     1. Use the Simple Search Tool with these exact parameters:
#        - document: pass the full document text as a string
#        - search_query: pass the medical procedure as a string (e.g., "knee surgery")
    
#     2. The document text is: '{document}'
    
#     3. From the previous agent's analysis, extract the medical procedure and search for it.
    
#     4. Example tool usage:
#        Action: Simple Search Tool
#        Action Input: {{"document": "Insurance Policy Document text...", "search_query": "knee surgery"}}
    
#     5. Analyze the search results to determine coverage eligibility.""",
#     expected_output="""A clear summary of the relevant policy information found, including:
#     - The specific policy terms that apply
#     - Waiting periods or restrictions
#     - Coverage eligibility based on the user's situation""",
#     agent=document_retrieval_agent,
#     context=[query_analysis_task]
# )

# # Add a synthesis agent for better final output
# synthesis_agent = Agent(
#     role="Insurance Advisor",
#     goal="Provide clear, actionable advice about insurance coverage based on policy analysis.",
#     backstory="You are an insurance expert who explains policy terms in simple language and provides clear recommendations.",
#     llm=llm,
#     verbose=True,
#     allow_delegation=False
# )

# synthesis_task = Task(
#     description="""Based on the user query analysis and document search results, provide a comprehensive answer.
    
#     The original query was: '{query}'
    
#     Provide:
#     1. Direct answer about coverage eligibility
#     2. Explanation of relevant policy terms
#     3. Clear recommendation or next steps
#     4. Timeline information if applicable""",
#     expected_output="""A clear, helpful response that directly answers the user's question about their insurance coverage.""",
#     agent=synthesis_agent,
#     context=[query_analysis_task, document_search_task]
# )

# # --- 5. Create the Crew ---
# query_crew = Crew(
#     agents=[query_understanding_agent, document_retrieval_agent, synthesis_agent],
#     tasks=[query_analysis_task, document_search_task, synthesis_task],
#     process=Process.sequential,
#     verbose=True
# )

# # --- 6. Update the Main Orchestrator Function ---
# def run_orchestrator(query: str):
#     print(f"Orchestrator starting workflow for query: {query}")
#     emit_agent_update("Orchestrator", "processing", f"Query received. Starting multi-agent workflow...")

#     dummy_document = """Insurance Policy Document - HealthPlus Plan
# Section 1: General Coverage
# - All standard procedures are covered after a 30-day waiting period.
# Section 2: Special Procedures  
# - Coverage for specialized surgeries, including knee surgery, requires a 6-month waiting period from the policy start date.
# - Cardiac procedures have a 12-month waiting period.
# Section 3: Exclusions
# - Pre-existing conditions are not covered for the first 24 months."""

#     inputs = {
#         'query': query,
#         'document': dummy_document
#     }
    
#     try:
#         crew_result = query_crew.kickoff(inputs=inputs)
#         final_answer = crew_result

#         emit_agent_update(
#             "Workflow Complete",
#             "complete",
#             str(final_answer)
#         )

#         print(f"Orchestrator finished with result: {final_answer}")
#         return {
#             "final_answer": final_answer
#         }
    
#     except Exception as e:
#         error_msg = f"Error in orchestrator workflow: {str(e)}"
#         print(error_msg)
#         emit_agent_update("Orchestrator", "error", error_msg)
#         return {
#             "error": error_msg,
#             "final_answer": "An error occurred while processing your query. Please try again."
#         } 

# app/agents/orchestrator_agent.py

import os
import json
from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq

from ..config.settings import GROQ_API_KEY
from ..socket_setup import emit_agent_update
from .tools.search_tools import SimpleSearchTool 

# --- 1. Initialize the LLM ---
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="groq/llama-3.3-70b-versatile",
    temperature=0.0
)

# --- 2. Initialize the Tool ---
search_tool = SimpleSearchTool()

# --- 3. Define the Agents ---

query_understanding_agent = Agent(
    role="Insurance Query Analyst",
    goal="""Accurately extract key entities from a user's insurance query and format them into a strict JSON object.""",
    backstory="""You are an expert NLP agent specialized in insurance domain analysis. You are meticulous and precise and ONLY output valid JSON.""",
    llm=llm,
    verbose=True,
    allow_delegation=False
)

document_retrieval_agent = Agent(
    role="Document Retrieval Specialist",
    goal="""Search insurance policy documents to find relevant information using the Simple Search Tool.""",
    backstory="""You are a document search specialist. You must use the Simple Search Tool with proper string inputs to find relevant policy information.""",
    llm=llm,
    tools=[search_tool],
    verbose=True,
    allow_delegation=False
)

synthesis_agent = Agent(
    role="Insurance Advisor",
    goal="Provide clear, actionable advice about insurance coverage based on policy analysis.",
    backstory="You are an insurance expert who explains policy terms in simple language and provides clear recommendations.",
    llm=llm,
    verbose=True,
    allow_delegation=False
)

# --- 4. Define the Tasks ---

query_analysis_task = Task(
    description="""Analyze the following user query: '{query}'. 
    
    Extract all relevant entities and return them as a JSON object with these fields:
    - age: user's age (if mentioned)
    - location: user's location (if mentioned) 
    - medical_procedure: the medical procedure needed
    - policy_age: how long they've had the policy
    - additional_context: any other relevant information
    
    Example output:
    {{
        "age": 46,
        "location": "Pune",
        "medical_procedure": "knee surgery",
        "policy_age": "3 months",
        "additional_context": "User needs surgery coverage"
    }}""",
    expected_output="""A valid JSON object containing the extracted entities. ONLY return the JSON, no additional text.""",
    agent=query_understanding_agent
)

document_search_task = Task(
    description="""You must search the insurance policy document using the Simple Search Tool.
    
    IMPORTANT INSTRUCTIONS:
    1. Use the Simple Search Tool with these exact parameters:
       - document: pass the full document text as a string
       - search_query: pass the medical procedure as a string (e.g., "knee surgery")
    
    2. The document text is: '{document}'
    
    3. From the previous agent's analysis, extract the medical procedure and search for it.
    
    4. Example tool usage:
       Action: Simple Search Tool
       Action Input: {{"document": "Insurance Policy Document text...", "search_query": "knee surgery"}}
    
    5. Analyze the search results to determine coverage eligibility.""",
    expected_output="""A clear summary of the relevant policy information found, including:
    - The specific policy terms that apply
    - Waiting periods or restrictions
    - Coverage eligibility based on the user's situation""",
    agent=document_retrieval_agent,
    context=[query_analysis_task]
)

synthesis_task = Task(
    description="""Based on the user query analysis and document search results, provide a comprehensive answer.
    
    The original query was: '{query}'
    
    Provide:
    1. Direct answer about coverage eligibility
    2. Explanation of relevant policy terms
    3. Clear recommendation or next steps
    4. Timeline information if applicable""",
    expected_output="""A clear, helpful response that directly answers the user's question about their insurance coverage.""",
    agent=synthesis_agent,
    context=[query_analysis_task, document_search_task]
)

# --- 5. Create the Crew ---
query_crew = Crew(
    agents=[query_understanding_agent, document_retrieval_agent, synthesis_agent],
    tasks=[query_analysis_task, document_search_task, synthesis_task],
    process=Process.sequential,
    verbose=True
)

# --- 6. Update the Main Orchestrator Function ---
def run_orchestrator(query: str):
    print(f"Orchestrator starting workflow for query: {query}")
    emit_agent_update("Orchestrator", "processing", f"Query received. Starting multi-agent workflow...")

    dummy_document = """Insurance Policy Document - HealthPlus Plan
Section 1: General Coverage
- All standard procedures are covered after a 30-day waiting period.
Section 2: Special Procedures  
- Coverage for specialized surgeries, including knee surgery, requires a 6-month waiting period from the policy start date.
- Cardiac procedures have a 12-month waiting period.
Section 3: Exclusions
- Pre-existing conditions are not covered for the first 24 months."""

    inputs = {
        'query': query,
        'document': dummy_document
    }
    
    try:
        crew_result = query_crew.kickoff(inputs=inputs)
        
        # --- THIS IS THE FIX ---
        # We extract the final raw string from the CrewOutput object.
        final_answer = crew_result.raw

        emit_agent_update(
            "Workflow Complete",
            "complete",
            str(final_answer)
        )

        print(f"Orchestrator finished with result: {final_answer}")
        return {
            "final_answer": final_answer
        }
    
    except Exception as e:
        error_msg = f"Error in orchestrator workflow: {str(e)}"
        print(error_msg)
        emit_agent_update("Orchestrator", "error", error_msg)
        return {
            "error": error_msg,
            "final_answer": "An error occurred while processing your query. Please try again."
        }

