import streamlit as st
import streamlit.components.v1 as components
import os
from groq import Groq

# 1. Page Configuration
st.set_page_config(
    page_title="Serenity Wellness",
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 2. Groq AI Engine Setup
# Ensure GROQ_API_KEY is in Streamlit Cloud > Settings > Secrets
api_key = st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

def get_serenity_response(user_text):
    if not client:
        return "System: Groq API Key is missing! 💙"
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are Serenity, a compassionate mental health assistant. Provide supportive, brief, and helpful advice. Stay concise."
                },
                {"role": "user", "content": user_text}
            ],
            model="llama3-8b-8192",
            temperature=0.7,
            max_tokens=200
        )
        # Clean response for JS safety
        reply = chat_completion.choices[0].message.content
        return reply.replace("`", "'").replace("\\", "/").replace("\n", " ")
    except Exception as e:
        return f"Serenity is offline: {str(e)}"

# 3. The Bridge: Catching messages from the JS via URL
# Using the most stable direct access method
user_query = st.query_params.get("msg")
ai_final_reply = ""

if user_query:
    ai_final_reply = get_serenity_response(user_query)
    # Clear parameters to prevent refresh loops
    st.query_params.clear()

# 4. File Loader
def load_frontend(reply_from_ai):
    try:
        # These files must exist in your GitHub repo
        with open("index.html", "r", encoding="utf-8") as f: html = f.read()
        with open("style.css", "r", encoding="utf-8") as f: css = f.read()
        with open("script.js", "r", encoding="utf-8") as f: js = f.read()

        # Passing the AI reply into the global JS variable 'window.SERENITY_REPLY'
        return f"""
        <!DOCTYPE html>
        <html>
            <head>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>{css}</style>
            </head>
            <body>
                {html}
                <script>
                    window.SERENITY_REPLY = `{reply_from_ai}`;
                    {js}
                </script>
            </body>
        </html>
        """
    except Exception as e:
        return f"<h2 style='color:white;'>Error Loading Files: {e}</h2>"

# 5. UI Cleanup (Removes Streamlit's default padding/header)
st.markdown("""
    <style>
    header, footer, #MainMenu {visibility: hidden; display: none;}
    .block-container {
        padding: 0rem !important;
        margin: 0rem !important;
        max-width: 100% !important;
    }
    .stApp { background-color: #0f172a; }
    iframe { width: 100vw !important; height: 100vh !important; border: none; }
    </style>
    """, unsafe_allow_html=True)

# 6. Render Dashboard
components.html(load_frontend(ai_final_reply), height=1000, scrolling=False)
