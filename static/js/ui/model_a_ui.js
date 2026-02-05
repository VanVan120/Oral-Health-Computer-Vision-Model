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
            
            // Store segmentation overlay (YOLO bounding boxes)
            if (preds.predictions.segmentation_overlay) {
                this.maSegmentationSrc = "data:image/jpeg;base64," + preds.predictions.segmentation_overlay;
            } else {
                this.maSegmentationSrc = "";
            }
            
            // Show/hide segmentation button based on availability
            const btnSeg = document.getElementById('ma-btn-segmentation');
            if (btnSeg) {
                if (this.maSegmentationSrc) {
                    btnSeg.style.display = 'inline-block';
                } else {
                    btnSeg.style.display = 'none';
                }
            }
            
            if (preds.predictions.heatmap_overlay) {
                this.maHeatmapSrc = "data:image/jpeg;base64," + preds.predictions.heatmap_overlay;
                document.getElementById('ma-heatmap-controls').style.display = 'flex';
                // Auto-show segmentation (bounding boxes) if available, otherwise heatmap
                if (preds.predictions.abnormality_detected) {
                    if (this.maSegmentationSrc) {
                        this.switchImage('segmentation');
                    } else {
                        this.switchImage('heatmap');
                    }
                } else {
                    this.switchImage('original');
                }
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
        if (p.abnormality_detected) {
            badge.className = 'status-badge danger';
            badge.innerHTML = '<i class="fas fa-exclamation-triangle"></i> ' + t('abnormalityDetected', 'Abnormality Detected');
        } else {
            badge.className = 'status-badge success';
            badge.innerHTML = '<i class="fas fa-check-circle"></i> ' + t('noAbnormality', 'No Abnormality');
        }

        const probPct = (p.confidence * 100).toFixed(1);
        document.getElementById('ma-prob-value').textContent = probPct + '%';
        document.getElementById('ma-prob-bar').style.width = probPct + '%';
        
        // New 3-class cell feature counts
        document.getElementById('ma-mitotic-value').textContent = p.mitotic_figures_count;
        document.getElementById('ma-nucleol-value').textContent = p.multiple_nucleol_count;
        document.getElementById('ma-hyperchrom-value').textContent = p.nuclear_hyperchromatism_count;
        document.getElementById('ma-total-value').textContent = p.total_abnormal_cells;
    }

    switchImage(type) {
        const img = document.getElementById('ma-image-preview');
        const btnOrig = document.getElementById('ma-btn-original');
        const btnHeat = document.getElementById('ma-btn-heatmap');
        const btnSeg = document.getElementById('ma-btn-segmentation');

        // Remove active from all buttons
        btnOrig.classList.remove('active');
        btnHeat.classList.remove('active');
        if (btnSeg) btnSeg.classList.remove('active');

        if (type === 'original') {
            img.src = this.maOriginalSrc;
            btnOrig.classList.add('active');
        } else if (type === 'segmentation' && this.maSegmentationSrc) {
            img.src = this.maSegmentationSrc;
            if (btnSeg) btnSeg.classList.add('active');
        } else {
            // Default to heatmap
            img.src = this.maHeatmapSrc;
            btnHeat.classList.add('active');
        }
    }
    
    getImageSrc() {
        return this.maHeatmapSrc ? this.maHeatmapSrc : this.maOriginalSrc;
    }
}
