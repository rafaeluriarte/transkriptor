import pytest
from pathlib import Path
from src.utils import sample_images

def test_sample_images():
    """Test the image sampling strategy."""
    # Create test data
    image_paths = [
        Path(f"image_{i}.jpg") for i in range(10)
    ]
    
    # Test with default sample size
    sampled = sample_images(image_paths)
    
    # Should return 5 images
    assert len(sampled) == 5
    
    # First two should be the first two from original list
    assert sampled[0] == image_paths[0]
    assert sampled[1] == image_paths[1]
    
    # Remaining should be from the rest of the images
    for img in sampled[2:]:
        assert img in image_paths[2:]

def test_sample_images_small_input():
    """Test sampling when input is smaller than sample size."""
    image_paths = [Path(f"image_{i}.jpg") for i in range(3)]
    
    sampled = sample_images(image_paths)
    
    # Should return all images if input is smaller than sample size
    assert len(sampled) == 3
    assert set(sampled) == set(image_paths)

def test_sample_images_alphabetical_order():
    """Test that first two images are selected in alphabetical order."""
    # Create test data in non-alphabetical order
    image_paths = [
        Path("zebra.jpg"),
        Path("banana.jpg"),
        Path("apple.jpg"),
        Path("cat.jpg"),
        Path("dog.jpg")
    ]
    
    sampled = sample_images(image_paths)
    
    # Should return 5 images
    assert len(sampled) == 5
    
    # First two should be alphabetically first
    assert sampled[0] == Path("apple.jpg")
    assert sampled[1] == Path("banana.jpg")
    
    # Remaining should be from the rest of the images
    for img in sampled[2:]:
        assert img in [Path("cat.jpg"), Path("dog.jpg"), Path("zebra.jpg")] 