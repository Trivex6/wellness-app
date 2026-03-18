import streamlit as st
import streamlit.components.v1 as components
from groq import Groq

# 1. Page Configuration
st.set_page_config(
    page_title="Serenity Wellness",
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 2. Groq AI Engine Setup
# Ensure GROQ_API_KEY is in your Streamlit Secrets!
api_key = st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

def get_serenity_response(user_text):
    if not client: return "System: Groq API Key is missing! 💙"
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are Serenity, a kind mental health assistant. Give very brief, warm, supportive advice."},
                {"role": "user", "content": user_text}
            ],
            model="llama3-8b-8192",
            temperature=0.7,
            max_tokens=150
        )
        reply = chat_completion.choices[0].message.content
        # Escape characters that break JavaScript strings
        return reply.replace("`", "'").replace("\\", "/").replace("\n", " ")
    except Exception as e:
        return f"Serenity is resting: {str(e)}"

# 3. DIRECT QUERY BRIDGE
ai_final_reply = ""
# We use .get() to avoid the 'NoneType' error from your screenshot
user_query = st.query_params.get("msg")

if user_query:
    ai_final_reply = get_serenity_response(user_query)
    # Clear the parameter so the next page refresh is clean
    st.query_params.clear()

# 4. File Loader
def load_frontend(reply_from_ai):
    try:
        with open("index.html", "r", encoding="utf-8") as f: html = f.read()
        with open("style.css", "r", encoding="utf-8") as f: css = f.read()
        with open("script.js", "r", encoding="utf-8") as f: js = f.read()
        
        return f"""
        <!DOCTYPE html>
        <html>
            <head><style>{css}</style></head>
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
        return f"<div style='color:white; padding:20px;'>File Error: {e}</div>"

# 5. UI Cleanup (Removes Streamlit's default headers)
st.markdown("""
    <style>
    header, footer, #MainMenu {visibility: hidden; display: none;}
    .block-container { padding: 0rem !important; margin: 0rem !important; }
    .stApp { background-color: #0f172a; }
    iframe { width: 100vw !important; height: 100vh !important; border: none; }
    </style>
    """, unsafe_allow_html=True)

# 6. Render
components.html(load_frontend(ai_final_reply), height=1000, scrolling=False)
