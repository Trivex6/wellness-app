import streamlit as st
import streamlit.components.v1 as components
import os

# 1. Setup
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

        # Added a wrapper div with 'display: flex' to handle layout alignment
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

# 2. CSS to remove ALL Streamlit gaps
st.markdown("""
    <style>
    /* Hide all Streamlit elements */
    header, footer, #MainMenu {visibility: hidden; display: none;}
    
    /* This is the key: Force the container to 100% width and 0 padding */
    .block-container {
        padding: 0rem !important;
        margin: 0rem !important;
        max-width: 100% !important;
        width: 100% !important;
    }
    
    .stApp {
        background-color: #0f172a;
    }

    /* Remove top margin from the first element */
    [data-testid="stVerticalBlock"] > div:first-child {
        padding-top: 0 !important;
    }

    /* Target the iframe directly */
    iframe {
        width: 100vw !important;
        height: 100vh !important;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Render
frontend_content = load_frontend()

# Use width=None here so it stretches to fill the container we just fixed
components.html(frontend_content, height=1000, scrolling=True)