# app/api/routes.py

from flask import Blueprint, request, jsonify
from ..agents.orchestrator_agent import run_orchestrator # This will now work

# Create a Blueprint for our main API
main_api_blueprint = Blueprint('main_api', __name__)

@main_api_blueprint.route('/process-query', methods=['POST'])
def process_query():
    """
    Main endpoint to receive a user query and kick off the agent workflow.
    """
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({"error": "Query not provided"}), 400

    query = data['query']
    
    # Call our orchestrator agent
    result = run_orchestrator(query) 
    
    print(f"Orchestrator finished with result: {result}")
    
    return jsonify(result), 200 # Return the final result from the agent

@main_api_blueprint.route('/health', methods=['GET'])
def health_check():
    """A simple health check endpoint."""
    return jsonify({"status": "ok"}), 200

