# app/main.py

import os
from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS
from .socket_setup import socketio
from .api.routes import main_api_blueprint
from .agents.orchestrator_agent import initialize_rag_pipeline


def create_app():
    load_dotenv()
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    socketio.init_app(app)
    print("✅ Socket.IO initialized.")

    app.register_blueprint(main_api_blueprint, url_prefix='/api/v1')
    print("✅ API routes registered.")

    # Initialize the RAG Pipeline and Vector DB
    initialize_rag_pipeline()
    

    @app.route('/')
    def index():
        return "IntelliClaim Agent Server is running!"
        
    return app

