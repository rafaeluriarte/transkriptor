import logging
from pathlib import Path
from typing import List, Dict, Any
import base64
from PIL import Image
import io

logger = logging.getLogger(__name__)

class ImageAnalyzer:
    """Class for analyzing images and preparing them for LLM processing."""
    
    def __init__(self, sample_size: int = 5):
        """
        Initialize the image analyzer.
        
        Args:
            sample_size: Number of images to sample for analysis
        """
        self.sample_size = sample_size
        
    def sample_images(self, image_paths: List[Path]) -> List[Path]:
        """
        Sample a subset of images for analysis.
        
        Args:
            image_paths: List of paths to images
            
        Returns:
            List of sampled image paths
        """
        from src.utils import sample_files
        
        logger.info(f"Sampling {self.sample_size} images from {len(image_paths)} total images")
        return sample_files(image_paths, self.sample_size)
    
    def encode_image_to_base64(self, image_path: Path) -> str:
        """
        Encode an image to base64 for API transmission.
        
        Args:
            image_path: Path to the image
            
        Returns:
            Base64 encoded image string
        """
        try:
            # Open and resize image if needed
            with Image.open(image_path) as img:
                # Resize if the image is too large
                max_size = 1024
                if max(img.size) > max_size:
                    ratio = max_size / max(img.size)
                    new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
                    img = img.resize(new_size, Image.LANCZOS)
                
                # Convert to bytes
                buffer = io.BytesIO()
                img.save(buffer, format="JPEG")
                
            # Encode to base64
            return base64.b64encode(buffer.getvalue()).decode('utf-8')
            
        except Exception as e:
            logger.error(f"Error encoding image {image_path}: {e}")
            raise
    
    def prepare_images_for_llm(self, image_paths: List[Path]) -> List[Dict[str, Any]]:
        """
        Prepare images for LLM analysis.
        
        Args:
            image_paths: List of paths to images
            
        Returns:
            List of image data dictionaries ready for LLM API
        """
        logger.info(f"Preparing {len(image_paths)} images for LLM analysis")
        
        image_data = []
        for path in image_paths:
            try:
                base64_image = self.encode_image_to_base64(path)
                image_data.append({
                    "path": str(path),
                    "base64": base64_image
                })
            except Exception as e:
                logger.error(f"Error preparing image {path}: {e}")
                
        return image_data 