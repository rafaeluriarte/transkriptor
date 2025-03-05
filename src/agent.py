import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Union, Tuple

from .pdf_processor import PDFProcessor
from .image_analyzer import ImageAnalyzer
from .llm_interface import LLMInterface
from .utils import validate_input_path, get_file_list

logger = logging.getLogger(__name__)

class TranscriptionAgent:
    """
    Agent that processes document images and provides material descriptions.
    """
    
    def __init__(
        self, 
        llm_interface: LLMInterface,
        pdf_processor: PDFProcessor,
        image_analyzer: ImageAnalyzer,
        material_types: List[str],
        sample_size: int = 5
    ):
        """
        Initialize the transcription agent.
        
        Args:
            llm_interface: Interface for LLM communication
            pdf_processor: Processor for PDF files
            image_analyzer: Analyzer for images
            material_types: List of potential material types
            sample_size: Number of images to sample for analysis
        """
        self.llm_interface = llm_interface
        self.pdf_processor = pdf_processor
        self.image_analyzer = image_analyzer
        self.material_types = material_types
        self.sample_size = sample_size
        
    def process_input(self, input_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Process input files and generate material description.
        
        Args:
            input_path: Optional path to input directory
            
        Returns:
            Dictionary with processing results
        """
        logger.info("Starting input processing")
        
        # Validate input path
        input_dir = validate_input_path(input_path)
        
        # Get PDF and image files
        pdf_files = get_file_list(input_dir, ["pdf"])
        image_files = get_file_list(input_dir, ["jpg", "jpeg", "png"])
        
        if not pdf_files and not image_files:
            logger.error(f"No PDF or image files found in {input_dir}")
            raise FileNotFoundError(f"No PDF or image files found in {input_dir}")
        
        # Process files
        all_images = []
        
        # Process PDFs if any
        for pdf_file in pdf_files:
            pdf_images = self.pdf_processor.convert_pdf_to_images(pdf_file)
            all_images.extend(pdf_images)
        
        # Add direct image files
        all_images.extend(image_files)
        
        # Sample images for analysis
        sampled_images = self.image_analyzer.sample_images(all_images)
        
        # Prepare images for LLM
        image_data = self.image_analyzer.prepare_images_for_llm(sampled_images)
        
        # Send to LLM for analysis
        llm_response = self.llm_interface.analyze_images(image_data, self.material_types)
        
        # Extract analysis text
        analysis_text = self.llm_interface.extract_analysis_text(llm_response)
        
        # Prepare result
        result = {
            "input_directory": str(input_dir),
            "total_pdfs": len(pdf_files),
            "total_images": len(all_images),
            "sampled_images": [str(img) for img in sampled_images],
            "analysis": analysis_text,
            "raw_response": llm_response
        }
        
        logger.info("Input processing completed successfully")
        return result 