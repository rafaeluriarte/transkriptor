import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.image_analyzer import ImageAnalyzer

@pytest.fixture
def image_analyzer():
    """Create an ImageAnalyzer instance for testing."""
    return ImageAnalyzer()

@pytest.fixture
def sample_image_path(tmp_path):
    """Create a temporary image file for testing."""
    image_path = tmp_path / "test_image.jpg"
    image_path.touch()
    return image_path

@patch("src.image_analyzer.Image.open")
def test_analyze_image(mock_image_open, image_analyzer, sample_image_path):
    """Test basic image analysis functionality."""
    # Setup mock image
    mock_image = MagicMock()
    mock_image_open.return_value = mock_image
    mock_image.size = (800, 600)
    
    # Execute
    result = image_analyzer.analyze_image(sample_image_path)
    
    # Assert
    mock_image_open.assert_called_once_with(sample_image_path)
    assert isinstance(result, dict)
    assert "dimensions" in result
    assert result["dimensions"] == (800, 600)

@patch("src.image_analyzer.Image.open")
def test_analyze_image_error_handling(mock_image_open, image_analyzer, sample_image_path):
    """Test error handling when image analysis fails."""
    # Setup
    mock_image_open.side_effect = Exception("Failed to open image")
    
    # Execute and assert
    with pytest.raises(Exception, match="Failed to open image"):
        image_analyzer.analyze_image(sample_image_path)

@patch("src.image_analyzer.Image.open")
def test_batch_analyze_images(mock_image_open, image_analyzer, tmp_path):
    """Test analyzing multiple images in batch."""
    # Setup
    image_paths = [
        tmp_path / "image1.jpg",
        tmp_path / "image2.jpg",
        tmp_path / "image3.jpg"
    ]
    for path in image_paths:
        path.touch()
    
    mock_image = MagicMock()
    mock_image.size = (800, 600)
    mock_image_open.return_value = mock_image
    
    # Execute
    results = image_analyzer.batch_analyze_images(image_paths)
    
    # Assert
    assert len(results) == len(image_paths)
    assert all(isinstance(result, dict) for result in results)
    assert mock_image_open.call_count == len(image_paths)

def test_invalid_image_path(image_analyzer):
    """Test handling of non-existent image path."""
    invalid_path = Path("nonexistent.jpg")
    
    with pytest.raises(FileNotFoundError):
        image_analyzer.analyze_image(invalid_path)

@patch("src.image_analyzer.Image.open")
def test_image_metadata_extraction(mock_image_open, image_analyzer, sample_image_path):
    """Test extraction of image metadata."""
    # Setup
    mock_image = MagicMock()
    mock_image_open.return_value = mock_image
    mock_image.size = (800, 600)
    mock_image.format = "JPEG"
    mock_image.info = {"dpi": (72, 72)}
    
    # Execute
    result = image_analyzer.analyze_image(sample_image_path)
    
    # Assert
    assert "format" in result
    assert result["format"] == "JPEG"
    assert "dpi" in result
    assert result["dpi"] == (72, 72) 