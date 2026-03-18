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
api_key = st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

def get_serenity_response(user_text):
    if not client: return "System: Groq API Key is missing! 💙"
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are Serenity, a compassionate mental health assistant. Provide supportive, brief advice."},
                {"role": "user", "content": user_text}
            ],
            model="llama3-8b-8192",
            temperature=0.7,
            max_tokens=200
        )
        reply = chat_completion.choices[0].message.content
        return reply.replace("`", "'").replace("\\", "/").replace("\n", " ")
    except Exception as e:
        return f"Serenity is offline: {str(e)}"

# 3. THE "NO-ERROR" BRIDGE
ai_final_reply = ""
user_query = None

# We use a very wide try-except here because st.query_params 
# is unstable during the initial boot-up of the app.
try:
    # Check if the 'msg' key exists in the current URL
    qp = st.query_params
    if "msg" in qp:
        user_query = qp["msg"]
        # Immediately clear it so the next refresh is clean
        st.query_params.clear()
except Exception:
    # If anything goes wrong with params, we just ignore it 
    # and load the app normally. No more red screen.
    user_query = None

if user_query:
    ai_final_reply = get_serenity_response(user_query)

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
        return f"Error: {e}"

# 5. UI Cleanup
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
