#!/usr/bin/env python3
"""
Aplica los cambios del CSV frases_astrologicas_completas.csv a los archivos Markdown.
Hace backup automático antes de modificar.
"""

import csv
import glob
import os
import shutil
from datetime import datetime

def backup_files(data_dir: str = "data"):
    """Crea backup de todos los archivos .md"""
    backup_dir = f"data_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    backup_path = os.path.join(os.path.dirname(data_dir), backup_dir)
    
    os.makedirs(backup_path, exist_ok=True)
    
    md_files = glob.glob(os.path.join(data_dir, "*.md"))
    for md_file in md_files:
        filename = os.path.basename(md_file)
        shutil.copy2(md_file, os.path.join(backup_path, filename))
    
    print(f"💾 Backup creado en: {backup_path}")
    return backup_path

def apply_changes(csv_file: str = "frases_astrologicas_completas.csv", data_dir: str = "data"):
    """Aplica los cambios del CSV a los archivos Markdown"""
    
    print("🚀 APLICANDO CAMBIOS")
    print("=" * 80)
    
    # 1. Crear backup
    backup_path = backup_files(data_dir)
    
    # 2. Leer CSV
    frases = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)  # Saltar header
        for row in reader:
            if len(row) >= 2:
                original = row[0].strip()
                nuevo = row[1].strip()
                if original != nuevo:  # Solo procesar si hay cambio
                    frases.append({
                        'original': original,
                        'nuevo': nuevo
                    })
    
    print(f"📄 Total de cambios a aplicar: {len(frases)}")
    print()
    
    # 3. Aplicar cambios
    md_files = glob.glob(os.path.join(data_dir, "*.md"))
    aplicados = 0
    
    for frase_data in frases:
        original = frase_data['original']
        nuevo = frase_data['nuevo']
        
        for md_file in md_files:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if original in content:
                # Reemplazar
                new_content = content.replace(original, nuevo)
                
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                aplicados += 1
                filename = os.path.basename(md_file)
                print(f"✅ Aplicado en {filename}: {original[:50]}... → {nuevo[:50]}...")
                break
    
    # 4. Resumen
    print()
    print("=" * 80)
    print(f"📊 RESUMEN:")
    print(f"   Cambios aplicados: {aplicados}/{len(frases)}")
    print(f"   Backup guardado en: {backup_path}")
    print()
    print("📝 SIGUIENTES PASOS:")
    print("   1. Regenerar natal_map.json:")
    print("      python generate_natal_json.py")
    print("   2. Reiniciar el servidor:")
    print("      bash ../stop_astro.sh && bash ../start_astro.sh")
    print("   3. Probar la carta nuevamente")

if __name__ == "__main__":
    apply_changes()