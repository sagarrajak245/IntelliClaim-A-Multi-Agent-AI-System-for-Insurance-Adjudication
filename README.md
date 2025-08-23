🤖 IntelliClaim: A Multi-Agent AI System for Insurance Adjudication
IntelliClaim is a cutting-edge, full-stack application that leverages a sophisticated multi-agent system to automate and revolutionize the insurance claim adjudication process. By combining advanced AI techniques like RAG, NLP, and LLM reasoning, this project demonstrates a production-quality solution for delivering fast, accurate, and fully transparent insurance decisions.

(This is a placeholder: You can replace this with a GIF of your application in action once it's running!)

✨ Key Features
🧠 Advanced Multi-Agent Architecture: Utilizes a team of specialized AI agents, each with a distinct role, to handle complex decision-making workflows.

🚀 Real-Time Processing: A live dashboard visualizes each agent's activity and decision-making process in real-time using WebSockets.

🔍 Explainable AI (XAI): Generates clear, human-readable explanations for every decision, providing full transparency and auditability.

📄 Intelligent Document Retrieval (RAG): Employs Retrieval-Augmented Generation to instantly find and analyze the most relevant clauses from dense policy documents.

💬 Natural Language Understanding (NLP): Accepts complex user queries in plain English and extracts structured information for processing.

⚙️ Full-Stack Implementation: A complete solution with a modern React frontend and a robust Python (Flask) backend.

🏗️ Technology Stack
The system is built with a modern, scalable technology stack designed for high-performance AI applications.

Category

Technology

🤖 Backend

Flask, CrewAI/LangGraph (Agent Orchestration), Socket.io, PostgreSQL, Redis

🎨 Frontend

React.js, Vite, Tailwind CSS, Zustand, React Query, Socket.io-client, Framer Motion

🧠 AI/ML

Groq LLMs (Llama, Mixtral), LangChain, spaCy (NLP), ChromaDB (Vector Store), Sentence Transformers

🚀 Getting Started
Follow these instructions to get a local copy of the project up and running for development and testing.

Prerequisites
Node.js (v18 or higher)

Python (v3.10 or higher)

A free API key from Groq

Backend Setup
Navigate to the backend directory:

cd multi-agent-backend

Create and activate a Python virtual environment:

python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

Install the required dependencies:

pip install -r requirements.txt
python -m spacy download en_core_web_sm

Set up your environment variables:

Create a .env file in the multi-agent-backend root.

Add your Groq API key: GROQ_API_KEY="your_api_key_here"

Run the Flask server:

flask --app app/main.py run

Frontend Setup
Navigate to the frontend directory:

cd multi-agent-frontend

Install the required dependencies:

npm install

Run the development server:

npm run dev

The application will be available at http://localhost:5173.

🏛️ Architecture Overview
The project is built on a multi-agent system where specialized AI agents collaborate to solve a complex problem.

Orchestrator Agent: The master controller that manages the workflow.

Query Understanding Agent: Extracts entities and intent from user queries.

Document Retrieval Agent: Finds relevant information from policy documents using RAG.

Business Rules Agent: Enforces insurance-specific logic.

Decision Making Agent: Synthesizes all information to make a reasoned decision.

And more... (QA, Response Generation, Audit Trail)

This modular, agent-based approach makes the system highly scalable, maintainable, and easy to extend with new capabilities.

🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

📄 License
This project is licensed under the MIT License. See the LICENSE file for details.
