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
# (Make sure to add GROQ_API_KEY in Streamlit Cloud > Settings > Secrets)
api_key = st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

def get_serenity_response(user_text):
    if not client:
        return "System: Groq API Key is missing in Secrets! 💙"
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are Serenity, a compassionate mental health assistant. Provide supportive, brief, and helpful advice."
                },
                {"role": "user", "content": user_text}
            ],
            model="llama3-8b-8192",
            temperature=0.7,
            max_tokens=200
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Serenity is offline: {str(e)}"

# 3. File Loader
def load_frontend():
    try:
        with open("index.html", "r", encoding="utf-8") as f: html = f.read()
        with open("style.css", "r", encoding="utf-8") as f: css = f.read()
        with open("script.js", "r", encoding="utf-8") as f: js = f.read()

        return f"""
        <!DOCTYPE html>
        <html>
            <head>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>{css}</style>
            </head>
            <body>
                {html}
                <script>{js}</script>
            </body>
        </html>
        """
    except Exception as e:
        return f"<h2 style='color:white;'>Error Loading Files: {e}</h2>"

# 4. CSS Fixes to remove Streamlit padding/branding
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

# 5. Sidebar AI Test Console
with st.sidebar:
    st.title("🛡️ API Test Console")
    st.info("Verify your Groq connection:")
    u_input = st.text_input("Send a message:")
    if st.button("Ask Serenity"):
        if u_input:
            with st.spinner("Wait..."):
                st.markdown(f"**AI:** {get_serenity_response(u_input)}")
        else:
            st.warning("Type something first!")

# 6. Render Dashboard
components.html(load_frontend(), height=1000, scrolling=False)