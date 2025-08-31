import { io } from 'socket.io-client';
import { useAgentStore } from '../store/agentStore';

// The URL of our Flask Socket.IO server
const SERVER_URL = "http://127.0.0.1:5000";

class SocketService {
    socket;

    connect() {
        // Disconnect any existing socket
        if (this.socket) {
            this.socket.disconnect();
        }

        // Connect to the server and set up listeners
        this.socket = io(SERVER_URL, {
            transports: ['websocket'],
        });

        this.socket.on('connect', () => {
            console.log('✅ Frontend connected to IntelliClaim server');
        });

        this.socket.on('disconnect', () => {
            console.log('🔌 Frontend disconnected from IntelliClaim server');
        });

        // This is the most important listener. 
        // It receives real-time updates from the backend agents.
        this.socket.on('agent_update', (data) => {
            console.log('📢 Agent Update Received:', data);
            const { agent, status, result } = data;

            // Update our Zustand store with the new agent status
            useAgentStore.getState().updateAgent(agent, status, result);
        });

        return this.socket;
    }

    // Function to send a query to the backend
    processQuery(query) {
        if (this.socket) {
            console.log(`🚀 Sending query to backend: "${query}"`);
            // Start the process in our state manager
            useAgentStore.getState().startProcess(query);

            // Make the API call to the main endpoint
            fetch(`${SERVER_URL}/api/v1/process-query`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query }),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        // Handle any errors from the main HTTP call
                        useAgentStore.getState().setError(data.error);
                    } else {
                        // Set the final answer in our state manager
                        useAgentStore.getState().setFinalAnswer(data.final_answer);
                    }
                })
                .catch(error => {
                    console.error("Fetch error:", error);
                    useAgentStore.getState().setError("Failed to fetch response from the server.");
                });
        }
    }
}

// Export a singleton instance of the service
const socketService = new SocketService();
export default socketService;
