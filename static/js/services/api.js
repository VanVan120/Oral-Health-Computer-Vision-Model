export class APIService {
    static async analyzeImage(file) {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });
        return await response.json();
    }

    static async generateReport(payload) {
        const response = await fetch('/generate-report', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error("Failed to generate report");
        }
        return await response.blob();
    }

    static async sendReportEmail(payload) {
        const response = await fetch('/api/send-report', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        
        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || "Failed to send email");
        }
        return await response.json();
    }

    static async sendChatMessage(message, context) {
        const payload = {
            message: message,
            context: context
        };

        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        return await response.json();
    }

    static async getSuggestion(modelType, analysisData) {
        const response = await fetch('/api/get-suggestion', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                model_type: modelType,
                analysis_data: analysisData
            })
        });
        return await response.json();
    }

    static async saveHabitLog(payload) {
        const response = await fetch('/habits/log', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || 'Failed to save habit log');
        }
        return await response.json();
    }

    static async getHabitHistory(userId) {
        const response = await fetch(`/habits/history/${userId}`);
        if (!response.ok) {
            throw new Error('Failed to fetch habit history');
        }
        return await response.json();
    }

    static async submitChatFeedback(payload) {
        const token = localStorage.getItem('access_token');
        if (!token) throw new Error("User must be logged in to provide feedback.");

        const response = await fetch('/api/chat/feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || 'Failed to submit feedback');
        }
        return await response.json();
    }
}
