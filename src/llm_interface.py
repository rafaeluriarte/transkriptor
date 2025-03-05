import logging
import requests
import json
from typing import List, Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class LLMInterface:
    """Interface for communicating with the LLM API."""
    
    def __init__(self, api_key: str, api_url: str, model: str):
        """
        Initialize the LLM interface.
        
        Args:
            api_key: API key for the LLM service
            api_url: URL for the LLM API
            model: Model name to use
        """
        self.api_key = api_key
        self.api_url = api_url
        self.model = model
        
    def create_analysis_prompt(self, material_types: List[str]) -> str:
        """
        Create a prompt for analyzing document images.
        
        Args:
            material_types: List of potential material types
            
        Returns:
            Formatted prompt string
        """
        prompt = (
            "Analyze these document images and describe the material in detail. "
            "Consider the following potential types:\n\n"
        )
        
        for material_type in material_types:
            prompt += f"- {material_type}\n"
            
        prompt += (
            "\nPlease provide the following information:\n"
            "1. Language of the document\n"
            "2. Time period/era\n"
            "3. Type of material (from the list above or other if applicable)\n"
            "4. Whether it's handwritten, printed, or both\n"
            "5. Format and layout description\n"
            "6. Sequencing information (page numbers, etc.)\n"
            "7. Dependencies on previous or other pages\n"
            "8. Potential challenges for transcription (what to be careful with)\n\n"
            "Provide a comprehensive analysis based on the sample images."
        )
        
        return prompt
    
    def analyze_images(self, image_data: List[Dict[str, Any]], material_types: List[str]) -> Dict[str, Any]:
        """
        Send images to LLM for analysis.
        
        Args:
            image_data: List of image data dictionaries
            material_types: List of potential material types
            
        Returns:
            LLM response
        """
        logger.info(f"Sending {len(image_data)} images to LLM for analysis")
        
        prompt = self.create_analysis_prompt(material_types)
        
        # Prepare the message content
        content = [
            {"type": "text", "text": prompt}
        ]
        
        # Add images to the content
        for img in image_data:
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{img['base64']}"
                }
            })
        
        # Prepare the API request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": content
                }
            ],
            "max_tokens": 1000
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error communicating with LLM API: {e}")
            raise
    
    def extract_analysis_text(self, response: Dict[str, Any]) -> str:
        """
        Extract the analysis text from the LLM response.
        
        Args:
            response: LLM API response
            
        Returns:
            Extracted analysis text
        """
        try:
            return response["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            logger.error(f"Error extracting analysis from LLM response: {e}")
            logger.debug(f"Response structure: {json.dumps(response, indent=2)}")
            raise ValueError("Invalid response format from LLM API") 