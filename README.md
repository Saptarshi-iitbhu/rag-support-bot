# AI Customer Support Bot

An AI-powered customer support agent that simulates support interactions, handles FAQs using a RAG (Retrieval-Augmented Generation) approach, maintains conversational context, and simulates escalation.

## Features

- **Hybrid Response Engine**:
- **FAQ Lookup**: Uses TF-IDF and Cosine Similarity to find answers from the `MakTek/Customer_support_faqs_dataset` on HuggingFace.
- **LLM Fallback**: Uses OpenAI (GPT-3.5) to generate context-aware responses if no FAQ match is found, incorporating retrieved FAQ context.
- **Contextual Memory**: Remembers previous interactions within a session.
- **Escalation Simulation**: Detects when to escalate queries to a human agent based on sentiment and keywords.
- **Session Management**: Persists chat sessions using SQLite and local storage.
- **Modern UI**: Responsive, dark-themed chat interface built with React.

## Tech Stack

- **Backend**: Python, FastAPI, SQLAlchemy, SQLite, scikit-learn, pandas, datasets
- **Frontend**: React, Vite, Tailwind CSS
- **AI**: OpenAI API, HuggingFace Datasets

## Setup Instructions

### Prerequisites
- Node.js & npm
- Python 3.x
- OpenAI API Key

### Backend Setup
1. Navigate to the `server` directory:
```bash
cd server
```
2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Configure Environment:
- The project uses a `.env` file for configuration.
- Open `.env` and add your `OPENAI_API_KEY`:
```env
OPENAI_API_KEY=sk-your-api-key-here
DATABASE_URL=sqlite:///./chat_sessions.db
```
5. Run the server:
```bash
uvicorn app.main:app --reload
```
The API will be available at `http://localhost:8000`.

### Frontend Setup
1. Navigate to the `client` directory:
```bash
cd client
```
2. Install dependencies:
```bash
npm install
```
3. Run the development server:
```bash
npm run dev
```
The app will be available at `http://localhost:5173`.

## Usage

1. Open the frontend URL in your browser.
2. Type a question (e.g., "How do I reset my password?").
3. The bot will first check the FAQ dataset.
4. If no direct match is found, it will use the LLM to generate a helpful response.
5. If the bot cannot help or you express frustration, it will trigger an "escalation" action (visible in the console/network response).

## Project Structure

```
.
├── client/ # React Frontend
│ ├── src/
│ │ ├── components/ # ChatInterface.jsx
│ │ └── styles/ # index.css
├── server/ # FastAPI Backend
│ ├── app/
│ │ ├── routers/ # API Routes (chat.py)
│ │ ├── services/ # Logic Layer
│ │ │ ├── faq_engine.py # TF-IDF Search & Dataset loading
│ │ │ └── llm_service.py # OpenAI integration & Orchestration
│ │ ├── database.py # DB Connection
│ │ └── models.py # SQLAlchemy Models
│ ├── main.py # App Entrypoint
│ └── requirements.txt # Python Dependencies
└── README.md
```
## Preview Video
[Preview Video.mp4](https://github.com/Saptarshi-iitbhu/rag-support-bot/blob/main/Preview%20Video.mp4)
