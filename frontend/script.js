// Configuration
const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
let userInput;
let chatMessages;
let sendButton;
let typingIndicator;
let welcomeMessage;
let emergencyWarning;
let charCount;
let statusIndicator;
let disclaimerModal;
let disclaimerModalContent;

// State
let messageHistory = [];
let isProcessing = false;

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    initializeElements();
    setupEventListeners();
    checkBackendStatus();
    loadChatHistory();
});

// Initialize DOM element references
function initializeElements() {
    userInput = document.getElementById('userInput');
    chatMessages = document.getElementById('chatMessages');
    sendButton = document.getElementById('sendButton');
    typingIndicator = document.getElementById('typingIndicator');
    welcomeMessage = document.getElementById('welcomeMessage');
    emergencyWarning = document.getElementById('emergencyWarning');
    charCount = document.getElementById('charCount');
    statusIndicator = document.getElementById('statusIndicator');
    disclaimerModal = document.getElementById('disclaimerModal');
    disclaimerModalContent = document.getElementById('disclaimerModalContent');
}

// Setup event listeners
function setupEventListeners() {
    // Send button click
    sendButton.addEventListener('click', sendMessage);
    
    // Enter key to send (Shift+Enter for new line)
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Auto-resize textarea
    userInput.addEventListener('input', () => {
        autoResizeTextarea();
        updateCharCount();
    });
    
    // Close modal on background click
    disclaimerModal.addEventListener('click', (e) => {
        if (e.target === disclaimerModal) {
            closeDisclaimerModal();
        }
    });
}

// Auto-resize textarea based on content
function autoResizeTextarea() {
    userInput.style.height = 'auto';
    userInput.style.height = Math.min(userInput.scrollHeight, 120) + 'px';
}

// Update character count
function updateCharCount() {
    const count = userInput.value.length;
    charCount.textContent = `${count}/1000`;
    charCount.style.color = count > 900 ? '#d32f2f' : '';
}

// Check backend health status
async function checkBackendStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            updateStatusIndicator(true, data);
        } else {
            updateStatusIndicator(false);
        }
    } catch (error) {
        console.error('Backend health check failed:', error);
        updateStatusIndicator(false);
    }
}

// Update status indicator
function updateStatusIndicator(isOnline, data = null) {
    const statusDot = statusIndicator.querySelector('.status-dot');
    const statusText = statusIndicator.childNodes[1];
    
    if (isOnline) {
        statusDot.classList.remove('offline');
        statusText.textContent = ' Backend Connected';
        if (data && data.rag_enabled) {
            statusText.textContent += ' • RAG Enabled';
        }
    } else {
        statusDot.classList.add('offline');
        statusText.textContent = ' Backend Offline';
    }
}

// Send message
async function sendMessage() {
    const message = userInput.value.trim();
    
    if (!message || isProcessing) {
        return;
    }
    
    // Hide welcome message on first message
    if (welcomeMessage) {
        welcomeMessage.style.display = 'none';
    }
    
    // Add user message to chat
    addMessage(message, 'user');
    
    // Clear input
    userInput.value = '';
    updateCharCount();
    autoResizeTextarea();
    
    // Disable input while processing
    setProcessingState(true);
    
    // Show typing indicator
    showTypingIndicator();
    
    try {
        // Call backend API
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message
            })
        });
        
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Hide typing indicator
        hideTypingIndicator();
        
        // Add bot response
        addMessage(data.response, 'bot');
        
        // Check for emergency
        if (data.is_emergency) {
            showEmergencyWarning();
        } else {
            hideEmergencyWarning();
        }
        
        // Save chat history
        saveChatHistory();
        
    } catch (error) {
        console.error('Error sending message:', error);
        hideTypingIndicator();
        addMessage(
            '❌ Sorry, I encountered an error connecting to the backend. Please check if the server is running on port 8000 and try again.',
            'bot'
        );
    } finally {
        setProcessingState(false);
    }
}

// Add message to chat
function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = sender === 'user' ? '👤' : '⚕️';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    bubble.textContent = text;
    
    const time = document.createElement('div');
    time.className = 'message-time';
    time.textContent = getCurrentTime();
    
    contentDiv.appendChild(bubble);
    contentDiv.appendChild(time);
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(contentDiv);
    
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    scrollToBottom();
    
    // Save to history
    messageHistory.push({
        text: text,
        sender: sender,
        timestamp: new Date().toISOString()
    });
}

// Show typing indicator
function showTypingIndicator() {
    typingIndicator.style.display = 'flex';
    scrollToBottom();
}

// Hide typing indicator
function hideTypingIndicator() {
    typingIndicator.style.display = 'none';
}

// Show emergency warning
function showEmergencyWarning() {
    emergencyWarning.style.display = 'block';
}

// Hide emergency warning
function hideEmergencyWarning() {
    emergencyWarning.style.display = 'none';
}

// Set processing state
function setProcessingState(processing) {
    isProcessing = processing;
    sendButton.disabled = processing;
    userInput.disabled = processing;
}

// Scroll chat to bottom
function scrollToBottom() {
    setTimeout(() => {
        chatMessages.parentElement.scrollTop = chatMessages.parentElement.scrollHeight;
    }, 100);
}

// Get current time formatted
function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit',
        hour12: true 
    });
}

// Close disclaimer banner
function closeDisclaimer() {
    const banner = document.getElementById('disclaimerBanner');
    banner.style.display = 'none';
}

// Show full disclaimer modal
async function showDisclaimer() {
    try {
        const response = await fetch(`${API_BASE_URL}/disclaimer`);
        const data = await response.json();
        
        disclaimerModalContent.innerHTML = `
            <h3>Medical Disclaimer</h3>
            <p>${data.disclaimer}</p>
            <h3 style="margin-top: 1.5rem;">Important Information</h3>
            <ul style="margin-left: 1.5rem; line-height: 1.8;">
                <li>This chatbot is for informational purposes only</li>
                <li>It does not provide medical diagnosis or treatment</li>
                <li>Always consult qualified healthcare professionals for medical advice</li>
                <li>In case of emergency, call 108 (India) or visit your nearest hospital</li>
                <li>This is an academic project demonstrating AI in healthcare</li>
            </ul>
        `;
        
        disclaimerModal.style.display = 'flex';
    } catch (error) {
        console.error('Error loading disclaimer:', error);
        disclaimerModalContent.innerHTML = '<p>Error loading disclaimer. Please try again.</p>';
        disclaimerModal.style.display = 'flex';
    }
}

// Close disclaimer modal
function closeDisclaimerModal() {
    disclaimerModal.style.display = 'none';
}

// Clear chat
function clearChat() {
    if (confirm('Are you sure you want to clear the chat history?')) {
        chatMessages.innerHTML = '';
        messageHistory = [];
        welcomeMessage.style.display = 'block';
        hideEmergencyWarning();
        localStorage.removeItem('chatHistory');
    }
}

// Save chat history to localStorage
function saveChatHistory() {
    try {
        localStorage.setItem('chatHistory', JSON.stringify(messageHistory));
    } catch (error) {
        console.error('Error saving chat history:', error);
    }
}

// Load chat history from localStorage
function loadChatHistory() {
    try {
        const saved = localStorage.getItem('chatHistory');
        if (saved) {
            messageHistory = JSON.parse(saved);
            
            // Restore messages
            if (messageHistory.length > 0) {
                welcomeMessage.style.display = 'none';
                messageHistory.forEach(msg => {
                    addMessageFromHistory(msg);
                });
            }
        }
    } catch (error) {
        console.error('Error loading chat history:', error);
        messageHistory = [];
    }
}

// Add message from history (without saving again)
function addMessageFromHistory(msg) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${msg.sender}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = msg.sender === 'user' ? '👤' : '⚕️';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    bubble.textContent = msg.text;
    
    const time = document.createElement('div');
    time.className = 'message-time';
    const msgTime = new Date(msg.timestamp);
    time.textContent = msgTime.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit',
        hour12: true 
    });
    
    contentDiv.appendChild(bubble);
    contentDiv.appendChild(time);
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(contentDiv);
    
    chatMessages.appendChild(messageDiv);
}

// Check backend status periodically
setInterval(checkBackendStatus, 30000); // Every 30 seconds
