import argparse
import logging
import json
from pathlib import Path
import os
import sys

from config import (
    INPUT_DIR, OUTPUT_DIR, OPENAI_API_KEY, 
    OPENAI_MODEL, MAX_TOKENS, SAMPLE_SIZE, MATERIAL_TYPES
)
from src.agent import TranscriptionAgent
from src.pdf_processor import PDFProcessor
from src.image_analyzer import ImageAnalyzer
from src.llm_interface import LLMInterface

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

logger = logging.getLogger(__name__)

def main():
    """Main entry point for the transcription agent."""
    
    print("=== DEBUG: Script started ===")
    
    try:
        print("Starting transcription agent...")
        
        # Use environment variables or default paths
        input_dir = os.getenv("TRANSCRIPTOR_INPUT", "./data")
        output_dir = os.getenv("TRANSCRIPTOR_OUTPUT", "./output")
        
        print(f"DEBUG: Input directory: {input_dir}")
        print(f"DEBUG: Output directory: {output_dir}")
        
        # Convert to Path objects
        input_dir = Path(input_dir)
        output_dir = Path(output_dir)
        
        # Create output directory
        output_dir.mkdir(exist_ok=True)
        
        # Check for API key
        print(f"DEBUG: Checking API key...")
        if not OPENAI_API_KEY:
            raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")
        print(f"Using API key: {OPENAI_API_KEY[:10]}...")
        
        print("DEBUG: Initializing components...")
        # Initialize components
        pdf_processor = PDFProcessor(output_dir)
        image_analyzer = ImageAnalyzer(sample_size=SAMPLE_SIZE)
        llm_interface = LLMInterface(
            api_key=OPENAI_API_KEY,
            api_url="https://api.openai.com/v1/chat/completions",
            model=OPENAI_MODEL
        )
        
        print("DEBUG: Creating agent...")
        # Initialize agent
        agent = TranscriptionAgent(
            llm_interface=llm_interface,
            pdf_processor=pdf_processor,
            image_analyzer=image_analyzer,
            material_types=MATERIAL_TYPES,
            sample_size=SAMPLE_SIZE
        )
        
        print("DEBUG: Processing input...")
        # Process input
        result = agent.process_input(input_dir)
        
        # Save result to file
        result_file = output_dir / "analysis_result.json"
        with open(result_file, "w") as f:
            json.dump(result, f, indent=2)
        
        # Display analysis to user
        print("\n" + "="*80)
        print("DOCUMENT MATERIAL ANALYSIS")
        print("="*80 + "\n")
        print(result["analysis"])
        print("\n" + "="*80)
        print(f"Analysis saved to: {result_file}")
        
    except Exception as e:
        print(f"=== ERROR: {str(e)} ===")
        logger.error(f"Error in transcription agent: {e}", exc_info=True)
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 