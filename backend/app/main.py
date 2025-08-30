# app/main.py

from flask import Flask
from flask_cors import CORS

# Import configurations and socket setup
from .config.settings import GROQ_API_KEY 
from .socket_setup import socketio
from .api.routes import main_api_blueprint

def create_app():
    """
    Creates and configures the Flask application.
    """
    app = Flask(__name__)
    
    # Enable CORS for all routes, allowing your React frontend to connect.
    CORS(app)

    # A simple check to ensure the API key is loaded
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY not configured. Check your .env file.")
    
    print("✅ Groq API Key loaded successfully.")

    # Initialize Socket.IO with the Flask app
    socketio.init_app(app)
    print("✅ Socket.IO initialized.")

    # Register the API blueprint
    app.register_blueprint(main_api_blueprint, url_prefix='/api/v1')
    print("✅ API routes registered.")

    @app.route("/")
    def index():
        return "<h1>IntelliClaim Agent Server is running!</h1>"

    return app

# This pattern allows us to run the app using `flask run` or a WSGI server like Gunicorn
app = create_app()

if __name__ == '__main__':
    # Running with socketio.run() is crucial for WebSocket support
    socketio.run(app, debug=True, port=5000)

