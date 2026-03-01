import { APIService } from '../services/api.js';

export class ChatUI {
    constructor(contextProvider) {
        this.contextProvider = contextProvider || (() => null);
        this.chatWindow = document.getElementById('chat-window');
        this.chatInput = document.getElementById('chat-input');
        this.messagesContainer = document.getElementById('chat-messages');
        this.sendBtn = document.getElementById('chat-send-btn');
        this.toggleBtn = document.getElementById('chat-toggle-btn');
        this.closeBtn = document.getElementById('chat-close-btn');
        this.minimizeBtn = document.getElementById('chat-minimize-btn');
        this.notificationDot = document.getElementById('chat-notification-dot');
        
        this.initEventListeners();
        this.loadHistory();
        this.checkUnreadStatus();
    }

    initEventListeners() {
        // Toggle
        if (this.toggleBtn) {
            this.toggleBtn.addEventListener('click', () => this.toggle());
        }

        // Close & Minimize
        if (this.closeBtn) {
            this.closeBtn.addEventListener('click', () => this.toggle());
        }
        if (this.minimizeBtn) {
            this.minimizeBtn.addEventListener('click', () => this.toggle());
        }

        // Send Message
        if (this.sendBtn) {
            this.sendBtn.addEventListener('click', () => this.handleSend());
        }
        if (this.chatInput) {
            this.chatInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') this.handleSend();
            });
        }

        // Quick Actions
        document.querySelectorAll('.quick-action-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.chatInput.value = e.target.innerText;
                this.handleSend();
            });
        });
    }

    toggle() {
        this.chatWindow.classList.toggle('d-none');
        this.toggleBtn.classList.toggle('d-none');
        
        if (!this.chatWindow.classList.contains('d-none')) {
            this.chatInput.focus();
            // Scroll to bottom when opened
            this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
            // Hide notification dot when opened
            if (this.notificationDot) this.notificationDot.classList.add('d-none');
            sessionStorage.setItem('chat_has_unread', 'false');
        }
    }

    async handleSend() {
        const message = this.chatInput.value.trim();
        if (!message) return;

        const context = this.contextProvider();

        this.addMessage('user', message);
        this.chatInput.value = '';
        this.chatInput.disabled = true;
        if (this.sendBtn) this.sendBtn.disabled = true;

        // Typing indicator
        const typingId = this.addTypingIndicator();

        try {
            const data = await APIService.sendChatMessage(message, context);
            
            this.removeMessage(typingId);

            if (data.error) {
                this.addMessage('bot', 'Sorry, I encountered an error: ' + data.error);
            } else {
                this.addMessage('bot', data.reply, true, message); // Pass prompt for feedback
            }

        } catch (error) {
            console.error("Chat Error:", error);
            this.removeMessage(typingId);
            this.addMessage('bot', 'Sorry, I am having trouble connecting right now.');
        } finally {
            this.chatInput.disabled = false;
            if (this.sendBtn) this.sendBtn.disabled = false;
            this.chatInput.focus();
        }
    }

    loadHistory() {
        const history = JSON.parse(sessionStorage.getItem('chat_history') || '[]');
        history.forEach(msg => {
            this.addMessage(msg.sender, msg.text, false);
        });
    }

    checkUnreadStatus() {
        const hasUnread = sessionStorage.getItem('chat_has_unread') === 'true';
        if (hasUnread && this.notificationDot) {
            this.notificationDot.classList.remove('d-none');
        }
    }

    addMessage(sender, text, save = true, originalPrompt = "") {
        // Save to session storage
        if (save) {
            const history = JSON.parse(sessionStorage.getItem('chat_history') || '[]');
            history.push({ sender, text, timestamp: Date.now() });
            sessionStorage.setItem('chat_history', JSON.stringify(history));

            // Show notification if bot sends message and window is closed
            if (sender === 'bot' && this.chatWindow.classList.contains('d-none')) {
                if (this.notificationDot) this.notificationDot.classList.remove('d-none');
                sessionStorage.setItem('chat_has_unread', 'true');
            }
        }

        const msgDiv = document.createElement('div');
        const msgId = 'msg-' + Date.now();
        msgDiv.id = msgId;
        
        if (sender === 'user') {
            msgDiv.className = 'd-flex justify-content-end chat-message-enter';
            msgDiv.innerHTML = `
                <div class="user-message-bubble bg-primary text-white p-3 rounded-4 shadow-sm small" style="max-width: 80%; border-top-right-radius: 4px !important; background: linear-gradient(135deg, #3b82f6, #2563eb);">
                    ${text}
                </div>
            `;
        } else {
            // Parse Markdown for bot messages
            const parsedText = typeof marked !== 'undefined' ? marked.parse(text) : text;
            
            // Build the core message bubble
            let botHTML = `
                <div class="rounded-circle bg-white shadow-sm d-flex align-items-center justify-content-center flex-shrink-0 border border-light-subtle" style="width: 36px; height: 36px;">
                    <i class="fas fa-robot text-primary small"></i>
                </div>
                <div class="d-flex flex-column gap-1 w-100" style="max-width: 80%;">
                    <div class="bot-message-bubble bg-white p-3 rounded-4 shadow-sm border border-light-subtle text-dark" 
                         style="border-top-left-radius: 4px !important; border-left: 3px solid #3b82f6;">
                        ${parsedText}
                    </div>
                    <div class="d-flex justify-content-between align-items-center mt-1">
                        <span class="text-muted fw-medium" style="font-size: 10px; letter-spacing: 0.5px;">AI ASSISTANT • JUST NOW</span>
            `;

            // If it's a freshly generated bot response (save=true) AND we have the prompt, inject Feedback UI
            if (save && originalPrompt && localStorage.getItem('access_token')) {
                 botHTML += `
                        <div class="feedback-container d-flex align-items-center justify-content-between w-100 mt-2 pt-2 border-top border-light" id="feedback-ctn-${msgId}">
                            <span class="text-muted fw-semibold" style="font-size: 10px; letter-spacing: 0.5px;"><i class="far fa-star me-1"></i> RATE THIS</span>
                            <div class="d-flex gap-1">
                                <button class="btn btn-sm rounded-circle d-flex align-items-center justify-content-center feedback-btn text-muted bg-light border-0 shadow-none ai-feedback-btn hover-emerald" data-helpful="true" data-msgid="${msgId}" style="width: 28px; height: 28px; transition: all 0.2s ease;">
                                    <i class="fas fa-thumbs-up" style="font-size: 11px;"></i>
                                </button>
                                <button class="btn btn-sm rounded-circle d-flex align-items-center justify-content-center feedback-btn text-muted bg-light border-0 shadow-none ai-feedback-btn hover-rose" data-helpful="false" data-msgid="${msgId}" style="width: 28px; height: 28px; transition: all 0.2s ease;">
                                    <i class="fas fa-thumbs-down" style="font-size: 11px;"></i>
                                </button>
                            </div>
                        </div>
                 `;
            }

            botHTML += `
                    </div>
                    <!-- Hidden Correction form for this specific message -->
                    <div class="correction-form d-none mt-2 p-2 rounded-3 border" id="correction-form-${msgId}" style="background: rgba(248, 250, 252, 0.8); border-color: rgba(0,0,0,0.05) !important;">
                        <textarea class="form-control form-control-sm mb-2 shadow-none bg-white" rows="2" placeholder="Tell us how we can improve (optional)..." id="correction-input-${msgId}" style="font-size: 0.85rem; border-radius: 8px; resize: none; border-color: rgba(0,0,0,0.1); color: #334155;"></textarea>
                        <div class="d-flex justify-content-end">
                            <button class="btn btn-primary px-3 py-1 d-flex align-items-center gap-1 submit-feedback-btn shadow-sm" data-msgid="${msgId}" data-prompt="${encodeURIComponent(originalPrompt)}" data-response="${encodeURIComponent(text)}" style="border-radius: 12px; font-size: 0.8rem; font-weight: 500; background: linear-gradient(135deg, #3b82f6, #2563eb); border: none;">
                                <i class="fas fa-paper-plane" style="font-size: 10px;"></i> Send
                            </button>
                        </div>
                    </div>
                </div>
            `;

            msgDiv.className = 'd-flex gap-3 chat-message-enter w-100';
            msgDiv.innerHTML = botHTML;
        }
        
        this.messagesContainer.appendChild(msgDiv);
        
        // Attach Feedback Event Listeners if applicable
        if (sender === 'bot' && save && originalPrompt && localStorage.getItem('access_token')) {
            this.bindFeedbackEvents(msgId);
        }

        this.scrollToBottom();
        return msgId;
    }

    bindFeedbackEvents(msgId) {
        let isHelpful = null;
        const container = document.getElementById(`feedback-ctn-${msgId}`);
        const thumbsBtns = container.querySelectorAll('.feedback-btn');
        const correctionForm = document.getElementById(`correction-form-${msgId}`);
        const submitBtn = document.querySelector(`.submit-feedback-btn[data-msgid="${msgId}"]`);
        const correctionInput = document.getElementById(`correction-input-${msgId}`);

        thumbsBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const target = e.currentTarget;
                isHelpful = target.dataset.helpful === "true";
                
                // Toggle active state styling
                thumbsBtns.forEach(b => {
                    b.classList.remove('text-success', 'text-danger');
                    b.classList.add('text-muted');
                    b.style.backgroundColor = '';
                });
                
                target.classList.remove('text-muted');
                if (isHelpful) {
                    target.classList.add('text-success');
                    target.style.backgroundColor = '#d1fae5';
                } else {
                    target.classList.add('text-danger');
                    target.style.backgroundColor = '#fee2e2';
                }

                // Show correction form
                if (correctionForm) correctionForm.classList.remove('d-none');
                this.scrollToBottom();
            });
        });

        submitBtn.addEventListener('click', async (e) => {
            const btn = e.currentTarget;
            const prompt = decodeURIComponent(btn.dataset.prompt);
            const responseText = decodeURIComponent(btn.dataset.response);
            const correction = correctionInput.value.trim();

            const payload = {
                prompt: prompt,
                gemini_response: responseText,
                is_helpful: isHelpful,
                user_correction: correction || null
            };

            btn.disabled = true;
            btn.innerText = "Submitting...";

            try {
                await APIService.submitChatFeedback(payload);
                container.innerHTML = `<span class="text-success" style="font-size: 11px;"><i class="fas fa-check-circle"></i> Feedback Saved!</span>`;
                correctionForm.remove(); // Remove form after success
            } catch (error) {
                console.error("Feedback error:", error);
                btn.innerText = "Error: " + error.message;
                btn.disabled = false;
            }
        });
    }

    addTypingIndicator() {
        const msgDiv = document.createElement('div');
        const msgId = 'typing-' + Date.now();
        msgDiv.id = msgId;
        msgDiv.className = 'd-flex gap-3 chat-message-enter';
        msgDiv.innerHTML = `
            <div class="rounded-circle bg-white shadow-sm d-flex align-items-center justify-content-center flex-shrink-0 border border-light" style="width: 32px; height: 32px;">
                <i class="fas fa-robot text-primary small"></i>
            </div>
            <div class="d-flex flex-column gap-1">
                <div class="bot-message-bubble d-flex align-items-center gap-1 bg-white p-3 rounded-4 shadow-sm border border-light" style="height: 42px; border-top-left-radius: 4px !important;">
                    <div class="typing-dot bg-secondary rounded-circle" style="width: 6px; height: 6px;"></div>
                    <div class="typing-dot bg-secondary rounded-circle" style="width: 6px; height: 6px;"></div>
                    <div class="typing-dot bg-secondary rounded-circle" style="width: 6px; height: 6px;"></div>
                </div>
            </div>
        `;
        this.messagesContainer.appendChild(msgDiv);
        this.scrollToBottom();
        return msgId;
    }

    removeMessage(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    scrollToBottom() {
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }
}
