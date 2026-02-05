import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models, transforms
from PIL import Image
import numpy as np
import os
import cv2
import base64
from io import BytesIO
from stain_utils import MacenkoNormalizer
from yolo_visualizer import CellSegmentationVisualizer

# --- 1. Model Architecture (Must match Training Notebook) ---

# Class names for the 3-class detection
CLASS_NAMES = {
    0: 'Mitotic Figures',
    1: 'Multiple Nucleol',
    2: 'Nuclear Hyperchromatism'
}

class OSCCMultiTaskModel(nn.Module):
    """
    Multi-Task Model for OSCC Cell Feature Detection
    
    Tasks:
    1. TVNT: Binary classification (Abnormality detected vs Normal)
    2. Mitotic Figures Count: Regression
    3. Multiple Nucleol Count: Regression
    4. Nuclear Hyperchromatism Count: Regression
    """
    def __init__(self):
        super().__init__()
        self.backbone = models.densenet169(weights=None)  # Pretrained not needed for inference
        num_ftrs = self.backbone.classifier.in_features
        self.backbone.classifier = nn.Identity()
        
        # TVNT Head (Binary Classification)
        self.head_tvnt = nn.Sequential(
            nn.Linear(num_ftrs, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 2)
        )
        
        # Mitotic Figures Count (Regression)
        self.head_mitotic = nn.Sequential(
            nn.Linear(num_ftrs, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, 1)
        )
        
        # Multiple Nucleol Count (Regression)
        self.head_nucleol = nn.Sequential(
            nn.Linear(num_ftrs, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, 1)
        )
        
        # Nuclear Hyperchromatism Count (Regression)
        self.head_hyperchrom = nn.Sequential(
            nn.Linear(num_ftrs, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, 1)
        )

    def forward(self, x):
        features = self.backbone.features(x)
        pooled = F.relu(features, inplace=False)
        pooled = F.adaptive_avg_pool2d(pooled, (1, 1))
        pooled = torch.flatten(pooled, 1)
        
        return {
            'tvnt': self.head_tvnt(pooled),
            'mitotic': self.head_mitotic(pooled),
            'nucleol': self.head_nucleol(pooled),
            'hyperchrom': self.head_hyperchrom(pooled)
        }

# --- 2. Inference Wrapper Class ---

class ModelAInference:
    def __init__(self, model_path="model_a.pth", device=None):
        self.device = device if device else torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Loading Model A from {model_path} on {self.device}...")
        
        self.model = OSCCMultiTaskModel()
        if os.path.exists(model_path):
            self.model.load_state_dict(torch.load(model_path, map_location=self.device, weights_only=False), strict=False)
            print("Model weights loaded successfully.")
        else:
            print(f"WARNING: Model file {model_path} not found. Using random weights.")
            
        self.model.to(self.device)
        self.model.eval()
        
        # Initialize Stain Normalizer
        self.normalizer = MacenkoNormalizer()
        
        # Initialize YOLO Visualizer (for bounding box segmentation)
        try:
            self.yolo_visualizer = CellSegmentationVisualizer()
        except:
            print("⚠️ YOLO visualizer not available, using Grad-CAM only")
            self.yolo_visualizer = None
        
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

    def generate_heatmap(self, img_tensor, pred_score):
        """Generates Grad-CAM heatmap."""
        # Hook to capture feature maps and gradients
        gradients = []
        activations = []
        
        def backward_hook(module, grad_input, grad_output):
            gradients.append(grad_output[0])
            
        def forward_hook(module, input, output):
            activations.append(output)
            
        # Hook into the last dense block of DenseNet169
        target_layer = self.model.backbone.features.norm5 
        
        handle_f = target_layer.register_forward_hook(forward_hook)
        handle_b = target_layer.register_full_backward_hook(backward_hook)
        
        # Zero grads
        self.model.zero_grad()
        
        # We need to re-run forward pass to ensure hooks capture this specific image
        # (The previous forward pass in predict() was inside no_grad context)
        # Enable grad temporarily for Grad-CAM
        with torch.enable_grad():
            output = self.model(img_tensor)
            score = output['tvnt']
            target_class = torch.argmax(score)
            score[:, target_class].backward()
        
        # Generate Heatmap
        grads = gradients[0].cpu().data.numpy().squeeze()
        fmaps = activations[0].cpu().data.numpy().squeeze()
        
        weights = np.mean(grads, axis=(1, 2))
        cam = np.zeros(fmaps.shape[1:], dtype=np.float32)
        for i, w in enumerate(weights):
            cam += w * fmaps[i]
            
        cam = np.maximum(cam, 0)
        cam = cv2.resize(cam, (224, 224))
        cam = cam - np.min(cam)
        cam = cam / np.max(cam)
        
        # Cleanup
        handle_f.remove()
        handle_b.remove()
        
        return cam

    def predict(self, image_path):
        """
        Runs inference on a single image.
        Returns a dictionary of predictions for 3-class cell feature detection.
        """
        try:
            image = Image.open(image_path).convert("RGB")
            
            # Apply Stain Normalization
            img_np = np.array(image)
            try:
                img_norm_np = self.normalizer.normalize(img_np)
                image_norm = Image.fromarray(img_norm_np)
            except Exception as e:
                print(f"Warning: Stain normalization failed ({e}). Using original image.")
                image_norm = image

            img_tensor = self.transform(image_norm).unsqueeze(0).to(self.device)
            
            with torch.no_grad():
                outputs = self.model(img_tensor)
                
            # Process Outputs
            tvnt_prob = F.softmax(outputs['tvnt'], dim=1)[0]
            
            # Confidence Threshold Check
            confidence_score = float(tvnt_prob[1].item()) if tvnt_prob[1].item() > tvnt_prob[0].item() else float(tvnt_prob[0].item())
            
            if confidence_score < 0.55:
                 return {
                    "status": "error",
                    "message": "The uploaded image does not appear to be a valid histopathological sample. Confidence too low."
                }

            # Abnormality detection (any of the 3 classes present)
            abnormality_detected = tvnt_prob[1].item() > 0.5
            
            # Get counts for each class (ensure non-negative)
            # Raw outputs from regression heads
            raw_mitotic = outputs['mitotic'].item()
            raw_nucleol = outputs['nucleol'].item()
            raw_hyperchrom = outputs['hyperchrom'].item()
            
            print(f"[DEBUG] Raw outputs - Mitotic: {raw_mitotic:.4f}, Nucleol: {raw_nucleol:.4f}, Hyperchrom: {raw_hyperchrom:.4f}")
            
            mitotic_count = max(0, int(round(raw_mitotic)))
            nucleol_count = max(0, int(round(raw_nucleol)))
            hyperchrom_count = max(0, int(round(raw_hyperchrom)))
            
            # Total abnormal cells count
            total_abnormal = mitotic_count + nucleol_count + hyperchrom_count
            
            # Generate Heatmap (if abnormality detected)
            heatmap_b64 = None
            original_b64 = None
            segmentation_b64 = None  # For YOLO bounding boxes
            
            if abnormality_detected:
                heatmap = self.generate_heatmap(img_tensor, outputs['tvnt'])
                
                # Create Grad-CAM Overlay
                img_resized = image.resize((224, 224))
                img_np = np.array(img_resized)
                heatmap_color = cv2.applyColorMap(np.uint8(255 * heatmap), cv2.COLORMAP_JET)
                heatmap_color = cv2.cvtColor(heatmap_color, cv2.COLOR_BGR2RGB)
                
                overlay = cv2.addWeighted(img_np, 0.6, heatmap_color, 0.4, 0)
                
                # Convert Grad-CAM to Base64
                pil_img = Image.fromarray(overlay)
                buff = BytesIO()
                pil_img.save(buff, format="JPEG")
                heatmap_b64 = base64.b64encode(buff.getvalue()).decode("utf-8")

                buff_orig = BytesIO()
                img_resized.save(buff_orig, format="JPEG")
                original_b64 = base64.b64encode(buff_orig.getvalue()).decode("utf-8")
                
                # Generate YOLO Segmentation (bounding boxes for individual cells)
                if self.yolo_visualizer:
                    try:
                        yolo_result = self.yolo_visualizer.detect_and_visualize(image_path)
                        if yolo_result["status"] == "success":
                            segmentation_b64 = yolo_result["segmentation_overlay"]
                            print(f"[INFO] YOLO detections: {yolo_result['detection_details']}")
                    except Exception as e:
                        print(f"[WARNING] YOLO segmentation failed: {e}")

            return {
                "status": "success",
                "predictions": {
                    "abnormality_detected": abnormality_detected,
                    "confidence": float(confidence_score),
                    "mitotic_figures_count": mitotic_count,
                    "multiple_nucleol_count": nucleol_count,
                    "nuclear_hyperchromatism_count": hyperchrom_count,
                    "total_abnormal_cells": total_abnormal,
                    "heatmap_overlay": heatmap_b64,
                    "segmentation_overlay": segmentation_b64,  # NEW: YOLO bounding boxes
                    "original_resized": original_b64
                }
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    # Test run
    inference = ModelAInference()
    # Create a dummy image for testing
    dummy_img_path = "test_patch.jpg"
    Image.new('RGB', (224, 224), color='red').save(dummy_img_path)
    
    result = inference.predict(dummy_img_path)
    print("Test Prediction:", result)
    os.remove(dummy_img_path)
