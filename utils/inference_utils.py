import torch
import torch.nn.functional as F

def predict_with_tta(model, image, device):
    """
    Perform Test Time Augmentation (TTA) by averaging predictions 
    from original, horizontal flip, vertical flip, and 90-degree rotation.
    
    Args:
        model: PyTorch model
        image: Input tensor (1, C, H, W) or (C, H, W)
        device: torch device
        
    Returns:
        Averaged probabilities
    """
    model.eval()
    
    # Ensure image has batch dimension
    if image.dim() == 3:
        image = image.unsqueeze(0)
        
    image = image.to(device)
    
    with torch.no_grad():
        # 1. Original
        out1 = F.softmax(model(image), dim=1)
        
        # 2. Horizontal Flip
        img_hflip = torch.flip(image, [3])
        out2 = F.softmax(model(img_hflip), dim=1)
        
        # 3. Vertical Flip
        img_vflip = torch.flip(image, [2])
        out3 = F.softmax(model(img_vflip), dim=1)
        
        # 4. Rotate 90 degrees
        img_rot90 = torch.rot90(image, 1, [2, 3])
        out4 = F.softmax(model(img_rot90), dim=1)
    
    # Average the probabilities
    final_pred = (out1 + out2 + out3 + out4) / 4.0
    
    return final_pred
