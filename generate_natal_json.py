import json
import re
import os
import glob
import sys
import unicodedata

# Asegurar que el encoding sea utf-8 para todo
sys.stdout.reconfigure(encoding='utf-8')

def generate_json_from_markdown(data_dir: str = "data"):
    """
    Genera el archivo natal_map.json leyendo TODOS los archivos markdown en la carpeta data.
    """
    print(f"🚀 Iniciando generación de JSON desde {data_dir}/*.md...")
    
    natal_map = {}
    header_pattern = re.compile(r'^(#{2,3})\s+(.+)$')
    
    files = glob.glob(os.path.join(data_dir, "*.md"))
    files.sort()
    
    print(f"📂 Se encontraron {len(files)} archivos markdown.")
    
    processed_count = 0
    total_entries = 0
    
    for file_path in files:
        filename = os.path.basename(file_path)
        
        if filename.startswith("Maestro_") or filename.startswith("MAESTRO_") or filename.startswith("Títulos"):
            continue
            
        print(f"📄 Procesando: {filename}...")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            lines = content.split('\n')
            current_h2 = ""
            current_h3 = ""
            current_text = []
            
            for line in lines:
                line = line.strip()
                match = header_pattern.match(line)
                
                if match:
                    if current_h3 and current_text:
                        full_key = current_h3.lower().strip()
                        text_content = "\n".join(current_text).strip()
                        
                        if text_content:
                            keys_to_add = _expand_compound_key(full_key)
                            for k in keys_to_add:
                                natal_map[k] = {
                                    "titulo": current_h3,
                                    "texto": text_content,
                                    "tipo": _inferir_tipo(k),
                                    "archivo": filename
                                }
                                total_entries += 1
                                # Debug específico para confirmar corrección
                                if "sol" in k and "saturno" in k and "sextil" in k:
                                    print(f"  ✅ KEY GENERADA: {k}")
                    
                    level = match.group(1)
                    title = match.group(2).strip()
                    
                    if level == "##":
                        current_h2 = title
                        current_h3 = ""
                    elif level == "###":
                        current_h3 = title
                    
                    current_text = []
                else:
                    if current_h3:
                        current_text.append(line)
            
            # Procesar el último bloque
            if current_h3 and current_text:
                full_key = current_h3.lower().strip()
                text_content = "\n".join(current_text).strip()
                if text_content:
                    keys_to_add = _expand_compound_key(full_key)
                    for k in keys_to_add:
                        natal_map[k] = {
                            "titulo": current_h3,
                            "texto": text_content,
                            "tipo": _inferir_tipo(k),
                            "archivo": filename
                        }
                        total_entries += 1
                        if "sol" in k and "saturno" in k and "sextil" in k:
                            print(f"  ✅ KEY GENERADA: {k}")
                    
            processed_count += 1
            
        except Exception as e:
            print(f"❌ Error leyendo {filename}: {e}")

    output_path = os.path.join(data_dir, "natal_map.json")
    print(f"💾 Guardando {len(natal_map)} interpretaciones en {output_path}...")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(natal_map, f, indent=2, ensure_ascii=False)
        
    print("✅ Generación completada con éxito.")

def _expand_compound_key(key: str) -> list[str]:
    """
    Expande claves compuestas.
    Normaliza entrada a NFC para comparar chars correctamente.
    """
    key = unicodedata.normalize('NFC', key)
    
    # Si contiene " y " es una regla compleja condicional, NO expandir.
    if " y " in key:
        return [key]
    
    # Lista de aspectos conocidos
    aspectos = ["conjunción", "oposición", "cuadratura", "trígono", "sextil"]
    aspectos = [unicodedata.normalize('NFC', a) for a in aspectos]
    
    # 1. Detectar si es compuesta por " o " / " u "
    if " o " in key or " u " in key:
        
        # 2. Identificar qué aspectos están presentes
        presentes = [a for a in aspectos if a in key]
        
        if len(presentes) > 1:
            # 3. Intentar separar [Planeta + Aspectos] de [Planeta 2]
            # Usar regex para ' a ' con espacios flexibles
            # 'sol sextil o trígono a saturno' -> ['sol sextil o trígono', 'saturno']
            parts = re.split(r'\s+a\s+', key)
            
            if len(parts) >= 2:
                # Tomamos la última parte como el planeta 2
                p2 = parts[-1].strip()
                
                # Todo lo anterior es la parte 1
                p1_section = " a ".join(parts[:-1]).strip()
                
                # Extraer el nombre del Planeta 1 (primera palabra)
                words = p1_section.split()
                if not words: return [key] 
                p1 = words[0]
                
                expanded = []
                for asp in presentes:
                    new_key = f"{p1} {asp} a {p2}"
                    expanded.append(new_key)
                
                return expanded

    return [key]

def _inferir_tipo(key):
    key = key.lower()
    if "casa" in key: return "PlanetaEnCasa"
    if "conjunción" in key or "oposición" in key or "cuadratura" in key or "trígono" in key or "sextil" in key:
        return "Aspecto"
    if "en" in key: return "PlanetaEnSigno"
    return "General"

if __name__ == "__main__":
    generate_json_from_markdown()
