# Gaming Laptop Advisor Chatbot 🎮💻

A powerful AI chatbot designed to help users find the perfect gaming laptop based on their budget and requirements. Powered by **Google ADK (Agent Development Kit)** and **Gemini 2.5 Flash**, featuring a **Google Search** grounded agent and a stylish **Cyberpunk-themed React frontend**.

## Features

*   **Intelligent Recommendations**: Suggests gaming laptops from a curated selection based on your budget.
*   **Real-time Search**: Integrated **Google Search Grounding** allows the agent to find live prices, new models (e.g., "newest Razer Blade"), and reviews from the web.
*   **Smart Context**: Understands budget queries (e.g., "cheapest", "best") without repetitive questioning.
*   **Cyberpunk UI**: A responsive, neon-styled chat interface built with React and Vite.

## Tech Stack

*   **Backend**: Python, Google ADK, FastAPI, Google Gen AI SDK.
*   **AI Model**: Gemini 2.5 Flash.
*   **Frontend**: React, Vite, CSS (Cyberpunk aesthetic).

## Setup & Running

### Prerequisites
*   Python 3.10+
*   Node.js & npm
*   Google API Key (Get one at [Google AI Studio](https://aistudio.google.com/))

### 1. Backend Setup (Google ADK)

1.  Navigate to the `laptop_advisor` directory (or project root).
2.  Install dependencies (if not already installed):
    ```bash
    pip install google-adk fastapi uvicorn python-dotenv
    ```
3.  Configure Environment Variables:
    *   Open `laptop_advisor/.env`.
    *   Add your API Key: `GOOGLE_API_KEY="AIzaSy..."`.
4.  Run the Backend Server:
    ```bash
    python laptop_advisor/backend_server.py
    ```
    *   The server runs on `http://localhost:8000`.

### 2. Frontend Setup (React)

1.  Navigate to the `web_ui` directory:
    ```bash
    cd web_ui
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Start the Development Server:
    ```bash
    npm run dev
    ```
4.  Open your browser at `http://localhost:5173` to chat!

## Usage

*   **Ask for recommendations**: "I have a budget of $1500."
*   **Find specific models**: "How much is the ASUS TUF F15?"
*   **Get live info**: "What is the newest Alienware laptop available now?" (Uses Google Search)
