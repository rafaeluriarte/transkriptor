import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.pdf_processor import PDFProcessor

@pytest.fixture
def pdf_processor(tmp_path):
    """Create a PDFProcessor instance for testing."""
    return PDFProcessor(tmp_path)

def test_init_creates_output_dir(tmp_path):
    """Test that the output directory is created during initialization."""
    output_dir = tmp_path / "output"
    PDFProcessor(output_dir)
    assert output_dir.exists()

@patch("src.pdf_processor.convert_from_path")
def test_convert_pdf_to_images(mock_convert, pdf_processor, tmp_path):
    """Test converting PDF to images."""
    # Setup
    pdf_path = tmp_path / "test.pdf"
    pdf_path.touch()
    
    # Create mock images
    mock_image1 = MagicMock()
    mock_image2 = MagicMock()
    mock_convert.return_value = [mock_image1, mock_image2]
    
    # Execute
    result = pdf_processor.convert_pdf_to_images(pdf_path)
    
    # Assert
    mock_convert.assert_called_once_with(pdf_path)
    assert len(result) == 2
    assert all(isinstance(path, Path) for path in result)
    assert all(str(path).endswith(".jpg") for path in result)
    
    # Check that images were saved
    mock_image1.save.assert_called_once()
    mock_image2.save.assert_called_once()

@patch("src.pdf_processor.convert_from_path")
def test_convert_pdf_error_handling(mock_convert, pdf_processor, tmp_path):
    """Test error handling during PDF conversion."""
    # Setup
    pdf_path = tmp_path / "test.pdf"
    pdf_path.touch()
    
    # Make the conversion fail
    mock_convert.side_effect = Exception("PDF conversion failed")
    
    # Execute and assert
    with pytest.raises(Exception, match="PDF conversion failed"):
        pdf_processor.convert_pdf_to_images(pdf_path) 