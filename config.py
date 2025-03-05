import os
from pathlib import Path
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"

# Create directories if they don't exist
INPUT_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# LLM Configuration
# LLM_API_KEY = os.getenv("LLM_API_KEY")
# LLM_API_URL = os.getenv("LLM_API_URL", "https://api.openai.com/v1/chat/completions")
# LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4-vision-preview")

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = BASE_DIR / "transcription_agent.log"

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

# Sample size for image analysis
SAMPLE_SIZE = 5

# Material types for prompting
MATERIAL_TYPES = [
    "Monographs/Journals",
    "Exhibition/Museum catalogs",
    "Inventories or lists",
    "Diaries",
    "Historical Photographs",
    "Photograph catalog index cards",
    "Other Archival material"
]

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-vision-preview")
MAX_TOKENS = 1000

# Supported Image Formats
SUPPORTED_IMAGE_FORMATS = ['.jpg', '.jpeg', '.png']  # Add more if needed 