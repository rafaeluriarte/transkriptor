# Transcriptor

## Overview

Transcriptor is an AI-supported document transcription software designed for historical documents. It processes a collection of documents by generating structured descriptions, analyzing their content, and refining prompts for improved transcription accuracy. The system consists of a series of intelligent agents that assist in the document transcription workflow.

This is the first implemented agent, designed to test the feasibility of a fully automated transcription process. Additional agents will be implemented in the future to complete the workflow.

## Features

### Implemented Agent Functions

1. **Process PDFs into Images (if needed)**
2. **Sample Representative Images**
   - Selects 5 images: first two pages and three randomly sampled pages.
3. **Analyze Material using GPT-4 or Claude**
4. **Generate a Detailed Description including:**
   - Language
   - Time Period
   - Material Type
   - Format (Handwritten/Printed)
   - Layout Characteristics
   - Sequential Dependencies
   - Transcription Challenges

## Workflow

### User Input

- Provide a folder containing images (PDF or JPG).
- Default data folder is `data/`. 

### Processing Steps

1. **Describe the Material**

   - Convert PDFs into images (if applicable).
   - Select 5 representative images.
   - Send images to GPT-4 or Claude for material analysis.
   - The analysis includes the classification of the document as one of the following:
     - Monographs/Journals
     - Exhibition/Museum Catalogs
     - Inventories or Lists
     - Diaries
     - Historical Photographs
     - Photograph Catalog Index Cards
     - Other Archival Material
   - Extract information regarding language, period, type, handwriting vs. print, format, layout, sequencing, dependencies, and transcription challenges.
   - Display results to the user.

2. **Generate the Prompt for Transcription**

   - The agent refines the prompt based on document characteristics.

3. **Generate Ground Truth**

   - Initial transcription is produced.

4. **User Evaluation and Correction**

   - Users review and correct transcription outputs.

5. **Refine Prompt Based on Corrections**

   - Adjustments are made to improve accuracy.
   
6. **Process the Entire Collection**

   - The system applies refined parameters to transcribe all documents.

## Future Agents

Additional agents will be implemented to enhance the system:
1. **Transcription Agent** - Uses refined prompts to generate transcriptions.
2. **Verification Agent** - Cross-checks transcriptions against reference texts.
3. **Correction Agent** - Suggests corrections based on user feedback.
4. **Formatting Agent** - Ensures proper structuring of transcribed text.
5. **Metadata Extraction Agent** - Extracts metadata such as author, date, and location.

## Requirements

- Python 3.8+
- OpenAI API Key
- PDF2Image library dependencies (if processing PDFs)
- See `requirements.txt` for the full list

## Configuration

Edit `.env` to modify settings (a template is provided in the repository):

- Sample size (default: 5)
- Supported file types
- Material categories
- Model parameters
- API keys

## TODO

- Multi-page documents where context from one page affects another.
- Sequential images (e.g., books, inventories).
- Recto/Verso document handling (common in photographs and manuscripts).
- Small grouped images representing one conceptual object (e.g., multi-page correspondence).

## How to Run

1. Place the input files (PDFs or images) into the `data/` folder.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables in `.env`.
4. Run the main script:
   ```bash
   python main.py
   ```

The system will process the documents, analyze them, and guide the user through transcription and refinement.

---

This project aims to create a robust and scalable document transcription pipeline adaptable to a wide range of archival and historical materials.

