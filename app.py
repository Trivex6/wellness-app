import streamlit as st
import streamlit.components.v1 as components
import os

# 1. Page Configuration - Changed to 'centered' for a more focused UI
st.set_page_config(
    page_title="Serenity Wellness",
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# 2. File Loading Logic
def load_frontend():
    try:
        # Load with explicit encoding
        with open("index.html", "r", encoding="utf-8") as f:
            html = f.read()
        with open("style.css", "r", encoding="utf-8") as f:
            css = f.read()
        with open("script.js", "r", encoding="utf-8") as f:
            js = f.read()

        # Wrap everything in a standard HTML structure 
        # We add a max-width to the body style here as a safety measure
        full_code = f"""
        <!DOCTYPE html>
        <html>
            <head>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    {css}
                    /* Ensure the inner body doesn't stretch awkwardly */
                    body {{ 
                        margin: 0; 
                        padding: 0; 
                        display: flex; 
                        justify-content: center; 
                        background: transparent;
                    }}
                </style>
            </head>
            <body>
                <div style="width: 100%; max-width: 1200px;">
                    {html}
                </div>
                <script>{js}</script>
            </body>
        </html>
        """
        return full_code
    except Exception as e:
        return f"<h2 style='color:white;'>Error Loading Files: {e}</h2>"

# 3. UI Cleanup
# This part removes the Streamlit header and padding to make it feel like a standalone app
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    /* Remove padding from the Streamlit container */
    .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    .stApp { 
        background-color: #0f172a; 
    }
    iframe { 
        border: none; 
        display: block;
        margin: 0 auto;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. Render the App
frontend_content = load_frontend()

# Using width=None allows it to take the full width of the 'centered' Streamlit column
components.html(frontend_content, height=1000, scrolling=True)