import os
import re
import json
import unicodedata

DATA_DIR = "data/draco"
OUTPUT_FILE = "data/draco.json"

def normalize_key(text):
    text = text.lower().strip()
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    text = re.sub(r'[^\w\s]', '', text) # Remove punctuation
    text = re.sub(r'\s+', '_', text)     # Replace spaces with underscores
    return text.strip('_')

def parse_markdown_file(filepath):
    interpretations = {}
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    # Stack for headers: [h1_text, h2_text, h3_text, ...]
    # But wait, logic should be:
    # A text block belongs to the sequence of headers above it.
    
    header_stack = []
    current_text = []
    
    # We need to track header levels.
    # Assumes standard markdown: #, ##, ###, etc.
    
    for line in lines:
        stripped = line.strip()
        
        if stripped.startswith('#'):
            # It's a header
            # Save previous section if exists
            if header_stack and current_text:
                full_key = "_".join([normalize_key(h) for h in header_stack])
                # Special handling: If keys become too long or repetitive?
                # The existing keys were just concatenated.
                interpretations[full_key] = "\n".join(current_text).strip()
                current_text = []

            # Determine new level
            level = 0
            for char in stripped:
                if char == '#':
                    level += 1
                else:
                    break
            
            header_text = stripped.lstrip('#').strip()
            
            # Update stack
            # If level is deeper than stack, append.
            # If level is shallow/equal, pop until correct level.
            # Stack index 0 is H1 (level 1), index 1 is H2 (level 2).
            
            while len(header_stack) >= level:
                header_stack.pop()
            
            header_stack.append(header_text)
            
        elif stripped:
            if header_stack: # Only accumulate if we are under a header
                current_text.append(stripped)
    
    # Save last section
    if header_stack and current_text:
        full_key = "_".join([normalize_key(h) for h in header_stack])
        interpretations[full_key] = "\n".join(current_text).strip()
        
    return interpretations

def main():
    all_data = {}
    
    # List files sorted
    files = sorted([f for f in os.listdir(DATA_DIR) if f.endswith('.md')])
    
    print(f"Found {len(files)} markdown files in {DATA_DIR}")
    
    for filename in files:
        filepath = os.path.join(DATA_DIR, filename)
        print(f"Parsing {filename}...")
        data = parse_markdown_file(filepath)
        print(f"  -> {len(data)} keys found.")
        all_data.update(data)
        
    print(f"\nTotal keys generated: {len(all_data)}")
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)
        
    print(f"Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
