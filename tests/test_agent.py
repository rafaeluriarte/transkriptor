import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

from src.agent import TranscriptionAgent

@pytest.fixture
def mock_components():
    """Create mock components for testing."""
    llm_interface = MagicMock()
    pdf_processor = MagicMock()
    image_analyzer = MagicMock()
    
    return {
        "llm_interface": llm_interface,
        "pdf_processor": pdf_processor,
        "image_analyzer": image_analyzer,
        "material_types": ["Type1", "Type2"],
        "sample_size": 2
    }

@pytest.fixture
def agent(mock_components):
    """Create a TranscriptionAgent instance with mock components."""
    return TranscriptionAgent(**mock_components)

def test_process_input_with_pdfs(agent, mock_components, tmp_path):
    """Test processing input with PDF files."""
    # Setup
    pdf_path = tmp_path / "test.pdf"
    pdf_path.touch()
    
    # Mock return values
    mock_components["pdf_processor"].convert_pdf_to_images.return_value = [
        Path("image1.jpg"), Path("image2.jpg")
    ]
    mock_components["image_analyzer"].sample_images.return_value = [Path("image1.jpg")]
    mock_components["image_analyzer"].prepare_images_for_llm.return_value = [{"path": "image1.jpg", "base64": "data"}]
    mock_components["llm_interface"].analyze_images.return_value = {"choices": [{"message": {"content": "Analysis"}}]}
    mock_components["llm_interface"].extract_analysis_text.return_value = "Analysis"
    
    # Mock utility functions
    with patch("src.agent.validate_input_path", return_value=tmp_path):
        with patch("src.agent.get_file_list") as mock_get_files:
            mock_get_files.side_effect = [[pdf_path], []]  # First call for PDFs, second for images
            
            # Execute
            result = agent.process_input(str(tmp_path))
    
    # Assert
    assert result["total_pdfs"] == 1
    assert result["total_images"] == 2
    assert result["analysis"] == "Analysis"
    mock_components["pdf_processor"].convert_pdf_to_images.assert_called_once_with(pdf_path)
    mock_components["image_analyzer"].sample_images.assert_called_once()
    mock_components["llm_interface"].analyze_images.assert_called_once()

def test_process_input_with_images(agent, mock_components, tmp_path):
    """Test processing input with image files."""
    # Setup
    image_path = tmp_path / "test.jpg"
    image_path.touch()
    
    # Mock return values
    mock_components["image_analyzer"].sample_images.return_value = [image_path]
    mock_components["image_analyzer"].prepare_images_for_llm.return_value = [{"path": str(image_path), "base64": "data"}]
    mock_components["llm_interface"].analyze_images.return_value = {"choices": [{"message": {"content": "Analysis"}}]}
    mock_components["llm_interface"].extract_analysis_text.return_value = "Analysis"
    
    # Mock utility functions
    with patch("src.agent.validate_input_path", return_value=tmp_path):
        with patch("src.agent.get_file_list") as mock_get_files:
            mock_get_files.side_effect = [[], [image_path]]  # First call for PDFs, second for images
            
            # Execute
            result = agent.process_input(str(tmp_path))
    
    # Assert
    assert result["total_pdfs"] == 0
    assert result["total_images"] == 1
    assert result["analysis"] == "Analysis"
    mock_components["pdf_processor"].convert_pdf_to_images.assert_not_called()
    mock_components["image_analyzer"].sample_images.assert_called_once()
    mock_components["llm_interface"].analyze_images.assert_called_once()

def test_process_input_no_files(agent, mock_components, tmp_path):
    """Test processing input with no files."""
    # Mock utility functions
    with patch("src.agent.validate_input_path", return_value=tmp_path):
        with patch("src.agent.get_file_list") as mock_get_files:
            mock_get_files.side_effect = [[], []]  # No PDFs, no images
            
            # Execute and assert
            with pytest.raises(FileNotFoundError):
                agent.process_input(str(tmp_path)) 