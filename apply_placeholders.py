#!/usr/bin/env python3
"""
Aplica los cambios del CSV editado a los archivos Markdown originales.
"""

import csv
import os
from collections import defaultdict

def apply_changes(csv_file: str = "placeholders_para_editar.csv", data_dir: str = "data"):
    """Aplica los cambios del CSV a los archivos Markdown"""
    
    # Leer el CSV
    changes_by_file = defaultdict(list)
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            archivo = row['archivo']
            linea = int(row['linea'])
            texto_original = row['texto_original']
            texto_nuevo = row['texto_nuevo'].strip()
            
            # Solo procesar si hay un texto nuevo
            if texto_nuevo:
                changes_by_file[archivo].append({
                    'linea': linea,
                    'original': texto_original,
                    'nuevo': texto_nuevo
                })
    
    if not changes_by_file:
        print("⚠️ No hay cambios para aplicar (columna 'texto_nuevo' vacía)")
        return
    
    # Aplicar cambios archivo por archivo
    total_changes = 0
    for archivo, cambios in changes_by_file.items():
        file_path = os.path.join(data_dir, archivo)
        
        if not os.path.exists(file_path):
            print(f"❌ No se encontró: {file_path}")
            continue
        
        # Leer archivo
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Aplicar cambios (líneas son 1-indexed en el CSV)
        applied = 0
        for cambio in cambios:
            line_idx = cambio['linea'] - 1
            if line_idx < len(lines):
                # Verificar que el contenido coincide
                original_line = lines[line_idx].strip()
                csv_original = cambio['original'].strip()
                
                if original_line == csv_original:
                    lines[line_idx] = cambio['nuevo'] + '\n'
                    applied += 1
                    print(f"✅ {archivo}:{cambio['linea']} - Cambio aplicado")
                else:
                    print(f"⚠️ {archivo}:{cambio['linea']} - El contenido no coincide:")
                    print(f"   Esperado: {csv_original[:50]}...")
                    print(f"   Encontrado: {original_line[:50]}...")
            else:
                print(f"❌ {archivo}:{cambio['linea']} - Número de línea fuera de rango")
        
        # Guardar archivo modificado
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        total_changes += applied
        print(f"💾 {archivo}: {applied} cambios aplicados\n")
    
    print(f"✅ Total de cambios aplicados: {total_changes}")
    print(f"\n📝 Siguientes pasos:")
    print(f"   1. Regenerar natal_map.json: python generate_natal_json.py")
    print(f"   2. Reiniciar el servidor RAG")
    print(f"   3. Probar la carta nuevamente")

if __name__ == "__main__":
    apply_changes()