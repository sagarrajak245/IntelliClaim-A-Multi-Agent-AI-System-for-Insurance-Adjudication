import { create } from 'zustand';

// Define the initial state of our agents
const initialAgentState = {
    "Orchestrator": { status: "pending", result: "" },
    "Query Understanding Agent": { status: "pending", result: "" },
    "Document Retrieval Specialist": { status: "pending", result: "" },
    "Decision Making Agent": { status: "pending", result: "" },
};

export const useAgentStore = create((set) => ({
    // The query the user has submitted
    query: "",
    // The final answer from the crew
    finalAnswer: null,
    // The current state of all agents
    agents: initialAgentState,
    // Any error messages
    error: null,
    // A flag to indicate if the process is running
    isRunning: false,

    // --- ACTIONS ---

    // Action to start a new query process
    startProcess: (query) => set({
        query,
        finalAnswer: null,
        agents: initialAgentState,
        error: null,
        isRunning: true
    }),

    // Action to update the status of a specific agent
    updateAgent: (agentName, status, result) => set((state) => ({
        agents: {
            ...state.agents,
            [agentName]: { status, result },
        },
    })),

    // Action to set the final answer and stop the process
    setFinalAnswer: (answer) => set({
        finalAnswer: answer,
        isRunning: false
    }),

    // Action to handle any errors from the backend
    setError: (errorMessage) => set({
        error: errorMessage,
        isRunning: false
    }),
}));        