# Mindful Companion - System Architecture

## 1. Overview
A full-stack mental health companion featuring mood tracking, guided breathing, and an AI-driven empathetic chat interface.

## 2. Tech Stack
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Backend:** Python (FastAPI)
- **AI Integration:** Google Gemini API (or OpenAI) for empathetic conversation.
- **State Management:** LocalStorage (Frontend) & SQLite/PostgreSQL (Backend).
- **Configuration:** Streamlit (For API management and developer dashboard).

## 3. Data Flow
1. **User Interaction:** User inputs mood or chat message via the `index.html` interface.
2. **API Request:** `script.js` sends a Fetch request to the FastAPI endpoint.
3. **Processing:** FastAPI retrieves the API key (from environment variables set via Streamlit) and queries the LLM.
4. **Response:** The LLM's empathetic response is sent back to the frontend and rendered in the chat window.

## 4. Security
- API Keys are never hardcoded.
- Keys are loaded from a `.env` file or Streamlit secrets.
- Input sanitization on all chat endpoints.