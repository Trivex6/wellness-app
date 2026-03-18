import streamlit as st
import streamlit.components.v1 as components
import os

# 1. Page Configuration
st.set_page_config(
    page_title="Serenity Wellness",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. File Loading Logic
def load_frontend():
    # Check if files exist in the current directory
    files = os.listdir(".")
    st.write(f"", unsafe_allow_html=True)
    
    try:
        # Load with explicit encoding to avoid Streamlit Cloud errors
        with open("index.html", "r", encoding="utf-8") as f:
            html = f.read()
        with open("style.css", "r", encoding="utf-8") as f:
            css = f.read()
        with open("script.js", "r", encoding="utf-8") as f:
            js = f.read()

        # Inject CSS and JS into the HTML string
        # We use a combined string to ensure everything loads simultaneously
        full_code = f"""
        <html>
            <head>
                <style>{css}</style>
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

# 3. UI Cleanup (Hides Streamlit's interface for a pure app look)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { margin-top: -80px; background-color: #0f172a; } /* Matches your dark theme */
    iframe { border: none; }
    </style>
    """, unsafe_allow_html=True)

# 4. Render the App
frontend_content = load_frontend()
components.html(frontend_content, height=1200, scrolling=True)