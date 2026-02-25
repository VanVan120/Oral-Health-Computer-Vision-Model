/**
 * Preventative Care Hub - Habits Tracker Module
 * Handles habit logging, history display, and action plan banner.
 */
export class HabitsUI {
    constructor(getAnalysisDataFn) {
        this.getAnalysisData = getAnalysisDataFn;
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
            // Close modal and open the chat widget
            const modal = bootstrap.Modal.getInstance(document.getElementById('actionPlanModal'));
            if (modal) modal.hide();
            const chatToggle = document.getElementById('chat-toggle-btn') || document.querySelector('.chat-toggle');
            if (chatToggle) chatToggle.click();
        };

        // Load existing data if user is logged in
        this.loadTodayLog();
        this.loadHistory();
    }

    getUserId() {
        // Try to get user_id from localStorage (set by auth system)
        const userData = localStorage.getItem('user');
        if (userData) {
            try {
                const user = JSON.parse(userData);
                return user.user_id || user.id;
            } catch (e) { /* ignore */ }
        }
        // Fallback: check for user_id directly
        return localStorage.getItem('user_id');
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
        const userId = this.getUserId();
        if (!userId) {
            this.showStatus('Please log in to save your habits.', 'error');
            return;
        }

        const btn = document.getElementById('btn-save-habits');
        const originalText = btn.innerHTML;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Saving...';
        btn.disabled = true;

        const payload = {
            user_id: parseInt(userId),
            smoked_cigarettes: document.getElementById('habit-smoked')?.checked || false,
            ate_sweets: document.getElementById('habit-sweets')?.checked || false,
            brushed_after_meal: document.getElementById('habit-brushed')?.checked || false,
            used_floss: document.getElementById('habit-floss')?.checked || false,
            used_sensodyne: document.getElementById('habit-sensodyne')?.checked || false,
        };

        try {
            const response = await fetch('/habits/log', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.detail || 'Failed to save');
            }

            this.showStatus('Habits saved successfully!', 'success');
            this.loadHistory();
        } catch (error) {
            console.error('Habit Save Error:', error);
            this.showStatus('Failed to save. ' + error.message, 'error');
        } finally {
            btn.innerHTML = originalText;
            btn.disabled = false;
        }
    }

    async loadTodayLog() {
        const userId = this.getUserId();
        if (!userId) return;

        try {
            const response = await fetch(`/habits/history/${userId}`);
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
            }
        } catch (e) {
            console.error('Load today log error:', e);
        }
    }

    async loadHistory() {
        const userId = this.getUserId();
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
        if (userId) {
            try {
                const response = await fetch(`/habits/history/${userId}`);
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
                // Count as a streak day if at least 3 good habits
                let goodCount = 0;
                if (log.brushed_after_meal) goodCount++;
                if (log.used_floss) goodCount++;
                if (log.used_sensodyne) goodCount++;
                if (!log.smoked_cigarettes) goodCount++;
                if (!log.ate_sweets) goodCount++;

                if (goodCount >= 3) streak++;
                else break;
            } else {
                if (i === 0) continue; // Today might not be logged yet
                break;
            }
        }

        streakEl.textContent = streak;
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
