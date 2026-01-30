import { APIService } from '../services/api.js';

export class ModelAUI {
    constructor() {
        this.maOriginalSrc = "";
        this.maHeatmapSrc = "";
        this.currentSuggestion = null;
        this.lastPredictions = null;
        this.initModalListeners();
    }

    initModalListeners() {
        const adviceBtn = document.getElementById('btn-ai-advice-a');
        
        const showModal = async () => {
            const modalText = document.getElementById('ai-suggestion-text-a');
            const modalEl = document.getElementById('aiSuggestionModalA');
            
            if (modalEl) {
                const modal = new bootstrap.Modal(modalEl);
                modal.show();
                
                if (!this.currentSuggestion && this.lastPredictions) {
                     if (modalText) modalText.textContent = "Generating AI suggestion...";
                     
                     try {
                         const data = await APIService.getSuggestion("Model A", this.lastPredictions);
                         
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

    show(preds, file) {
        this.lastPredictions = preds;
        this.currentSuggestion = null;

        document.getElementById('triage-view').classList.add('hidden-section');
        document.getElementById('model-a-view').classList.remove('hidden-section');

        const reader = new FileReader();
        reader.onload = (e) => {
            if (preds.predictions.original_resized) {
                this.maOriginalSrc = "data:image/jpeg;base64," + preds.predictions.original_resized;
            } else {
                this.maOriginalSrc = e.target.result;
            }
            
            document.getElementById('ma-image-preview').src = this.maOriginalSrc;
            
            if (preds.predictions.heatmap_overlay) {
                this.maHeatmapSrc = "data:image/jpeg;base64," + preds.predictions.heatmap_overlay;
                document.getElementById('ma-heatmap-controls').style.display = 'flex';
                this.switchImage('original');
            } else {
                this.maHeatmapSrc = "";
                document.getElementById('ma-heatmap-controls').style.display = 'none';
            }
        };
        reader.readAsDataURL(file);

        this.fillData(preds.predictions);
    }

    fillData(p) {
        // Helper function for translations
        const t = (key, fallback) => window.AppLanguage ? window.AppLanguage.t(key) : fallback;
        
        const badge = document.getElementById('ma-tumour-badge');
        if (p.tumour_detected) {
            badge.className = 'badge bg-danger fs-5 mb-2';
            badge.textContent = t('tumourDetected', 'Tumour Detected');
        } else {
            badge.className = 'badge bg-success fs-5 mb-2';
            badge.textContent = t('noTumour', 'No Tumour');
        }

        const probPct = (p.tumour_probability * 100).toFixed(1);
        document.getElementById('ma-prob-value').textContent = probPct + '%';
        document.getElementById('ma-prob-bar').style.width = probPct + '%';
        
        document.getElementById('ma-doi-value').textContent = p.depth_of_invasion_mm;
        document.getElementById('ma-poi-value').textContent = p.pattern_of_invasion;
        
        const pniEl = document.getElementById('ma-pni-value');
        pniEl.textContent = p.perineural_invasion ? t('detected', 'Detected') : t('notDetected', 'Not Detected');
        pniEl.style.color = p.perineural_invasion ? '#dc3545' : '#198754';

        document.getElementById('ma-tb-value').textContent = p.tumour_buds_count;
        document.getElementById('ma-mi-value').textContent = p.mitotic_figures_count;
    }

    switchImage(type) {
        const img = document.getElementById('ma-image-preview');
        const btnOrig = document.getElementById('ma-btn-original');
        const btnHeat = document.getElementById('ma-btn-heatmap');

        if (type === 'original') {
            img.src = this.maOriginalSrc;
            btnOrig.classList.add('active');
            btnHeat.classList.remove('active');
        } else {
            img.src = this.maHeatmapSrc;
            btnHeat.classList.add('active');
            btnOrig.classList.remove('active');
        }
    }
    
    getImageSrc() {
        return this.maHeatmapSrc ? this.maHeatmapSrc : this.maOriginalSrc;
    }
}
