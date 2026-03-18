import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv

# Import the database functions from your database.py file
from database import init_db, save_mood

# Load environment variables (API keys) set by your Streamlit dashboard
load_dotenv()

app = FastAPI(title="Mindful Companion API")

# Initialize the SQLite database on startup
init_db()

# CORS configuration: This allows your HTML file to talk to this Python server
# Essential for development when running on localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],
)

# --- Data Models for API Requests ---

class ChatRequest(BaseModel):
    message: str

class MoodRequest(BaseModel):
    value: int
    note: str

# --- API Endpoints ---

@app.get("/")
async def health_check():
    return {"status": "online", "message": "Mindful Backend is running"}

@app.post("/chat")
async def chat_with_ai(request: ChatRequest):
    """
    Processes user messages using Groq's Llama-3 model.
    The API key is pulled from the environment variable 'GROQ_API_KEY'.
    """
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        raise HTTPException(
            status_code=500, 
            detail="Groq API Key missing. Please set it in the Streamlit Dashboard."
        )

    try:
        client = Groq(api_key=api_key)
        
        # System prompt defines the "personality" of your companion
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system", 
                    "content": (
                        "You are 'Mindful', a kind and empathetic mental health companion. "
                        "Your goal is to provide a safe space for users to express feelings. "
                        "Be supportive, use warm language, and offer gentle mindfulness advice. "
                        "If a user is in a crisis, suggest professional help immediately."
                    )
                },
                {"role": "user", "content": request.message}
            ],
            temperature=0.7,
            max_tokens=1024,
            stream=False,
        )
        
        return {"response": completion.choices[0].message.content}

    except Exception as e:
        print(f"Error in Groq API: {e}")
        raise HTTPException(status_code=500, detail="Error communicating with AI service.")

@app.post("/save-mood")
async def log_user_mood(request: MoodRequest):
    """
    Endpoint to receive mood data from the frontend and save it to SQLite.
    """
    try:
        save_mood(request.value, request.note)
        return {"status": "success", "message": "Mood entry saved to database."}
    except Exception as e:
        print(f"Database Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to save mood data.")

# --- Execution ---

if __name__ == "__main__":
    import uvicorn
    # Start the server on localhost:8000
    uvicorn.run(app, host="127.0.0.1", port=8000)