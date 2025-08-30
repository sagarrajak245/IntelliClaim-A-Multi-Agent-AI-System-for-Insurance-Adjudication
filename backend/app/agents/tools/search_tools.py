# app/agents/tools/search_tools.py

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

class SimpleSearchToolInput(BaseModel):
    """Input schema for SimpleSearchTool."""
    document: str = Field(..., description="The document text to search within")
    search_query: str = Field(..., description="The search term to look for in the document")

class SimpleSearchTool(BaseTool):
    name: str = "Simple Search Tool"
    description: str = "A simple tool to search for keywords in a provided text block (document)."
    args_schema: Type[BaseModel] = SimpleSearchToolInput

    def _run(self, document: str, search_query: str) -> str:
        """
        Searches for a query within a document and returns relevant snippets.
        
        Args:
            document: The text document to search within
            search_query: The term to search for
            
        Returns:
            str: Relevant lines from the document containing the search query
        """
        if not document:
            return "Error: No document was provided to search within."
        
        if not search_query:
            return "Error: No search query was provided."
        
        found_lines = []
        lines = document.split('\n')
        
        for i, line in enumerate(lines):
            if search_query.lower() in line.lower():
                # Include some context around the found line
                context_start = max(0, i-1)
                context_end = min(len(lines), i+2)
                context_lines = lines[context_start:context_end]
                found_lines.extend(context_lines)
        
        if not found_lines:
            return f"No information found for '{search_query}' in the document."
        
        # Remove duplicates while preserving order
        unique_lines = []
        for line in found_lines:
            if line not in unique_lines:
                unique_lines.append(line)
                
        return "\n".join(unique_lines)