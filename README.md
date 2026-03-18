# 🌿 Serenity: AI-Driven Wellness Dashboard

**Live Demo:** [https://frontend-azw43kjzgbtknqphqddf6c.streamlit.app/](https://frontend-azw43kjzgbtknqphqddf6c.streamlit.app/)

---

## 📖 Project Overview
**Serenity** is a modern, high-performance wellness dashboard designed to provide a calming, interactive space for mental health management. By combining the data-handling power of **Python** with the aesthetic flexibility of **Vanilla JavaScript and CSS**, it delivers a seamless "Glassmorphism" UI that standard Streamlit components cannot achieve.

This project was developed as a technical challenge to bridge the gap between static web design and dynamic AI-driven backends.

## ✨ Core Features
* **🤖 AI Companion:** Real-time, compassionate chat powered by the **Groq Llama-3-8b** LLM, providing supportive wellness advice.
* **📊 Dynamic Mood Tracking:** An interactive logging tool with instant visual feedback via a custom JS-driven slider and emoji-state mapping.
* **🧘 Mindful Breathing:** A "Box Breathing" utility with animated visual cues to assist users in immediate stress reduction.
* **🎨 Glassmorphic UI:** A custom-styled frontend that overrides the default Streamlit layout for a premium, mobile-responsive experience.

## 🛠️ Tech Stack & Architecture
* **Frontend:** HTML5, CSS3 (Custom Variables/Animations), JavaScript (ES6+).
* **Backend:** Python 3.10+ (Streamlit Framework).
* **AI Engine:** Groq Cloud API.
* **Deployment:** Streamlit Cloud.

## 🚀 The Technical Challenge: The "Bridge" Protocol
Since Streamlit isolates custom HTML within an iframe, traditional state sharing is restricted. This project utilizes a custom-engineered **Parent-Window URL Redirect** protocol:
1.  **Frontend (JS):** Captures user chat input and forces a parent-level reload using `window.parent.location.href` with an encoded `?msg=` parameter.
2.  **Backend (Python):** Intercepts the query parameter using `st.query_params`, calls the Groq API, and injects the response back into the frontend's global scope (`window.SERENITY_REPLY`) upon reload.

## 📂 Repository Structure
* `app.py`: The Python backbone managing AI calls and frontend injection.
* `index.html`: Structural layout and dashboard components.
* `style.css`: Custom Glassmorphic styling and responsive design.
* `script.js`: Client-side logic for navigation, mood tracking, and the communication bridge.
* `requirements.txt`: Project dependencies (Streamlit, Groq).

