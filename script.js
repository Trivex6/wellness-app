// --- DOM Elements ---
const navBtns = document.querySelectorAll('.nav-btn');
const sections = document.querySelectorAll('.section');
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const chatMessages = document.getElementById('chatMessages');

// --- Navigation ---
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

    addMessage("Thinking...", false);

    // Instead of redirecting parent (broken on Streamlit Cloud)
    const url = new URL(window.location.href);
    url.searchParams.set("msg", text);

    // Update URL WITHOUT full parent reload
    //window.location.href = url.toString();
}
// Check for AI reply on load
window.onload = () => {
    if (window.SERENITY_REPLY && window.SERENITY_REPLY !== "" && window.SERENITY_REPLY !== "None") {
        // Automatically switch to companion tab
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

// --- Mood Tracking ---
const moodSlider = document.getElementById('moodSlider');
const moodEmoji = document.getElementById('moodEmoji');
const moodText = document.getElementById('moodText');
const moods = {
    1: { emoji: '😢', text: 'Struggling', color: '#ef4444' },
    2: { emoji: '😔', text: 'Down', color: '#f59e0b' },
    3: { emoji: '😐', text: 'Neutral', color: '#f59e0b' },
    4: { emoji: '🙂', text: 'Good', color: '#10b981' },
    5: { emoji: '😄', text: 'Amazing', color: '#6366f1' }
};

if(moodSlider) {
    moodSlider.oninput = (e) => {
        const mood = moods[e.target.value];
        moodEmoji.textContent = mood.emoji;
        moodText.textContent = mood.text;
        moodText.style.color = mood.color;
    };
}
