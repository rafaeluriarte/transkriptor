import os
import logging
import random
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)

def validate_input_path(input_path: Optional[str] = None) -> Path:
    """
    Validate and return the input path.
    
    Args:
        input_path: Optional path to the input folder
        
    Returns:
        Path object for the validated input path
    """
    from config import INPUT_DIR
    
    if input_path:
        path = Path(input_path)
        if not path.exists():
            logger.error(f"Input path {path} does not exist")
            raise FileNotFoundError(f"Input path {path} does not exist")
        return path
    
    logger.info(f"Using default input directory: {INPUT_DIR}")
    return INPUT_DIR

def get_file_list(directory: Path, extensions: List[str]) -> List[Path]:
    """
    Get list of files with specified extensions from a directory.
    
    Args:
        directory: Path to the directory
        extensions: List of file extensions to include
        
    Returns:
        List of Path objects for matching files
    """
    files = []
    for ext in extensions:
        files.extend(directory.glob(f"*.{ext}"))
        files.extend(directory.glob(f"*.{ext.upper()}"))
    
    if not files:
        logger.warning(f"No files with extensions {extensions} found in {directory}")
    else:
        logger.info(f"Found {len(files)} files with extensions {extensions}")
    
    return files

def sample_files(files: List[Path], sample_size: int) -> List[Path]:
    """
    Sample a subset of files.
    
    Args:
        files: List of files to sample from
        sample_size: Number of files to sample
        
    Returns:
        List of sampled files
    """
    if len(files) <= sample_size:
        return files
    
    return random.sample(files, sample_size)

def sample_images(image_paths: List[Path], sample_size: int = 5) -> List[Path]:
    """
    Sample images using the strategy:
    - First 2 images alphabetically
    - 3 random images from the remaining ones
    
    Args:
        image_paths: List of paths to images
        sample_size: Total number of images to sample (default 5)
    
    Returns:
        List of sampled image paths
    """
    if len(image_paths) <= sample_size:
        return sorted(image_paths)
        
    # Sort paths alphabetically and take first 2
    sorted_paths = sorted(image_paths)
    first_images = sorted_paths[:2]
    
    # Get remaining images for random sampling
    remaining_images = sorted_paths[2:]
    
    # Randomly sample 3 more images
    random_images = random.sample(remaining_images, min(3, len(remaining_images)))
    
    return first_images + random_images 