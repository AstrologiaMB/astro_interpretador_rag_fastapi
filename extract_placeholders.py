#!/usr/bin/env python3
"""
Extrae todos los placeholders (YYYY, WWW, etc.) de los archivos Markdown
y genera un CSV para revisión/edición.
"""

import re
import csv
import glob
import os

def extract_placeholders(data_dir: str = "data"):
    """Extrae placeholders de todos los archivos .md"""
    
    results = []
    placeholder_pattern = re.compile(r'\([A-Z]{2,}\)')
    
    # Buscar todos los archivos .md (excepto en subcarpetas)
    files = glob.glob(os.path.join(data_dir, "*.md"))
    
    for file_path in sorted(files):
        filename = os.path.basename(file_path)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line_num, line in enumerate(lines, 1):
            # Buscar placeholders en la línea
            if placeholder_pattern.search(line):
                # Limpiar la línea (quitar saltos de línea, etc.)
                clean_line = line.strip()
                
                results.append({
                    'archivo': filename,
                    'linea': line_num,
                    'texto_original': clean_line,
                    'texto_nuevo': ''  # Vacío para que el usuario lo llene
                })
    
    return results

def main():
    results = extract_placeholders()
    
    # Guardar en CSV
    output_file = "placeholders_para_editar.csv"
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['archivo', 'linea', 'texto_original', 'texto_nuevo'])
        writer.writeheader()
        writer.writerows(results)
    
    print(f"✅ Extraídos {len(results)} placeholders")
    print(f"💾 Guardado en: {output_file}")
    print(f"\n📋 Instrucciones:")
    print(f"   1. Abre {output_file} en Excel o editor de texto")
    print(f"   2. En la columna 'texto_nuevo' escribe el texto corregido (sin placeholders)")
    print(f"   3. Guarda el archivo")
    print(f"   4. Ejecuta: python apply_placeholders.py")

if __name__ == "__main__":
    main()