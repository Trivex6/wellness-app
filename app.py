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

# 2. Groq AI Engine
# Securely fetch API key from Streamlit Cloud Secrets
api_key = st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

def get_serenity_response(user_text, mood_value):
    if not client:
        return "System: Groq API Key is missing. Check your Streamlit Secrets! 💙"
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"You are Serenity, a compassionate mental health assistant. The user is currently feeling a mood level of {mood_value}/5. Provide supportive, brief, and helpful advice."
                },
                {
                    "role": "user",
                    "content": user_text,
                }
            ],
            model="llama3-8b-8192",
            temperature=0.7,
            max_tokens=200
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Serenity is resting right now. (Error: {str(e)})"

# 3. File Loader Logic
def load_frontend():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            html = f.read()
        with open("style.css", "r", encoding="utf-8") as f:
            css = f.read()
        with open("script.js", "r", encoding="utf-8") as f:
            js = f.read()

        full_code = f"""
        <!DOCTYPE html>
        <html style="margin: 0; padding: 0; height: 100%;">
            <head>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    {css}
                    body {{ 
                        margin: 0; 
                        padding: 0; 
                        background: #0f172a;
                        overflow-x: hidden;
                        height: 100%;
                    }}
                </style>
            </head>
            <body>
                {html}
                <script>{js}</script>
            </body>
        </html>
        """
        return full_code
    except Exception as e:
        return f"<h2 style='color:white;'>Error Loading Files: {e}</h2>"

# 4. Custom CSS to "Kill" Streamlit's default UI borders
st.markdown("""
    <style>
    header, footer, #MainMenu {visibility: hidden; display: none;}
    .block-container {
        padding: 0rem !important;
        margin: 0rem !important;
        max-width: 100% !important;
        width: 100% !important;
    }
    .stApp { background-color: #0f172a; }
    [data-testid="stVerticalBlock"] > div:first-child { padding-top: 0 !important; }
    iframe { width: 100vw !important; height: 100vh !important; border: none; }
    </style>
    """, unsafe_allow_html=True)

# 5. Sidebar - Testing & Configuration
with st.sidebar:
    st.title("🛡️ Serenity Console")
    st.info("Test your Groq connection below:")
    
    test_msg = st.text_input("Talk to Serenity:")
    mood_sim = st.slider("Current Mood (1-5):", 1, 5, 3)
    
    if st.button("Test AI Response"):
        if test_msg:
            with st.spinner("Thinking..."):
                response = get_serenity_response(test_msg, mood_sim)
                st.markdown(f"**Serenity:** {response}")
        else:
            st.warning("Please enter a message first.")

# 6. Render Main App
frontend_content = load_frontend()
components.html(frontend_content, height=1000, scrolling=False)