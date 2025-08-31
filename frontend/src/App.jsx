import { useEffect, useState } from 'react';
import AgentDashboard from './components/dashboard/AgentDashboard';
import socketService from './services/socketService';
import { useAgentStore } from './store/agentStore';

function App() {
  const [query, setQuery] = useState("");
  const { finalAnswer, isRunning, error } = useAgentStore();

  // Establish the socket connection when the component mounts
  useEffect(() => {
    socketService.connect();
    // Clean up the connection when the component unmounts
    return () => {
      if (socketService.socket) {
        socketService.socket.disconnect();
      }
    };
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim() && !isRunning) {
      socketService.processQuery(query);
    }
  };

  return (
    <div className="bg-gray-900 text-white min-h-screen p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        <header className="text-center mb-8">
          <h1 className="text-4xl md:text-5xl font-bold">
            IntelliClaim <span className="text-blue-400">AI</span>
          </h1>
          <p className="text-gray-400 mt-2">
            Your Multi-Agent System for Insurance Adjudication
          </p>
        </header>

        <main>
          <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
            <form onSubmit={handleSubmit}>
              <textarea
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Enter your insurance query here... (e.g., 'A 46-year-old client in Pune had knee surgery...')"
                className="w-full p-3 bg-gray-700 rounded border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
                rows="4"
                disabled={isRunning}
              />
              <button
                type="submit"
                className={`mt-4 w-full py-3 px-4 rounded font-bold text-white transition ${isRunning ? 'bg-gray-600 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'
                  }`}
                disabled={isRunning}
              >
                {isRunning ? 'Processing...' : 'Process Query'}
              </button>
            </form>
          </div>

          <AgentDashboard />

          {error && (
            <div className="mt-6 bg-red-900 border border-red-700 text-red-200 p-4 rounded-lg">
              <h3 className="font-bold">An Error Occurred</h3>
              <p>{error}</p>
            </div>
          )}

          {finalAnswer && (
            <div className="mt-6 bg-gray-800 p-6 rounded-lg shadow-lg">
              <h2 className="text-2xl font-bold text-white mb-4">Final Answer</h2>
              <div className="prose prose-invert max-w-none whitespace-pre-wrap">
                {finalAnswer}
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default App;    
