
import os
import re
from pathlib import Path

def scan_markdown_headers(data_dir):
    """
    Escanea todos los archivos .md en el directorio y extrae los encabezados,
    limpiándolos para que coincidan con el formato normalizado.
    """
    headers = set()
    
    # Patrón para machear headers markdown (#, ##, ###)
    # Buscamos headers de nivel 1, 2 y 3 (o más?)
    # El usuario menciona títulos como "sol en aries", que suelen ser H3 (###) o H2.
    header_pattern = re.compile(r'^(#{1,6})\s+(.+)$')
    
    files = sorted(Path(data_dir).glob('*.md'))
    
    print(f"📂 Escaneando {len(files)} archivos Markdown en {data_dir}...")
    
    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                match = header_pattern.match(line)
                if match:
                    header_text = match.group(2).strip().lower()
                    # Normalizaciones básicas que seguramente hizo el usuario
                    # Quitar caracteres especiales si los hubiera, etc.
                    # En su index actual se ve bastante limpio.
                    headers.add(header_text)
                    
    return headers

def load_existing_index(index_path):
    titles = set()
    if os.path.exists(index_path):
        with open(index_path, 'r', encoding='utf-8') as f:
            for line in f:
                t = line.strip().lower()
                if t:
                    titles.add(t)
    return titles

def main():
    base_dir = "/Users/apple/astro_interpretador_rag_fastapi/data"
    index_file = os.path.join(base_dir, "Títulos normalizados minusculas.txt")
    
    print("--- 🔍 Iniciando Auditoría de Títulos ---")
    
    # 1. Escanear MDs reales
    real_headers = scan_markdown_headers(base_dir)
    print(f"✅ Encontrados {len(real_headers)} títulos únicos en los archivos Markdown.")
    
    # 2. Cargar índice manual actual
    manual_titles = load_existing_index(index_file)
    print(f"📋 El archivo índice actual tiene {len(manual_titles)} títulos.")
    
    # 3. Comparar
    missing_in_md = manual_titles - real_headers
    missing_in_index = real_headers - manual_titles
    
    print("\n--- 📊 Resultados ---")
    
    if not missing_in_md and not missing_in_index:
        print("✨ ¡PERFECTO! El índice manual coincide exactamente con los headers de los archivos.")
        print(">>> Puedes borrar el archivo de texto sin miedo.")
    else:
        if missing_in_md:
            print(f"\n⚠️  HAY {len(missing_in_md)} TÍTULOS EN EL ÍNDICE QUE NO EXISTEN EN LOS MDs (Riesgo de perderlos):")
            for t in sorted(list(missing_in_md))[:10]:
                print(f"   - '{t}'")
            if len(missing_in_md) > 10: print(f"   ... y {len(missing_in_md)-10} más.")
            
        if missing_in_index:
            print(f"\nℹ️  HAY {len(missing_in_index)} HEADERS NUEVOS EN LOS MDs QUE NO ESTABAN EN EL ÍNDICE:")
            for t in sorted(list(missing_in_index))[:10]:
                print(f"   + '{t}'")
                
    print("\n-------------------------------------------")

if __name__ == "__main__":
    main()
