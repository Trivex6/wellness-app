// --- DOM Elements ---
const moodSlider = document.getElementById('moodSlider');
const moodEmoji = document.getElementById('moodEmoji');
const moodText = document.getElementById('moodText');
const saveMoodBtn = document.getElementById('saveMoodBtn');
const moodNote = document.getElementById('moodNote');
const moodHistoryList = document.getElementById('moodHistoryList');

// --- Configuration ---
const moods = {
    1: { emoji: '😢', text: 'Struggling', color: 'var(--danger-color)' },
    2: { emoji: '😔', text: 'Down', color: 'var(--warning-color)' },
    3: { emoji: '😐', text: 'Neutral', color: 'var(--warning-color)' },
    4: { emoji: '🙂', text: 'Good', color: 'var(--success-color)' },
    5: { emoji: '😄', text: 'Amazing', color: 'var(--primary-color)' }
};

// --- Mood Section Logic ---
if(moodSlider) {
    moodSlider.addEventListener('input', (e) => {
        const value = e.target.value;
        const mood = moods[value];
        moodEmoji.textContent = mood.emoji;
        moodText.textContent = mood.text;
        moodText.style.color = mood.color;
        moodEmoji.style.animation = 'none';
        void moodEmoji.offsetWidth; 
        moodEmoji.style.animation = 'bounce 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
    });
}

if(saveMoodBtn) {
    saveMoodBtn.addEventListener('click', () => {
        const moodValue = moodSlider.value;
        const mood = moods[moodValue];
        const noteText = moodNote.value.trim() || 'No note added';
        const now = new Date();
        const timestamp = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

        createHistoryItem(mood, noteText, timestamp, true);
        
        let moodHistory = JSON.parse(localStorage.getItem('moodHistory')) || [];
        moodHistory.unshift({ mood: moodValue, note: noteText, timestamp: now.toISOString() });
        localStorage.setItem('moodHistory', JSON.stringify(moodHistory.slice(0, 50)));

        moodNote.value = '';
        showNotification('Mood saved! Proud of you for checking in. 💙');
    });
}

function createHistoryItem(mood, note, time, prepend = false) {
    const historyItem = document.createElement('div');
    historyItem.className = 'history-item';
    historyItem.style.borderLeftColor = mood.color;
    historyItem.innerHTML = `
        <div style="display: flex; align-items: center; gap: 1rem;">
            <span class="emoji" style="font-size: 1.5rem;">${mood.emoji}</span>
            <div>
                <strong style="color: var(--gray-900);">${mood.text}</strong>
                <p style="font-size: 0.85rem; color: var(--gray-500); margin-top: 0.2rem;">${note}</p>
            </div>
        </div>
        <span class="time" style="font-weight: 600; color: var(--primary-light);">${time}</span>
    `;
    if (prepend) moodHistoryList.insertBefore(historyItem, moodHistoryList.firstChild);
    else moodHistoryList.appendChild(historyItem);
}

// --- Navigation Logic ---
const navBtns = document.querySelectorAll('.nav-btn');
const sections = document.querySelectorAll('.section');

navBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const sectionId = btn.getAttribute('data-section');
        navBtns.forEach(b => b.classList.remove('active'));
        sections.forEach(s => s.classList.remove('active'));
        btn.classList.add('active');
        document.getElementById(sectionId).classList.add('active');
    });
});

// --- Chat Section Logic ---
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const chatMessages = document.getElementById('chatMessages');

function addMessage(text, isUser) {
    if(!chatMessages) return;
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    messageDiv.innerHTML = `
        <div class="message-content">
            <p>${text}</p>
            <span class="timestamp">${timestamp}</span>
        </div>
    `;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTo({ top: chatMessages.scrollHeight, behavior: 'smooth' });
}

function sendMessage() {
    const message = chatInput.value.trim();
    if (!message) return;
    
    addMessage(message, true);
    chatInput.value = '';
    
    // Show local "Thinking" bubble
    addMessage("Thinking...", false);
    
    // Redirect parent window with message in URL
    // This forces the Python script to pick up 'msg' from query_params
    const baseUrl = window.parent.location.origin + window.parent.location.pathname;
    window.parent.location.assign(baseUrl + `?msg=${encodeURIComponent(message)}`);
}

// Handle AI response on page reload
window.addEventListener('load', () => {
    loadMoodHistory();
    // Check if Python injected a reply into the window
    if (window.SERENITY_REPLY && window.SERENITY_REPLY !== "" && window.SERENITY_REPLY !== "None") {
        addMessage(window.SERENITY_REPLY, false);
        
        // Auto-switch to chat tab if we have a reply
        const companionBtn = document.querySelector('[data-section="companion"]');
        if (companionBtn) companionBtn.click();
    }
});

if(sendBtn) sendBtn.addEventListener('click', sendMessage);
if(chatInput) chatInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') sendMessage(); });

// --- Breathing Section Logic ---
let isBreathing = false;
let breathingTimeout;

function animateBreathing() {
    if (!isBreathing) return;
    const circle = document.getElementById('breathingCircle');
    const text = document.getElementById('breathingText');

    text.textContent = 'Inhale...';
    circle.style.transform = 'scale(1.4)';

    breathingTimeout = setTimeout(() => {
        if (!isBreathing) return;
        text.textContent = 'Hold...';
        breathingTimeout = setTimeout(() => {
            if (!isBreathing) return;
            text.textContent = 'Exhale...';
            circle.style.transform = 'scale(1)';
            breathingTimeout = setTimeout(animateBreathing, 4000);
        }, 4000);
    }, 4000);
}

const startBtn = document.getElementById('startBreathBtn');
const stopBtn = document.getElementById('stopBreathBtn');

if(startBtn) {
    startBtn.addEventListener('click', () => {
        isBreathing = true;
        animateBreathing();
    });
}

if(stopBtn) {
    stopBtn.addEventListener('click', () => {
        isBreathing = false;
        clearTimeout(breathingTimeout);
        document.getElementById('breathingCircle').style.transform = 'scale(1)';
        document.getElementById('breathingText').textContent = 'Ready?';
    });
}

// --- Helpers ---
function loadMoodHistory() {
    if(!moodHistoryList) return;
    const moodHistory = JSON.parse(localStorage.getItem('moodHistory')) || [];
    moodHistoryList.innerHTML = '';
    moodHistory.slice(0, 10).forEach(item => {
        const mood = moods[item.mood];
        const time = new Date(item.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        createHistoryItem(mood, item.note, time);
    });
}

function showNotification(message) {
    const toast = document.createElement('div');
    toast.className = 'notification';
    toast.style.cssText = `position:fixed; bottom:30px; right:30px; background:white; padding:1rem; border-radius:12px; box-shadow:0 10px 15px rgba(0,0,0,0.1); z-index:9999; font-weight:600; border-left: 5px solid #6366f1; color: #1e293b;`;
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 4000);
}
