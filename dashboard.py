import streamlit as st
import os
from dotenv import load_dotenv, set_key

# Set page configuration
st.set_page_config(
    page_title="Mindful Admin Dashboard",
    page_icon="🧠",
    layout="wide"
)

# Load existing environment variables
env_path = ".env"
if not os.path.exists(env_path):
    with open(env_path, "w") as f:
        f.write("")
load_dotenv(env_path)

st.title("🧠 Mindful App Control Center")
st.markdown("---")

# --- API Configuration Section ---
st.subheader("🔑 API Configuration")
st.info("Your Groq API key is stored locally in a `.env` file and is never exposed to the frontend.")

current_key = os.getenv("GROQ_API_KEY", "")
new_key = st.text_input("Groq API Key", value=current_key, type="password", help="Get your key from console.groq.com")

if st.button("Save API Key"):
    if new_key:
        set_key(env_path, "GROQ_API_KEY", new_key)
        st.success("✅ API Key saved! Please restart your FastAPI server to apply changes.")
    else:
        st.error("❌ Please enter a valid API key.")

st.markdown("---")

# --- Database Overview (Bonus Feature) ---
st.subheader("📊 Mood Statistics")
if os.path.exists("mindful.db"):
    import sqlite3
    import pandas as pd
    
    try:
        conn = sqlite3.connect("mindful.db")
        df = pd.read_sql_query("SELECT * FROM mood_logs ORDER BY timestamp DESC", conn)
        conn.close()
        
        if not df.empty:
            st.write(f"Total entries: {len(df)}")
            # Simple chart of mood values
            st.line_chart(df.set_index('timestamp')['mood_value'])
            # Data table
            st.dataframe(df[['timestamp', 'mood_value', 'note', 'emoji']], use_container_width=True)
        else:
            st.write("No mood data recorded yet.")
    except Exception as e:
        st.error(f"Could not load database: {e}")
else:
    st.warning("Database file not found. It will be created when you run the FastAPI server.")

# --- System Status ---
st.sidebar.title("System Status")
st.sidebar.success("Dashboard: Online")
if os.getenv("GROQ_API_KEY"):
    st.sidebar.success("API Key: Configured")
else:
    st.sidebar.error("API Key: Missing")

st.sidebar.markdown("---")
st.sidebar.write("### How to use:")
st.sidebar.write("1. Enter Groq API Key.")
st.sidebar.write("2. Start `main.py` in your terminal.")
st.sidebar.write("3. Open `index.html` to start your companion.")