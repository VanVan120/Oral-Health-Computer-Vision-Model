import { APIService } from '../services/api.js';

export class ModelBUI {
    constructor() {
        this.currentSuggestion = null;
        this.lastPredictions = null;
        this.initModalListeners();
    }

    initModalListeners() {
        const adviceBtn = document.getElementById('btn-ai-advice-b');
        
        const showModal = async () => {
            const modalText = document.getElementById('ai-suggestion-text');
            const modalEl = document.getElementById('aiSuggestionModal');
            
            if (modalEl) {
                const modal = new bootstrap.Modal(modalEl);
                modal.show();
                
                if (!this.currentSuggestion && this.lastPredictions) {
                     if (modalText) modalText.textContent = "Generating AI suggestion...";
                     
                     try {
                         const data = await APIService.getSuggestion("Model B", this.lastPredictions);
                         
                         this.currentSuggestion = data.ai_suggestion;
                         if (modalText) modalText.textContent = this.currentSuggestion;
                         
                     } catch (error) {
                         console.error("Error fetching suggestion:", error);
                         if (modalText) modalText.textContent = "Error loading suggestion.";
                     }
                } else {
                    if (modalText) modalText.textContent = this.currentSuggestion || "No analysis data available.";
                }
            }
        };

        if (adviceBtn) adviceBtn.addEventListener('click', showModal);
    }

    show(data, file) {
        document.getElementById('triage-view').classList.add('hidden-section');
        document.getElementById('model-b-view').classList.remove('hidden-section');

        const reader = new FileReader();
        reader.onload = (e) => {
            const img = document.getElementById('mb-preview-image');
            img.src = e.target.result;
            
            img.onload = () => {
                this.drawBoxes(data.detections, img);
            };
        };
        reader.readAsDataURL(file);

        this.fillData(data);
    }

    fillData(data) {
        this.lastPredictions = data;
        this.currentSuggestion = null;
        this.lastDetections = data.detections; // Store for report generation

        // Helper function for translations
        const t = (key, fallback) => window.AppLanguage ? window.AppLanguage.t(key) : fallback;

        // Show Quality Note if present
        const qualityAlert = document.getElementById('mb-quality-note');
        const qualityText = document.getElementById('mb-quality-text');
        if (data.quality_note && qualityAlert && qualityText) {
            // Translate quality note if it matches known patterns
            let translatedNote = data.quality_note;
            if (data.quality_note.includes("Low Resolution")) {
                translatedNote = t('qualityNoteLowRes', 'Low Resolution. Switched to Standard Mode for better stability.');
            }
            qualityText.textContent = translatedNote;
            
            // Style based on content
            if (data.quality_note.includes("Low Resolution")) {
                qualityAlert.className = 'viewport-badge warning';
            } else {
                qualityAlert.className = 'viewport-badge';
            }
            qualityAlert.classList.remove('d-none');
        } else if (qualityAlert) {
            qualityAlert.classList.add('d-none');
        }

        const screenRes = document.getElementById('mb-screening-result');
        // Translate screening result
        const screeningResultKey = 'screeningResult' + data.screening_result.replace(/\s+/g, '');
        screenRes.textContent = t(screeningResultKey, data.screening_result);
        screenRes.className = `h3 fw-bold mb-0 ${data.screening_result === 'Normal' ? 'text-success' : 'text-danger'}`;

        const hygieneRes = document.getElementById('mb-hygiene-score');
        // Translate hygiene score
        const hygieneKey = 'hygieneScore' + data.hygiene_score;
        hygieneRes.textContent = t(hygieneKey, data.hygiene_score);
        let color = 'text-dark';
        if (data.hygiene_score === 'High') color = 'text-success';
        if (data.hygiene_score === 'Medium') color = 'text-warning';
        if (data.hygiene_score === 'Low') color = 'text-danger';
        hygieneRes.className = `h3 fw-bold mb-0 ${color}`;

        const list = document.getElementById('mb-findings-list');
        list.innerHTML = '';
        
        if (data.detections.length === 0) {
            list.innerHTML = `<div class="text-center text-muted py-5"><i class="fas fa-check-circle display-4 mb-3 text-success"></i><p>${t('noIssuesDetected', 'No specific issues detected.')}</p></div>`;
        } else {
            const counts = {};
            data.detections.forEach(d => counts[d.class] = (counts[d.class] || 0) + 1);
            
            for (const [cls, count] of Object.entries(counts)) {
                // Translate condition class name
                const conditionKey = 'condition' + cls.replace(/\s+/g, '');
                const translatedCls = t(conditionKey, cls);
                const detectedText = t('detectedCount', '{count} detected').replace('{count}', count);
                list.innerHTML += `
                    <div class="d-flex justify-content-between align-items-center p-3 bg-light rounded border">
                        <span class="fw-medium text-secondary">${translatedCls}</span>
                        <span class="badge bg-primary-subtle text-primary-emphasis rounded-pill">${detectedText}</span>
                    </div>`;
            }
        }
    }

    drawBoxes(detections, img) {
        const canvas = document.getElementById('mb-result-canvas');
        const ctx = canvas.getContext('2d');

        canvas.width = img.width;
        canvas.height = img.height;
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        const scaleX = img.width / img.naturalWidth;
        const scaleY = img.height / img.naturalHeight;

        detections.forEach(det => {
            const [x1, y1, x2, y2] = det.bbox;
            const sx = x1 * scaleX;
            const sy = y1 * scaleY;
            const sw = (x2 - x1) * scaleX;
            const sh = (y2 - y1) * scaleY;

            ctx.strokeStyle = '#EF4444';
            ctx.lineWidth = 4;
            ctx.strokeRect(sx, sy, sw, sh);

            ctx.fillStyle = '#EF4444';
            const text = `${det.class} ${Math.round(det.confidence * 100)}%`;
            ctx.font = 'bold 16px Inter, sans-serif';
            const textWidth = ctx.measureText(text).width;
            
            ctx.fillRect(sx, sy - 30, textWidth + 20, 30);

            ctx.fillStyle = '#FFFFFF';
            ctx.fillText(text, sx + 10, sy - 8);
        });
    }
    
    getImageSrc() {
        const img = document.getElementById('mb-preview-image');
        if (!this.lastDetections || !img) {
             return img ? img.src : null;
        }

        // Create a temporary canvas to draw the full-resolution annotated image
        const canvas = document.createElement('canvas');
        canvas.width = img.naturalWidth;
        canvas.height = img.naturalHeight;
        const ctx = canvas.getContext('2d');

        // 1. Draw original image
        ctx.drawImage(img, 0, 0);

        // 2. Draw boxes (using natural coordinates)
        this.lastDetections.forEach(det => {
            const [x1, y1, x2, y2] = det.bbox;
            const w = x2 - x1;
            const h = y2 - y1;

            // Scale styles relative to image size
            const scaleFactor = Math.max(1, img.naturalWidth / 1000);
            
            ctx.strokeStyle = '#EF4444';
            ctx.lineWidth = 4 * scaleFactor;
            ctx.strokeRect(x1, y1, w, h);

            // Draw Label Background
            ctx.fillStyle = '#EF4444';
            const text = `${det.class} ${Math.round(det.confidence * 100)}%`;
            
            const fontSize = Math.round(20 * scaleFactor);
            ctx.font = `bold ${fontSize}px Inter, sans-serif`;
            
            const textMetrics = ctx.measureText(text);
            const textWidth = textMetrics.width;
            const padding = 10 * scaleFactor;
            const boxHeight = fontSize + padding;
            
            ctx.fillRect(x1, y1 - boxHeight, textWidth + padding * 2, boxHeight);

            // Draw Label Text
            ctx.fillStyle = '#FFFFFF';
            ctx.fillText(text, x1 + padding, y1 - (padding / 2) - (fontSize * 0.1)); // Adjust baseline
        });

        return canvas.toDataURL('image/jpeg', 0.9);
    }
}
