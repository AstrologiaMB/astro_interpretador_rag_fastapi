
import re

def check_structure(filepath):
    print(f"Checking structure for: {filepath}")
    
    issues = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    last_header_level = 0
    in_code_block = False
    
    header_regex = re.compile(r'^(#+)(.*)')
    
    for i, line in enumerate(lines):
        linenum = i + 1
        stripped = line.strip()
        
        # Skip logic
        if not stripped: continue
        
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            continue
            
        if in_code_block: continue
        
        # Header Check
        match = header_regex.match(stripped)
        if match:
            level = len(match.group(1))
            text = match.group(2)
            
            # Rule 1: Space after #
            if not text.startswith(' '):
                issues.append(f"Line {linenum}: Header missing space after # -> '{stripped}'")
                
            # Rule 2: Hierarchy Jump (optional strictness)
            # Allowed: 1 -> 2, 2 -> 3, 3 -> 4, or 3 -> 2 (up), 3 -> 3 (same)
            # Bad: 2 -> 4 (skip level)
            if level > last_header_level + 1 and last_header_level != 0:
                 # Note: Not strictly an error in some MD flavors, but bad practice
                 issues.append(f"Line {linenum}: Hierarchy skip from H{last_header_level} to H{level} -> '{stripped}'")
            
            last_header_level = level
        else:
            # Content line check
            # Rule 3: Line starting with # but not being a header (e.g. "#Text") handled by regex above partially
            # but let's check for "confusing" lines
            if stripped.startswith('#') and ' ' not in stripped[0:2]:
                 issues.append(f"Line {linenum}: Potential malformed header -> '{stripped}'")
            
            # Rule 4: Suspicious "Title Case" lines that aren't headers?
            # heuristic: short line, capitalized words, no punctuation at end, followed by text?
            # Too noisy for now.
            pass

    if not issues:
        print("✅ No structural issues found!")
    else:
        print(f"❌ Found {len(issues)} potential issues:")
        for issue in issues:
            print(f"  - {issue}")

if __name__ == "__main__":
    check_structure("/Users/apple/astro_interpretador_rag_fastapi/data/20 - tránsitos.md")
