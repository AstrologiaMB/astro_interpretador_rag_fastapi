import re
import json
import os

# Configuration
CONTENT_DIR = "/Users/apple/astrochat/astro_interpretador_rag_fastapi/data/content"
OUTPUT_DIR = "/Users/apple/astrochat/astro_interpretador_rag_fastapi/data"

SOURCE_MAP = {
    "source_natal.md": "natal.json",
    "source_transits.md": "transitos.json",
    "source_progresiones.md": "progresiones.json",
    "source_proluna.md": "proluna.json"
}

def normalize_key(text):
    """
    Converts a header text into a standardized snake_case key.
    Example: "Sol en Aries" -> "sol_en_aries"
    """
    text = text.lower().strip()
    text = re.sub(r'[*\(\)]', '', text)  # Remove special chars
    text = re.sub(r'\s+', '_', text)     # Replace spaces with underscores
    text = re.sub(r'_+', '_', text)      # Deduplicate underscores
    return text.strip('_')

def parse_markdown_file(filepath):
    """
    Parses a single Markdown file and extracts interpretation snippets.
    Returns a dictionary mapping standardized keys to interpretation text.
    """
    interpretations = {}
    current_key_parts = []
    current_text = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for line in lines:
        stripped = line.strip()
        
        # Header Detection
        if stripped.startswith('#'):
            # Save previous section if exists
            if current_key_parts and current_text:
                full_key = "_".join(current_key_parts)
                interpretations[full_key] = "\n".join(current_text).strip()
            
            # Reset for new section
            # level = len(line.split()[0]) # Count format of hashtags e.g., '###' is 3
            header_text = normalize_key(stripped.lstrip('#').strip())
            
            # Logic: If level 1 (#), reset key parts. If level 2 (##), append? 
            # For this simple implementation, we assume FLATTENED keys based on the last header seen.
            # This matches the previous logic where headers were quite descriptive.
            # If "sol_en_aries" is unique, this is fine.
            
            current_key_parts = [header_text] 
            current_text = []

        elif stripped:
            # Accumulate text
            current_text.append(stripped)
            
    # Save last section
    if current_key_parts and current_text:
        full_key = "_".join(current_key_parts)
        interpretations[full_key] = "\n".join(current_text).strip()
        
    return interpretations

def main():
    if not os.path.exists(CONTENT_DIR):
        print(f"Error: Content directory {CONTENT_DIR} not found.")
        return

    for source_file, output_json in SOURCE_MAP.items():
        input_path = os.path.join(CONTENT_DIR, source_file)
        output_path = os.path.join(OUTPUT_DIR, output_json)
        
        if os.path.exists(input_path):
            print(f"Processing {source_file} -> {output_json}...")
            data = parse_markdown_file(input_path)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"  - Extracted {len(data)} items to {output_json}.")
        else:
            print(f"Warning: Source file {source_file} not found. Skipping.")

if __name__ == "__main__":
    main()
