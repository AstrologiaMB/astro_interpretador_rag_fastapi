#!/usr/bin/env python3
"""
DRY-RUN: Muestra qué cambios se harían sin aplicarlos.
Lee frases_astrologicas_completas.csv y busca coincidencias en los Markdown.
"""

import csv
import glob
import os

def dry_run(csv_file: str = "frases_astrologicas_completas.csv", data_dir: str = "data"):
    """Modo simulación - solo muestra, no cambia nada"""
    
    print("🔍 MODO DRY-RUN (simulación)")
    print("=" * 80)
    print("Buscando frases en archivos Markdown...")
    print("-" * 80)
    
    # Leer CSV
    frases = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)  # Saltar header
        for row in reader:
            if len(row) >= 2:
                frases.append({
                    'original': row[0].strip(),
                    'nuevo': row[1].strip()
                })
    
    print(f"📄 Total de frases a buscar: {len(frases)}")
    print()
    
    # Buscar en cada archivo Markdown
    md_files = glob.glob(os.path.join(data_dir, "*.md"))
    encontrados = 0
    no_encontrados = []
    
    for frase_data in frases:
        original = frase_data['original']
        nuevo = frase_data['nuevo']
        
        # Si son iguales, no hay cambio
        if original == nuevo:
            continue
            
        encontrado = False
        
        for md_file in md_files:
            filename = os.path.basename(md_file)
            
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                if original in line:
                    print(f"✅ ENCONTRADO en {filename}:{line_num}")
                    print(f"   Original: {original[:80]}...")
                    print(f"   Nuevo:    {nuevo[:80]}...")
                    print()
                    encontrado = True
                    encontrados += 1
                    break
            
            if encontrado:
                break
        
        if not encontrado:
            no_encontrados.append(original[:100])
    
    # Resumen
    print("=" * 80)
    print(f"📊 RESUMEN:")
    print(f"   Frases con cambios: {len([f for f in frases if f['original'] != f['nuevo']])}")
    print(f"   Encontradas en archivos: {encontrados}")
    print(f"   No encontradas: {len(no_encontrados)}")
    
    if no_encontrados:
        print()
        print("⚠️  Frases NO encontradas (podrían tener diferencias de espacios o formato):")
        for text in no_encontrados[:5]:  # Mostrar solo primeras 5
            print(f"   - {text}...")
    
    print()
    print("📝 Para aplicar los cambios reales, ejecuta:")
    print("   python apply_frases_corregidas.py")

if __name__ == "__main__":
    dry_run()