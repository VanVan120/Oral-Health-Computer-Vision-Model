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
                         
                         // Show feedback UI once insight generated
                         const fbContainer = document.getElementById('ai-suggestion-feedback-container-a');
                         if (fbContainer && localStorage.getItem('access_token')) {
                             fbContainer.classList.remove('d-none');
                             this.resetFeedbackUI();
                             this.bindFeedbackEvents("Model A");
                         }
                         
                     } catch (error) {
                         console.error("Error fetching suggestion:", error);
                         if (modalText) modalText.textContent = "Error loading suggestion.";
                     }
                } else {
                    if (modalText) modalText.textContent = this.currentSuggestion || "No analysis data available.";
                    const fbContainer = document.getElementById('ai-suggestion-feedback-container-a');
                    if (this.currentSuggestion && fbContainer && localStorage.getItem('access_token')) {
                         fbContainer.classList.remove('d-none');
                    }
                }
            }
        };

        if (adviceBtn) adviceBtn.addEventListener('click', showModal);
    }
    
    resetFeedbackUI() {
        const form = document.getElementById('ai-suggestion-correction-form-a');
        const btns = document.querySelectorAll('.feedback-btn-a');
        const container = document.getElementById('ai-suggestion-feedback-container-a');
        const input = document.getElementById('ai-suggestion-correction-input-a');
        const successMsg = document.getElementById('ai-suggestion-feedback-success-a');
        
        if (form) form.classList.add('d-none');
        if (input) input.value = '';
        if (successMsg) successMsg.remove();
        
        const btnGroup = document.getElementById('ai-suggestion-feedback-buttons-a');
        if (btnGroup) btnGroup.classList.remove('d-none');
        
        btns.forEach(b => {
             b.style.backgroundColor = 'rgba(255,255,255,0.02)';
             b.style.borderColor = 'rgba(255,255,255,0.15)';
             b.style.color = '';
             b.classList.remove('text-primary', 'text-danger');
             b.classList.add('text-secondary');
        });
    }

    bindFeedbackEvents(modelContext) {
        let isHelpful = null;
        const thumbsBtns = document.querySelectorAll('.feedback-btn-a');
        const correctionForm = document.getElementById('ai-suggestion-correction-form-a');
        const submitBtn = document.getElementById('submit-ai-suggestion-feedback-a');
        const correctionInput = document.getElementById('ai-suggestion-correction-input-a');
        const container = document.getElementById('ai-suggestion-feedback-container-a');
        const buttonsContainer = document.getElementById('ai-suggestion-feedback-buttons-a');

        // Note: use cloneNode to avoid duplicate event listeners if modal is opened multiple times
        thumbsBtns.forEach(btn => {
            const newBtn = btn.cloneNode(true);
            btn.parentNode.replaceChild(newBtn, btn);
            
            newBtn.addEventListener('click', (e) => {
                const target = e.currentTarget;
                isHelpful = target.dataset.helpful === "true";
                
                // Toggle active state styling
                document.querySelectorAll('.feedback-btn-a').forEach(b => {
                    b.style.backgroundColor = 'rgba(255,255,255,0.02)';
                    b.style.borderColor = 'rgba(255,255,255,0.15)';
                    b.style.color = '';
                    b.classList.remove('text-primary', 'text-danger');
                    b.classList.add('text-secondary');
                });
                
                if (isHelpful) {
                    target.classList.remove('text-secondary');
                    target.style.backgroundColor = 'rgba(16, 185, 129, 0.15)';
                    target.style.borderColor = 'rgba(16, 185, 129, 0.4)';
                    target.style.color = '#34d399'; // Emerald
                } else {
                    target.classList.remove('text-secondary');
                    target.style.backgroundColor = 'rgba(239, 68, 68, 0.15)';
                    target.style.borderColor = 'rgba(239, 68, 68, 0.4)';
                    target.style.color = '#f87171'; // Red
                }

                // Show correction form
                if (correctionForm) correctionForm.classList.remove('d-none');
            });
        });

        if (submitBtn) {
            const newSubmitBtn = submitBtn.cloneNode(true);
            submitBtn.parentNode.replaceChild(newSubmitBtn, submitBtn);
            
            newSubmitBtn.addEventListener('click', async (e) => {
                const btn = e.currentTarget;
                
                const prompt = `Provide an AI Insight Suggestion based on histopathological results for ${modelContext}.`;
                const responseText = this.currentSuggestion;
                const correction = correctionInput ? correctionInput.value.trim() : "";

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
                    if (correctionForm) correctionForm.classList.add('d-none');
                    if (buttonsContainer) buttonsContainer.classList.add('d-none');
                    container.innerHTML += `<div id="ai-suggestion-feedback-success-a" class="text-success mt-2" style="font-size: 14px;"><i class="fas fa-check-circle"></i> Insight Feedback Saved Successfully!</div>`;
                } catch (error) {
                    console.error("Feedback error:", error);
                    btn.innerText = "Error: " + error.message;
                    btn.disabled = false;
                }
            });
        }
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
            
            // Set background for blur effect
            document.getElementById('ma-viewport').style.backgroundImage = `url('${this.maOriginalSrc}')`;
            
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
            document.getElementById('ma-viewport').style.backgroundImage = `url('${this.maOriginalSrc}')`;
            btnOrig.classList.add('active');
        } else if (type === 'segmentation' && this.maSegmentationSrc) {
            img.src = this.maSegmentationSrc;
            // Keep background as original for context
             document.getElementById('ma-viewport').style.backgroundImage = `url('${this.maOriginalSrc}')`;
            if (btnSeg) btnSeg.classList.add('active');
        } else {
            // Default to heatmap
            img.src = this.maHeatmapSrc;
            document.getElementById('ma-viewport').style.backgroundImage = `url('${this.maHeatmapSrc}')`;
            btnHeat.classList.add('active');
        }
    }
    
    getImageSrc() {
        return this.maHeatmapSrc ? this.maHeatmapSrc : this.maOriginalSrc;
    }
}
