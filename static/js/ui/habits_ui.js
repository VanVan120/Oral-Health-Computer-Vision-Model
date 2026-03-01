/**
 * Preventative Care Hub - Habits Tracker Module
 * Handles habit logging, history display, action plan banner,
 * daily tips, achievement badges, and celebration animations.
 */
export class HabitsUI {
    constructor(getAnalysisDataFn) {
        this.getAnalysisData = getAnalysisDataFn;
        this.todaySaved = false;

        // Daily oral health tips (rotates by day of year)
        this.dailyTips = [
            { icon: 'fa-clock', title: 'Timing Matters', text: 'Wait 30 minutes after eating acidic foods before brushing — acid softens enamel temporarily.', color: '#2563eb' },
            { icon: 'fa-tongue', title: 'Don\'t Forget Your Tongue', text: 'Gently brush or scrape your tongue daily to remove bacteria that cause bad breath.', color: '#7c3aed' },
            { icon: 'fa-glass-water', title: 'Rinse After Coffee', text: 'Swish water after coffee or tea to reduce staining and neutralize acids.', color: '#059669' },
            { icon: 'fa-moon', title: 'Night Routine is Key', text: 'Your nighttime brush is the most important — saliva production drops during sleep, leaving teeth vulnerable.', color: '#1d4ed8' },
            { icon: 'fa-cheese', title: 'Cheese is Your Friend', text: 'Eating cheese raises mouth pH and strengthens enamel with calcium and casein.', color: '#f59e0b' },
            { icon: 'fa-leaf', title: 'Green Tea Benefits', text: 'Green tea contains catechins that fight oral bacteria and reduce inflammation naturally.', color: '#10b981' },
            { icon: 'fa-hand-sparkles', title: 'Replace Your Brush', text: 'Swap your toothbrush every 3 months, or sooner if bristles are frayed. Old brushes harbor bacteria.', color: '#ef4444' },
            { icon: 'fa-carrot', title: 'Crunchy Veggies Clean Teeth', text: 'Raw carrots, celery, and apples act as natural toothbrushes, stimulating saliva flow.', color: '#f97316' },
            { icon: 'fa-tint', title: 'Fluoride Boost', text: 'Don\'t rinse with water right after brushing — let fluoride toothpaste sit on teeth for maximum protection.', color: '#6366f1' },
            { icon: 'fa-smile', title: 'Smile More!', text: 'Smiling reduces stress hormones and boosts immune function — good for your overall and oral health.', color: '#ec4899' },
            { icon: 'fa-candy-cane', title: 'Sugar-Free Gum Helps', text: 'Chewing xylitol gum after meals stimulates saliva and actively fights cavity-causing bacteria.', color: '#14b8a6' },
            { icon: 'fa-bed', title: 'Sleep & Oral Health', text: 'Poor sleep weakens immunity and increases gum disease risk. Aim for 7-9 hours nightly.', color: '#8b5cf6' },
            { icon: 'fa-droplet', title: 'Stay Hydrated', text: 'Drinking water throughout the day keeps saliva levels healthy and washes away food particles.', color: '#0ea5e9' },
            { icon: 'fa-seedling', title: 'Vitamin C Power', text: 'Vitamin C strengthens gum tissue and fights gingivitis. Eat citrus fruits, peppers, and strawberries.', color: '#22c55e' },
        ];

        // Motivational messages by score
        this.scoreMessages = {
            5: ['Perfect score! You\'re a dental superstar!', 'Flawless! Your dentist would be proud!', 'Amazing! Keep this streak going!'],
            4: ['Great job! Almost perfect today!', 'Awesome effort! One small tweak away from perfection!', 'Very impressive! Keep it up!'],
            3: ['Good start! Room for improvement!', 'Not bad! Try to level up tomorrow!', 'Decent day! Challenge yourself for a 4 next time!'],
            2: ['Keep trying! Every small step counts!', 'Tomorrow is a fresh start!', 'You showed up — that matters!'],
            1: ['Don\'t give up! Logging is the first step!', 'Awareness is key — you\'re on the right track!'],
            0: ['Every journey starts somewhere! Try again tomorrow!', 'The fact that you\'re tracking shows you care!'],
        };

        // Achievement levels based on streak
        this.levels = [
            { min: 0,  label: 'Starter',        icon: 'fa-seedling',     color: '#94a3b8' },
            { min: 3,  label: 'Committed',       icon: 'fa-leaf',         color: '#10b981' },
            { min: 7,  label: 'Consistent',      icon: 'fa-star',         color: '#3b82f6' },
            { min: 14, label: 'Dedicated',        icon: 'fa-medal',        color: '#f59e0b' },
            { min: 21, label: 'Oral Care Pro',    icon: 'fa-crown',        color: '#7c3aed' },
            { min: 30, label: 'Legendary',        icon: 'fa-gem',          color: '#ec4899' },
        ];

        this.init();
    }

    init() {
        // Set today's date display
        const dateEl = document.getElementById('habit-date-display');
        if (dateEl) {
            const today = new Date();
            dateEl.textContent = today.toLocaleDateString('en-US', {
                weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
            });
        }

        // Expose global functions
        window.saveHabitLog = () => this.saveLog();
        window.openActionPlanChat = () => this.openActionPlanChat();
        window.showPreventativeCare = () => this.showView();
        window.openChatWidget = () => {
            const modal = bootstrap.Modal.getInstance(document.getElementById('actionPlanModal'));
            if (modal) modal.hide();
            const chatToggle = document.getElementById('chat-toggle-btn') || document.querySelector('.chat-toggle');
            if (chatToggle) chatToggle.click();
        };

        // Render daily tip
        this.renderDailyTip();

        // Load existing data if user is logged in
        this.loadTodayLog();
        this.loadHistory();
    }

    getAuthToken() {
        return localStorage.getItem('access_token');
    }

    isLoggedIn() {
        return !!this.getAuthToken();
    }

    showView() {
        // Hide all other views, show preventative care view
        const allViews = ['home-view', 'triage-view', 'model-a-view', 'model-b-view'];
        allViews.forEach(id => {
            const el = document.getElementById(id);
            if (el) el.classList.add('hidden-section');
        });

        const careView = document.getElementById('preventative-care-view');
        if (!careView) {
            // Not on the index page — redirect with hash
            window.location.href = '/#care-hub';
            return;
        }

        careView.classList.remove('hidden-section');
        careView.scrollIntoView({ behavior: 'smooth', block: 'start' });

        // Update navbar active state to highlight Care Hub
        const navLinks = document.querySelectorAll('.navbar-links a');
        navLinks.forEach(link => link.classList.remove('active'));
        const careLink = document.getElementById('nav-care');
        if (careLink) careLink.classList.add('active');

        this.loadTodayLog();
        this.loadHistory();
        this.checkForActionBanner();
    }

    async saveLog() {
        const token = this.getAuthToken();
        if (!token) {
            this.showStatus('Please log in to save your habits.', 'error');
            return;
        }

        if (this.todaySaved) return; // Already saved

        const btn = document.getElementById('btn-save-habits');
        const originalText = btn.innerHTML;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Saving...';
        btn.disabled = true;

        const payload = {
            smoked_cigarettes: document.getElementById('habit-smoked')?.checked || false,
            ate_sweets: document.getElementById('habit-sweets')?.checked || false,
            brushed_after_meal: document.getElementById('habit-brushed')?.checked || false,
            used_floss: document.getElementById('habit-floss')?.checked || false,
            used_sensodyne: document.getElementById('habit-sensodyne')?.checked || false,
        };

        try {
            const response = await fetch('/habits/log', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + token
                },
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.detail || 'Failed to save');
            }

            // Calculate today's score
            const score = this.calculateScore(payload);

            // Lock the form
            this.lockForm();

            // Show score celebration
            this.showScoreCelebration(score);

            this.showStatus('Habits saved successfully!', 'success');
            this.loadHistory();
        } catch (error) {
            console.error('Habit Save Error:', error);
            this.showStatus('Failed to save. ' + error.message, 'error');
            btn.innerHTML = originalText;
            btn.disabled = false;
        }
    }

    /**
     * Calculate habits score from a log/payload object
     */
    calculateScore(log) {
        let score = 0;
        if (log.brushed_after_meal) score++;
        if (log.used_floss) score++;
        if (log.used_sensodyne) score++;
        if (!log.smoked_cigarettes) score++;
        if (!log.ate_sweets) score++;
        return score;
    }

    /**
     * Lock all toggle switches and transform the save button
     */
    lockForm() {
        this.todaySaved = true;

        // Disable all habit checkboxes
        const checkboxes = ['habit-smoked', 'habit-sweets', 'habit-brushed', 'habit-floss', 'habit-sensodyne'];
        checkboxes.forEach(id => {
            const el = document.getElementById(id);
            if (el) {
                el.disabled = true;
                el.closest('.habit-switch')?.classList.add('locked');
            }
        });

        // Add locked class to the card body
        const cardBody = document.querySelector('.habit-card-body');
        if (cardBody) cardBody.classList.add('habits-locked');

        // Transform save button to "Saved" state
        const btn = document.getElementById('btn-save-habits');
        if (btn) {
            btn.innerHTML = '<i class="fas fa-check-circle me-2"></i>Saved for Today';
            btn.disabled = true;
            btn.classList.add('habit-saved-btn');
        }
    }

    /**
     * Show a dramatic full-screen celebration popup
     */
    showScoreCelebration(score) {
        // Remove any existing popup
        const existing = document.getElementById('score-popup-overlay');
        if (existing) existing.remove();

        const emojis = ['😟', '😐', '🙂', '😊', '🌟', '🏆'];
        const emoji = emojis[Math.min(score, 5)];

        const messages = this.scoreMessages[score] || this.scoreMessages[0];
        const message = messages[Math.floor(Math.random() * messages.length)];

        const cls = score >= 5 ? 'excellent' : score >= 4 ? 'good' : score >= 3 ? 'average' : 'poor';

        const subtitles = {
            excellent: 'Outstanding Performance',
            good: 'Great Effort Today',
            average: 'Solid Foundation',
            poor: 'Room to Grow'
        };

        const gradients = {
            excellent: 'linear-gradient(135deg, #10b981, #059669)',
            good: 'linear-gradient(135deg, #3b82f6, #2563eb)',
            average: 'linear-gradient(135deg, #f59e0b, #d97706)',
            poor: 'linear-gradient(135deg, #ef4444, #dc2626)'
        };

        // Build the stars display
        let starsHtml = '';
        for (let i = 1; i <= 5; i++) {
            const filled = i <= score;
            const delay = 0.6 + i * 0.12;
            starsHtml += `<span class="popup-star ${filled ? 'filled' : 'empty'}" style="animation-delay: ${delay}s;"><i class="fas fa-star"></i></span>`;
        }

        // Create overlay with INLINE critical styles (guarantees centering regardless of CSS cache)
        const overlay = document.createElement('div');
        overlay.id = 'score-popup-overlay';
        overlay.className = 'score-popup-overlay';
        Object.assign(overlay.style, {
            position: 'fixed',
            top: '0',
            left: '0',
            right: '0',
            bottom: '0',
            width: '100vw',
            height: '100vh',
            background: 'rgba(0, 0, 0, 0.5)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: '99999',
            padding: '20px',
            boxSizing: 'border-box',
            backdropFilter: 'blur(8px)',
            WebkitBackdropFilter: 'blur(8px)',
        });

        overlay.innerHTML = `
            <div class="score-popup-card score-popup-${cls}" style="position:relative; width:100%; max-width:380px; border-radius:28px; overflow:hidden; background:#fff; box-shadow:0 24px 80px rgba(0,0,0,0.25); animation:popupBounceIn 0.5s cubic-bezier(0.175,0.885,0.32,1.275);">
                <div class="score-popup-glow" style="height:6px; width:100%; background:${gradients[cls]};"></div>
                <div class="score-popup-content" style="padding:36px 32px 32px; text-align:center; position:relative; z-index:2;">
                    <div class="score-popup-emoji-ring" style="width:88px; height:88px; border-radius:50%; border:4px solid ${cls === 'excellent' ? '#10b981' : cls === 'good' ? '#3b82f6' : cls === 'average' ? '#f59e0b' : '#ef4444'}; display:flex; align-items:center; justify-content:center; margin:0 auto 20px; background:rgba(255,255,255,0.95); box-shadow:0 8px 32px rgba(0,0,0,0.08); animation:emojiPulse 0.6s ease-out 0.3s both;">
                        <span class="score-popup-emoji" style="font-size:2.5rem; line-height:1;">${emoji}</span>
                    </div>
                    <div class="score-popup-score" style="font-size:3rem; font-weight:800; line-height:1; margin-bottom:6px; color:#1e293b;">${score}<span class="score-popup-total" style="font-size:1.4rem; font-weight:600; opacity:0.4;">/5</span></div>
                    <div class="score-popup-stars" style="display:flex; justify-content:center; gap:8px; margin-bottom:18px;">${starsHtml}</div>
                    <div class="score-popup-subtitle" style="font-size:0.8rem; font-weight:700; text-transform:uppercase; letter-spacing:2px; margin-bottom:8px; color:${cls === 'excellent' ? '#10b981' : cls === 'good' ? '#3b82f6' : cls === 'average' ? '#f59e0b' : '#ef4444'};">${subtitles[cls]}</div>
                    <div class="score-popup-message" style="font-size:1rem; font-weight:500; color:#334155; line-height:1.5; margin-bottom:24px;">${message}</div>
                    <button class="score-popup-close-btn" id="score-popup-close" style="display:inline-flex; align-items:center; justify-content:center; padding:12px 36px; border:none; border-radius:50px; font-size:0.95rem; font-weight:700; color:#fff; cursor:pointer; background:${gradients[cls]}; box-shadow:0 4px 16px rgba(0,0,0,0.2); transition:all 0.3s ease;">
                        <i class="fas fa-check me-2"></i>Awesome!
                    </button>
                </div>
                <div class="score-popup-confetti" id="popup-confetti" style="position:absolute; top:50%; left:50%; width:0; height:0; pointer-events:none; z-index:1; overflow:visible;"></div>
            </div>`;

        document.body.appendChild(overlay);

        // Force reflow to ensure animations trigger
        void overlay.offsetHeight;

        // Close button handler (event listener — safer than inline onclick)
        const closeBtn = document.getElementById('score-popup-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => this.dismissPopup(overlay));
        }

        // Click overlay backdrop to close
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) this.dismissPopup(overlay);
        });

        // Escape key to close
        const escHandler = (e) => {
            if (e.key === 'Escape') {
                this.dismissPopup(overlay);
                document.removeEventListener('keydown', escHandler);
            }
        };
        document.addEventListener('keydown', escHandler);

        // Fire integrated confetti for good scores
        if (score >= 3) {
            setTimeout(() => this.firePopupConfetti(), 400);
        }

        // Auto-dismiss after 8 seconds
        setTimeout(() => {
            if (document.getElementById('score-popup-overlay')) {
                this.dismissPopup(overlay);
            }
        }, 8000);
    }

    /**
     * Dismiss the popup with exit animation
     */
    dismissPopup(overlay) {
        if (!overlay || overlay.classList.contains('closing')) return;
        overlay.classList.add('closing');
        overlay.style.opacity = '0';
        overlay.style.transition = 'opacity 0.35s ease-in';
        const card = overlay.querySelector('.score-popup-card');
        if (card) {
            card.style.transform = 'scale(0.7) translateY(30px)';
            card.style.opacity = '0';
            card.style.transition = 'all 0.3s ease-in';
        }
        setTimeout(() => overlay.remove(), 400);
    }

    /**
     * Fire confetti particles inside the popup
     */
    firePopupConfetti() {
        const container = document.getElementById('popup-confetti');
        if (!container) return;

        const colors = ['#10b981', '#3b82f6', '#f59e0b', '#ec4899', '#8b5cf6', '#ef4444', '#06b6d4', '#fbbf24', '#a78bfa'];

        for (let i = 0; i < 60; i++) {
            const particle = document.createElement('div');
            particle.className = 'confetti-particle';
            const xSpread = (Math.random() - 0.5) * 500;
            const ySpread = -Math.random() * 350 - 80;
            particle.style.setProperty('--x', `${xSpread}px`);
            particle.style.setProperty('--y', `${ySpread}px`);
            particle.style.setProperty('--r', `${Math.random() * 1080 - 540}deg`);
            particle.style.setProperty('--delay', `${Math.random() * 0.5}s`);
            particle.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];

            if (Math.random() > 0.5) {
                particle.style.borderRadius = '50%';
                const size = 6 + Math.random() * 8;
                particle.style.width = `${size}px`;
                particle.style.height = `${size}px`;
            } else {
                particle.style.width = `${8 + Math.random() * 10}px`;
                particle.style.height = `${4 + Math.random() * 5}px`;
                particle.style.borderRadius = '2px';
            }

            container.appendChild(particle);
        }
    }

    async loadTodayLog() {
        const token = this.getAuthToken();
        if (!token) return;

        try {
            const response = await fetch('/habits/history', {
                headers: { 'Authorization': 'Bearer ' + token }
            });
            if (!response.ok) return;

            const logs = await response.json();
            const today = new Date().toISOString().slice(0, 10);
            const todayLog = logs.find(l => l.date === today);

            if (todayLog) {
                document.getElementById('habit-smoked').checked = todayLog.smoked_cigarettes;
                document.getElementById('habit-sweets').checked = todayLog.ate_sweets;
                document.getElementById('habit-brushed').checked = todayLog.brushed_after_meal;
                document.getElementById('habit-floss').checked = todayLog.used_floss;
                document.getElementById('habit-sensodyne').checked = todayLog.used_sensodyne;

                // Lock form since today is already saved (no popup — only on fresh save)
                this.lockForm();
            }
        } catch (e) {
            console.error('Load today log error:', e);
        }
    }

    async loadHistory() {
        const token = this.getAuthToken();
        const grid = document.getElementById('habit-history-grid');
        if (!grid) return;

        const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
        const today = new Date();
        const todayStr = today.toISOString().slice(0, 10);

        // Always build the 7-day skeleton first
        const days = [];
        for (let i = 6; i >= 0; i--) {
            const d = new Date();
            d.setDate(d.getDate() - i);
            days.push({ date: d, log: null });
        }

        // If user is logged in, fetch data
        let logs = [];
        if (token) {
            try {
                const response = await fetch('/habits/history', {
                    headers: { 'Authorization': 'Bearer ' + token }
                });
                if (response.ok) {
                    logs = await response.json();
                    // Match logs to days
                    days.forEach(day => {
                        const dateStr = day.date.toISOString().slice(0, 10);
                        day.log = logs.find(l => l.date === dateStr) || null;
                    });
                }
            } catch (e) {
                console.error('Load history error:', e);
            }
        }

        // Render grid (always shows 7 day columns)
        grid.innerHTML = days.map(day => {
            const label = dayNames[day.date.getDay()];
            const dateNum = day.date.getDate();
            const dateStr = day.date.toISOString().slice(0, 10);
            const isToday = dateStr === todayStr;
            const todayCls = isToday ? ' today' : '';

            if (!day.log) {
                const emptyLabel = isToday ? 'Today' : '—';
                return `
                    <div class="habit-day-cell${todayCls}">
                        <div class="habit-day-label">${label}</div>
                        <div class="habit-day-date">${dateNum}</div>
                        <div class="habit-day-score none">${emptyLabel}</div>
                    </div>`;
            }

            // Calculate score: good habits add points, bad habits subtract
            let score = 0;
            if (day.log.brushed_after_meal) score++;
            if (day.log.used_floss) score++;
            if (day.log.used_sensodyne) score++;
            if (!day.log.smoked_cigarettes) score++;
            if (!day.log.ate_sweets) score++;

            let cls = 'poor';
            if (score >= 5) cls = 'excellent';
            else if (score >= 4) cls = 'good';
            else if (score >= 3) cls = 'average';

            return `
                <div class="habit-day-cell${todayCls}">
                    <div class="habit-day-label">${label}</div>
                    <div class="habit-day-date">${dateNum}</div>
                    <div class="habit-day-score ${cls}" title="${score}/5">${score}</div>
                </div>`;
        }).join('');

        // Update streak
        this.updateStreak(logs);
    }

    updateStreak(logs) {
        const streakEl = document.getElementById('habit-streak-count');
        if (!streakEl) return;

        let streak = 0;
        const today = new Date();

        for (let i = 0; i < 30; i++) {
            const d = new Date(today);
            d.setDate(d.getDate() - i);
            const dateStr = d.toISOString().slice(0, 10);
            const log = logs.find(l => l.date === dateStr);

            if (log) {
                let goodCount = 0;
                if (log.brushed_after_meal) goodCount++;
                if (log.used_floss) goodCount++;
                if (log.used_sensodyne) goodCount++;
                if (!log.smoked_cigarettes) goodCount++;
                if (!log.ate_sweets) goodCount++;

                if (goodCount >= 3) streak++;
                else break;
            } else {
                if (i === 0) continue;
                break;
            }
        }

        streakEl.textContent = streak;

        // Update achievement level badge
        this.updateLevelBadge(streak);
    }

    /**
     * Get the user's level based on streak count
     */
    getLevel(streak) {
        let level = this.levels[0];
        for (const l of this.levels) {
            if (streak >= l.min) level = l;
        }
        return level;
    }

    /**
     * Update the achievement level badge next to streak
     */
    updateLevelBadge(streak) {
        const level = this.getLevel(streak);
        const badgeContainer = document.getElementById('habit-level-badge');
        if (badgeContainer) {
            badgeContainer.innerHTML = `<i class="fas ${level.icon} me-1"></i>${level.label}`;
            badgeContainer.style.color = level.color;
            badgeContainer.style.borderColor = level.color + '40';
            badgeContainer.style.background = level.color + '15';
        }

        // Update streak badge fire color based on level
        const streakBadge = document.getElementById('habit-streak-badge');
        if (streakBadge && streak >= 3) {
            const fireIcon = streakBadge.querySelector('.fa-fire');
            if (fireIcon) fireIcon.style.color = '#f59e0b';
        }
    }

    /**
     * Render the daily tip card based on today's date
     */
    renderDailyTip() {
        const tipContainer = document.getElementById('daily-tip-container');
        if (!tipContainer) return;

        const dayOfYear = Math.floor((new Date() - new Date(new Date().getFullYear(), 0, 0)) / 86400000);
        const tip = this.dailyTips[dayOfYear % this.dailyTips.length];

        tipContainer.innerHTML = `
            <div class="daily-tip-card">
                <div class="daily-tip-header">
                    <div class="daily-tip-icon" style="background: ${tip.color}15; color: ${tip.color};">
                        <i class="fas ${tip.icon}"></i>
                    </div>
                    <div>
                        <small class="daily-tip-label"><i class="fas fa-lightbulb me-1"></i>Tip of the Day</small>
                        <h6 class="fw-bold mb-0">${tip.title}</h6>
                    </div>
                </div>
                <p class="daily-tip-text">${tip.text}</p>
            </div>`;
    }

    /**
     * Check if the latest analysis had Gingivitis/Caries and show the Action Banner
     */
    checkForActionBanner() {
        const banner = document.getElementById('action-plan-banner');
        if (!banner) return;

        const data = this.getAnalysisData ? this.getAnalysisData() : null;
        if (!data || !data.final_analysis) {
            banner.classList.add('d-none');
            return;
        }

        // Check Model B results for conditions
        const analysisStr = JSON.stringify(data.final_analysis).toLowerCase();
        const hasGingivitis = analysisStr.includes('gingivitis');
        const hasCaries = analysisStr.includes('caries') || analysisStr.includes('cavity') || analysisStr.includes('cavities');
        const hasCalculus = analysisStr.includes('calculus');

        if (hasGingivitis || hasCaries || hasCalculus) {
            const detail = document.getElementById('action-plan-detail');
            const conditions = [];
            if (hasGingivitis) conditions.push('Gingivitis');
            if (hasCaries) conditions.push('Caries');
            if (hasCalculus) conditions.push('Calculus');
            detail.textContent = `Detected: ${conditions.join(', ')}. Click for your personalized augmentation plan.`;

            banner.classList.remove('d-none');
        } else {
            banner.classList.add('d-none');
        }
    }

    async openActionPlanChat() {
        const modalEl = document.getElementById('actionPlanModal');
        if (!modalEl) return;

        const modal = new bootstrap.Modal(modalEl);
        modal.show();

        const responseEl = document.getElementById('action-plan-response');
        responseEl.innerHTML = `
            <div class="text-center py-5">
                <div class="spinner-border text-primary mb-3" role="status"></div>
                <p class="text-muted">Generating your personalized care plan...</p>
            </div>`;

        // Build context from analysis data
        const data = this.getAnalysisData ? this.getAnalysisData() : {};
        const message = "Based on my latest oral scan results, please create a detailed personalized oral care improvement plan. Include specific recommendations for brushing, flossing, diet changes, and products I should use. Format it clearly with sections.";

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message, context: data }),
            });

            if (!response.ok) throw new Error('Chat failed');

            const result = await response.json();

            // Parse markdown if available
            if (window.marked) {
                responseEl.innerHTML = marked.parse(result.reply);
            } else {
                responseEl.innerHTML = `<div style="white-space: pre-wrap;">${result.reply}</div>`;
            }
        } catch (error) {
            console.error('Action Plan Error:', error);
            responseEl.innerHTML = `
                <div class="text-center py-4">
                    <i class="fas fa-exclamation-circle text-danger fa-2x mb-3"></i>
                    <p class="text-muted">Failed to generate plan. Please try the chat widget instead.</p>
                </div>`;
        }
    }

    showStatus(message, type) {
        const el = document.getElementById('habit-save-status');
        if (!el) return;

        const color = type === 'success' ? '#10b981' : '#ef4444';
        const icon = type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle';
        el.innerHTML = `<span style="color: ${color};"><i class="fas ${icon} me-1"></i>${message}</span>`;

        setTimeout(() => { el.innerHTML = ''; }, 4000);
    }
}
