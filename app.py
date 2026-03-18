import streamlit as st
from groq import Groq

# ---------- CONFIG ----------
st.set_page_config(page_title="Serenity AI", layout="wide")

# ---------- API ----------
api_key = st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

def get_response(user_text):
    if not client:
        return "API key missing."

    try:
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are Serenity, a calm and supportive mental health assistant. Keep responses short and warm."},
                {"role": "user", "content": user_text}
            ],
            temperature=0.7,
            max_tokens=150
        )
        return res.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"


# ---------- UI ----------
st.title("💙 Serenity AI Companion")

# Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input
user_input = st.chat_input("How are you feeling today?")

if user_input:
    # User message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = get_response(user_input)
            st.write(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})


# ---------- EXTRA FEATURES (KEEP YOUR PROJECT VALUE) ----------

st.sidebar.title("🌿 Wellness Tools")

# Mood tracker
st.sidebar.subheader("Mood Tracker")
mood = st.sidebar.slider("How are you feeling?", 1, 5, 3)

mood_labels = {
    1: "😢 Struggling",
    2: "😔 Down",
    3: "😐 Neutral",
    4: "🙂 Good",
    5: "😄 Amazing"
}
st.sidebar.write(mood_labels[mood])

# Breathing exercise
st.sidebar.subheader("Breathing Exercise")
if st.sidebar.button("Start Breathing"):
    st.sidebar.write("Inhale... Hold... Exhale... Repeat 🌬️")
