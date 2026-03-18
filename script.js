// --- DOM Elements ---
const moodSlider = document.getElementById('moodSlider');
const moodEmoji = document.getElementById('moodEmoji');
const moodText = document.getElementById('moodText');
const saveMoodBtn = document.getElementById('saveMoodBtn');
const moodNote = document.getElementById('moodNote');
const moodHistoryList = document.getElementById('moodHistoryList');
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const chatMessages = document.getElementById('chatMessages');

// --- Configuration ---
const moods = {
    1: { emoji: '😢', text: 'Struggling', color: '#ef4444' },
    2: { emoji: '😔', text: 'Down', color: '#f59e0b' },
    3: { emoji: '😐', text: 'Neutral', color: '#f59e0b' },
    4: { emoji: '🙂', text: 'Good', color: '#10b981' },
    5: { emoji: '😄', text: 'Amazing', color: '#6366f1' }
};

// --- Mood Tracking ---
if(moodSlider) {
    moodSlider.oninput = (e) => {
        const mood = moods[e.target.value];
        moodEmoji.textContent = mood.emoji;
        moodText.textContent = mood.text;
        moodText.style.color = mood.color;
    };
}

if(saveMoodBtn) {
    saveMoodBtn.onclick = () => {
        showNotification('Mood saved! 💙');
        moodNote.value = '';
    };
}

// --- Navigation ---
const navBtns = document.querySelectorAll('.nav-btn');
const sections = document.querySelectorAll('.section');

navBtns.forEach(btn => {
    btn.onclick = () => {
        const target = btn.getAttribute('data-section');
        navBtns.forEach(b => b.classList.remove('active'));
        sections.forEach(s => s.classList.remove('active'));
        btn.classList.add('active');
        document.getElementById(target).classList.add('active');
    };
});

// --- Chat Logic ---
function addMessage(text, isUser) {
    if(!chatMessages) return;
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    msgDiv.innerHTML = `<div class="message-content"><p>${text}</p></div>`;
    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function sendMessage() {
    const text = chatInput.value.trim();
    if (!text) return;
    
    addMessage(text, true);
    chatInput.value = '';
    
    // Create "Thinking" indicator
    addMessage("Connecting to Serenity...", false);

    // BREAK OUT of iframe and reload parent with message
    const currentUrl = window.parent.location.href.split('?')[0];
    window.parent.location.href = currentUrl + "?msg=" + encodeURIComponent(text);
}

// Check for AI reply on load
window.onload = () => {
    if (window.SERENITY_REPLY && window.SERENITY_REPLY !== "" && window.SERENITY_REPLY !== "None") {
        // Automatically switch to chat tab
        const companionBtn = document.querySelector('[data-section="companion"]');
        if (companionBtn) companionBtn.click();
        addMessage(window.SERENITY_REPLY, false);
    }
};

if(sendBtn) sendBtn.onclick = sendMessage;
if(chatInput) chatInput.onkeypress = (e) => { if(e.key === 'Enter') sendMessage(); };

// --- Breathing Exercise ---
let breathing = false;
let bTimer;
const bCircle = document.getElementById('breathingCircle');
const bText = document.getElementById('breathingText');

function doBreath() {
    if(!breathing) return;
    bText.textContent = "Inhale...";
    bCircle.style.transform = "scale(1.4)";
    bTimer = setTimeout(() => {
        if(!breathing) return;
        bText.textContent = "Hold...";
        bTimer = setTimeout(() => {
            if(!breathing) return;
            bText.textContent = "Exhale...";
            bCircle.style.transform = "scale(1)";
            bTimer = setTimeout(doBreath, 4000);
        }, 4000);
    }, 4000);
}

document.getElementById('startBreathBtn').onclick = () => { breathing = true; doBreath(); };
document.getElementById('stopBreathBtn').onclick = () => { 
    breathing = false; 
    clearTimeout(bTimer); 
    bCircle.style.transform = "scale(1)";
    bText.textContent = "Ready?";
};

function showNotification(msg) {
    const n = document.createElement('div');
    n.style.cssText = "position:fixed;bottom:20px;right:20px;background:#6366f1;color:white;padding:12px;border-radius:8px;z-index:9999;";
    n.textContent = msg;
    document.body.appendChild(n);
    setTimeout(() => n.remove(), 3000);
}
