
import re

def normalize_title(t):
    return t.replace('#', '').strip().lower()

def main():
    markdown_path = "/Users/apple/astro_interpretador_rag_fastapi/data/20 - tránsitos.md"
    index_path = "/Users/apple/astro_interpretador_rag_fastapi/data/Títulos normalizados minusculas.txt"
    
    # 1. Extract Master List from Markdown
    print("Extracting titles from Markdown...")
    extracted_titles = []
    
    with open(markdown_path, 'r', encoding='utf-8') as f:
        for line in f:
            stripped = line.strip()
            if stripped.startswith('#'):
                # It's a header!
                title = normalize_title(stripped)
                if title:
                    extracted_titles.append(title)
                    
    print(f"Extracted {len(extracted_titles)} titles from markdown.")
    
    # 2. Read Index File
    print("Reading Indes File...")
    with open(index_path, 'r', encoding='utf-8') as f:
        index_lines = [l.rstrip() for l in f.readlines()]
        
    # 3. Find Boundaries
    start_idx = -1
    end_idx = -1
    
    for i, line in enumerate(index_lines):
        norm = line.strip().lower()
        if norm == 'tránsitos' and start_idx == -1:
            start_idx = i
        
        if norm == 'proluna' and start_idx != -1:
            end_idx = i
            break
            
    if start_idx == -1:
        print("❌ CRITICAL ERROR: Could not find 'tránsitos' start anchor.")
        return
        
    if end_idx == -1:
        # Maybe it ends at EOF?
        print("WARNING: Could not find 'proluna' end anchor. Assuming end of file.")
        end_idx = len(index_lines)

    print(f"Section detected: Lines {start_idx+1} to {end_idx} (Exclusive of end)")
    print(f"Replacing {end_idx - start_idx} existing lines with {len(extracted_titles)} new lines.")
    
    # 4. Construct New Content
    # Keep everything BEFORE start_idx
    new_content = index_lines[:start_idx]
    
    # Add extracted titles
    new_content.extend(extracted_titles)
    
    # Add everything FROM end_idx onwards
    new_content.extend(index_lines[end_idx:])
    
    # 5. Write Back
    with open(index_path, 'w', encoding='utf-8') as f:
        for line in new_content:
            f.write(line + "\n")
            
    print(f"✅ Successfully updated index. Total lines: {len(new_content)}")

if __name__ == "__main__":
    main()
