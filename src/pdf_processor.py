import logging
from pathlib import Path
from typing import List
import tempfile
from pdf2image import convert_from_path

logger = logging.getLogger(__name__)

class PDFProcessor:
    """Class for processing PDF files into images."""
    
    def __init__(self, output_dir: Path):
        """
        Initialize the PDF processor.
        
        Args:
            output_dir: Directory to save extracted images
        """
        self.output_dir = output_dir
        self.output_dir.mkdir(exist_ok=True)
        
    def convert_pdf_to_images(self, pdf_path: Path) -> List[Path]:
        """
        Convert a PDF file to a list of images.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of paths to the extracted images
        """
        logger.info(f"Converting PDF to images: {pdf_path}")
        
        try:
            # Create a subfolder for this PDF's images
            pdf_name = pdf_path.stem
            image_dir = self.output_dir / pdf_name
            image_dir.mkdir(exist_ok=True)
            
            # Convert PDF to images
            images = convert_from_path(pdf_path)
            
            # Save images
            image_paths = []
            for i, image in enumerate(images):
                image_path = image_dir / f"page_{i+1}.jpg"
                image.save(image_path, "JPEG")
                image_paths.append(image_path)
                
            logger.info(f"Extracted {len(image_paths)} images from {pdf_path}")
            return image_paths
            
        except Exception as e:
            logger.error(f"Error converting PDF to images: {e}")
            raise 