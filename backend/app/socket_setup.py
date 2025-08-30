 
from flask_socketio import SocketIO

# Initialize SocketIO. We'll attach it to the Flask app in main.py
# We allow all origins for development purposes. In production, you'd restrict this.
socketio = SocketIO(cors_allowed_origins="*")
  
def emit_agent_update(agent_name, status, result):
    """
    A helper function to emit real-time updates to the frontend. 
    This will be called by our agents during their process.
    """
    print(f"📢 Emitting update: Agent={agent_name}, Status={status}, Result={result}")
    socketio.emit('agent_update', {
        'agent': agent_name,
        'status': status,
        'result': result,
    })

  