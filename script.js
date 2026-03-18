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
moodSlider.addEventListener('input', (e) => {
    const value = e.target.value;
    const mood = moods[value];
    
    moodEmoji.textContent = mood.emoji;
    moodText.textContent = mood.text;
    moodText.style.color = mood.color;
    
    // Reset and trigger bounce animation
    moodEmoji.style.animation = 'none';
    void moodEmoji.offsetWidth; // Trigger reflow
    moodEmoji.style.animation = 'bounce 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
});

saveMoodBtn.addEventListener('click', () => {
    const moodValue = moodSlider.value;
    const mood = moods[moodValue];
    const noteText = moodNote.value.trim() || 'No note added';
    const now = new Date();
    const timestamp = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    createHistoryItem(mood, noteText, timestamp, true);

    const moodData = {
        mood: moodValue,
        note: noteText,
        timestamp: now.toISOString()
    };
    
    let moodHistory = JSON.parse(localStorage.getItem('moodHistory')) || [];
    moodHistory.unshift(moodData);
    localStorage.setItem('moodHistory', JSON.stringify(moodHistory.slice(0, 50)));

    moodNote.value = '';
    showNotification('Mood saved! Proud of you for checking in. 💙');
});

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
    
    if (prepend) {
        moodHistoryList.insertBefore(historyItem, moodHistoryList.firstChild);
    } else {
        moodHistoryList.appendChild(historyItem);
    }
}

function loadMoodHistory() {
    const moodHistory = JSON.parse(localStorage.getItem('moodHistory')) || [];
    moodHistoryList.innerHTML = ''; // Clear current list
    moodHistory.slice(0, 10).forEach(item => {
        const mood = moods[item.mood];
        const date = new Date(item.timestamp);
        const time = date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        createHistoryItem(mood, item.note, time);
    });
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
        const targetSection = document.getElementById(sectionId);
        targetSection.classList.add('active');
        
        // Mobile Sidebar Auto-close
        if (window.innerWidth <= 768) {
            document.querySelector('.sidebar').classList.remove('active');
        }
    });
});

// --- Chat Section Logic ---
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const chatMessages = document.getElementById('chatMessages');

function addMessage(text, isUser) {
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
    
    // Typing indicator
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot-message';
    typingDiv.innerHTML = `<div class="message-content"><p style="font-style: italic; opacity: 0.6;">Thinking...</p></div>`;
    chatMessages.appendChild(typingDiv);
    
    setTimeout(() => {
        typingDiv.remove();
        const botResponse = getBotResponse(message);
        addMessage(botResponse, false);
    }, 1200);
}

sendBtn.addEventListener('click', sendMessage);
chatInput.addEventListener('keypress', (e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); } });

// --- Breathing Section Logic ---
let isBreathing = false;
let cycleCount = 0;
let breathingTimeout;

function animateBreathing() {
    if (!isBreathing) return;

    const inhale = parseInt(document.getElementById('inhaleSlider').value) * 1000;
    const hold = parseInt(document.getElementById('holdSlider').value) * 1000;
    const exhale = parseInt(document.getElementById('exhaleSlider').value) * 1000;

    const circle = document.getElementById('breathingCircle');
    const text = document.getElementById('breathingText');

    // Inhale
    text.textContent = 'Inhale...';
    circle.style.transition = `all ${inhale}ms ease-in-out`;
    circle.style.transform = 'scale(1.4)';
    circle.style.boxShadow = '0 0 60px rgba(99, 102, 241, 0.4)';
    circle.style.filter = 'blur(2px)'; // Optional: adds a slight "air" effect

    breathingTimeout = setTimeout(() => {
        if (!isBreathing) return;
        // Hold
        text.textContent = 'Hold...';
        
        breathingTimeout = setTimeout(() => {
            if (!isBreathing) return;
            // Exhale
            text.textContent = 'Exhale...';
            circle.style.transition = `all ${exhale}ms ease-in-out`;
            circle.style.transform = 'scale(1)';
            circle.style.boxShadow = '0 0 0px rgba(99, 102, 241, 0)';

            breathingTimeout = setTimeout(() => {
                if (!isBreathing) return;
                cycleCount++;
                document.getElementById('cycleCounter').textContent = cycleCount;
                animateBreathing();
            }, exhale);
        }, hold);
    }, inhale);
}

document.getElementById('startBreathBtn').addEventListener('click', function() {
    isBreathing = true;
    cycleCount = 0;
    this.disabled = true;
    document.getElementById('stopBreathBtn').disabled = false;
    animateBreathing();
});

document.getElementById('stopBreathBtn').addEventListener('click', function() {
    isBreathing = false;
    clearTimeout(breathingTimeout);
    this.disabled = true;
    document.getElementById('startBreathBtn').disabled = false;
    const circle = document.getElementById('breathingCircle');
    circle.style.transform = 'scale(1)';
    document.getElementById('breathingText').textContent = 'Ready?';
});

// --- Helpers ---
function showNotification(message) {
    const existing = document.querySelector('.notification');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = 'notification';
    toast.style.cssText = `
        position: fixed; bottom: 30px; right: 30px;
        background: var(--white); border-left: 5px solid var(--primary-color);
        padding: 1rem 1.5rem; border-radius: 12px;
        box-shadow: var(--shadow-strong); z-index: 9999;
        animation: slideIn 0.4s ease-out; font-weight: 600;
    `;
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 4000);
}

// Initial Load
window.addEventListener('DOMContentLoaded', () => {
    loadMoodHistory();
    console.log('Mindful App: Connection established. 🧠');
});