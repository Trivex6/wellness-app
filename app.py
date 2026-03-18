import streamlit as st
import streamlit.components.v1 as components
import os

# 1. Force Wide Layout but we will control the inner width via CSS
st.set_page_config(
    page_title="Serenity Wellness",
    layout="wide", 
    initial_sidebar_state="collapsed"
)

def load_frontend():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            html = f.read()
        with open("style.css", "r", encoding="utf-8") as f:
            css = f.read()
        with open("script.js", "r", encoding="utf-8") as f:
            js = f.read()

        # This combined string fixes the 'double centering' issue
        full_code = f"""
        <!DOCTYPE html>
        <html>
            <head>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    {css}
                    body {{ 
                        margin: 0; 
                        padding: 0; 
                        overflow-x: hidden;
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

# 2. THE CRITICAL PART: Remove Streamlit's default padding
st.markdown("""
    <style>
    /* Hide Header and Footer */
    header, footer, #MainMenu {visibility: hidden;}
    
    /* Remove padding from the main Streamlit area */
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    /* Ensure the app background matches your dark theme */
    .stApp {
        background-color: #0f172a;
    }
    
    /* Remove the gap at the top */
    div[data-testid="stVerticalBlock"] > div:first-child {
        margin-top: 0;
    }
    
    iframe {
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Render the App
frontend_content = load_frontend()

# Use width=None and height=1000 to fill the space
components.html(frontend_content, height=1000, scrolling=False)