import pytest
import torch
from utils.inference_utils import predict_with_tta
import torch.nn as nn

class DummyModel(nn.Module):
    def forward(self, x):
        # Return a tensor of shape [batch_size, num_classes]
        # In this dummy model, we just return zeros or fixed values
        # Since TTA takes softmax, we will just return a simple tensor
        # Let's say batch_size=1, classes=2
        return torch.tensor([[1.0, 0.0]]) * x.mean() # Arbitrary operation just to return correct shape

def test_predict_with_tta():
    # Arrange
    model = DummyModel()
    # Create a dummy image tensor (C, H, W)
    image = torch.rand(3, 224, 224)
    device = torch.device("cpu")
    
    # Act
    output = predict_with_tta(model, image, device)
    
    # Assert
    assert output is not None
    # We should get a batch dimension and 2 classes
    assert output.shape == (1, 2)
    # TTA averages probabilities (softmaxed), so sum should be ~1
    assert torch.isclose(output.sum(), torch.tensor(1.0), atol=1e-5)
    
def test_predict_with_tta_batch_dim():
    model = DummyModel()
    # Create image WITH batch dimension (1, C, H, W)
    image = torch.rand(1, 3, 224, 224)
    device = torch.device("cpu")
    
    output = predict_with_tta(model, image, device)
    assert output.shape == (1, 2)
