#!/usr/bin/env python3
"""
Script para mostrar qué archivos de interpretaciones y títulos carga el interpretador_refactored.py
"""

import os
import sys
from pathlib import Path
import re

def mostrar_archivos_interpretaciones():
    """Mostrar archivos de interpretaciones que carga el sistema"""
    print("=" * 60)
    print("📄 ARCHIVOS DE INTERPRETACIONES CARGADOS")
    print("=" * 60)
    
    interpretaciones_dir = Path("data")
    md_files = sorted([f for f in interpretaciones_dir.glob("[0-9]*.md")])
    
    if not md_files:
        print("❌ No se encontraron archivos de interpretaciones numerados")
        return
    
    print(f"📊 Total de archivos encontrados: {len(md_files)}")
    print()
    
    for i, file_path in enumerate(md_files, 1):
        file_size = file_path.stat().st_size
        print(f"{i:2d}. {file_path.name}")
        print(f"    📁 Ruta: {file_path}")
        print(f"    📏 Tamaño: {file_size:,} bytes")
        
        # Leer las primeras líneas para mostrar el contenido
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()[:5]  # Primeras 5 líneas
                if lines:
                    first_line = lines[0].strip()
                    if first_line.startswith('#'):
                        print(f"    📝 Título: {first_line}")
                    else:
                        print(f"    📝 Inicio: {first_line[:50]}...")
        except Exception as e:
            print(f"    ⚠️  Error leyendo archivo: {e}")
        
        print()

def mostrar_titulos_objetivo():
    """Mostrar títulos objetivo cargados desde el archivo MD"""
    print("=" * 60)
    print("🎯 TÍTULOS OBJETIVO CARGADOS")
    print("=" * 60)
    
    titles_file_path = "data/Títulos Numerados tropico.md"
    
    if not Path(titles_file_path).exists():
        print(f"❌ Archivo de títulos no encontrado: {titles_file_path}")
        return
    
    target_titles = set()
    aspect_keywords = ["conjunción", "oposición", "cuadratura", "trígono", "sextil"]
    
    try:
        with open(titles_file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                match_header = re.match(r"^#{2,4}\s*\d+(?:\.\d+)*\s+(.*)", line)
                match_retrograde = re.match(r"^## \d+\.\d+\s+([A-ZÁÉÍÓÚÜÑ]+\s+RETRÓGRADO).*", line)
                title_to_process = None

                if match_header:
                    title_to_process = match_header.group(1).strip()
                elif match_retrograde:
                    title_to_process = match_retrograde.group(1).strip()
                elif re.match(r"^[A-Z\s]+ RETRÓGRADO", line):
                    title_to_process = line.strip()

                if title_to_process:
                    normalized_title = re.sub(r'\s*\([^)]*\)', '', title_to_process)
                    normalized_title = re.sub(r':.*', '', normalized_title)
                    normalized_title = normalized_title.lower()
                    normalized_title = re.sub(r'\s+', ' ', normalized_title).strip()
                    normalized_title = normalized_title.replace(" en casa dos", " en casa 2")

                    is_relevant = (
                        normalized_title.startswith("aspecto ") or
                        " en " in normalized_title or
                        normalized_title.endswith(" retrógrado") or
                        " en el ascendente" in normalized_title
                    )

                    if is_relevant:
                        if normalized_title.startswith("aspecto "):
                            match_aspect = re.match(r"aspecto\s+([a-záéíóúüñ]+)\s+(.*?)\s+a\s+([a-záéíóúüñ]+)", normalized_title)
                            if match_aspect:
                                planet1 = match_aspect.group(1)
                                aspect_part = match_aspect.group(2)
                                planet2 = match_aspect.group(3)

                                found_aspects = [kw for kw in aspect_keywords if kw in aspect_part.split()]

                                if found_aspects:
                                    for asp in found_aspects:
                                        specific_title = f"aspecto {planet1} {asp} a {planet2}"
                                        target_titles.add(specific_title)
                                else:
                                    target_titles.add(normalized_title)
                            else:
                                target_titles.add(normalized_title)
                        else:
                            target_titles.add(normalized_title)

        print(f"📊 Total de títulos objetivo cargados: {len(target_titles)}")
        print()
        
        # Categorizar títulos
        categorias = {
            "Planetas en Signos": [],
            "Planetas en Casas": [],
            "Planetas Retrógrados": [],
            "Aspectos": [],
            "Ascendente": [],
            "Otros": []
        }
        
        for title in sorted(target_titles):
            if title.endswith(" retrógrado"):
                categorias["Planetas Retrógrados"].append(title)
            elif " en casa " in title:
                categorias["Planetas en Casas"].append(title)
            elif title.startswith("aspecto "):
                categorias["Aspectos"].append(title)
            elif " en el ascendente" in title:
                categorias["Ascendente"].append(title)
            elif " en " in title and " casa " not in title:
                categorias["Planetas en Signos"].append(title)
            else:
                categorias["Otros"].append(title)
        
        # Mostrar por categorías
        for categoria, titulos in categorias.items():
            if titulos:
                print(f"📂 {categoria} ({len(titulos)} títulos):")
                for i, titulo in enumerate(titulos[:10], 1):  # Mostrar solo los primeros 10
                    print(f"   {i:2d}. {titulo}")
                if len(titulos) > 10:
                    print(f"   ... y {len(titulos) - 10} más")
                print()
                
    except Exception as e:
        print(f"❌ Error procesando archivo de títulos: {e}")

def verificar_compatibilidad():
    """Verificar compatibilidad entre archivos y títulos"""
    print("=" * 60)
    print("🔍 VERIFICACIÓN DE COMPATIBILIDAD")
    print("=" * 60)
    
    # Verificar que existe el interpretador
    if not Path("interpretador_refactored.py").exists():
        print("❌ No se encontró interpretador_refactored.py")
        return
    
    # Verificar directorio data
    if not Path("data").exists():
        print("❌ No se encontró el directorio 'data'")
        return
    
    # Verificar archivos de interpretaciones
    interpretaciones_dir = Path("data")
    md_files = sorted([f for f in interpretaciones_dir.glob("[0-9]*.md")])
    
    if not md_files:
        print("❌ No se encontraron archivos de interpretaciones numerados")
        return
    
    # Verificar archivo de títulos
    titles_file = Path("data/Títulos Numerados tropico.md")
    if not titles_file.exists():
        print("❌ No se encontró el archivo de títulos objetivo")
        return
    
    print("✅ Todos los archivos necesarios están presentes")
    print(f"✅ {len(md_files)} archivos de interpretaciones encontrados")
    print(f"✅ Archivo de títulos objetivo encontrado")
    
    # Verificar variables de entorno
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Variable OPENAI_API_KEY no encontrada")
    else:
        print("✅ Variable OPENAI_API_KEY configurada")

def main():
    """Función principal"""
    print("🚀 ANÁLISIS DEL SISTEMA INTERPRETADOR RAG")
    print("=" * 60)
    print()
    
    # Verificar compatibilidad primero
    verificar_compatibilidad()
    print()
    
    # Mostrar archivos de interpretaciones
    mostrar_archivos_interpretaciones()
    
    # Mostrar títulos objetivo
    mostrar_titulos_objetivo()
    
    print("=" * 60)
    print("✅ ANÁLISIS COMPLETADO")
    print("=" * 60)
    
    # Información adicional
    print("\n📋 INFORMACIÓN ADICIONAL:")
    print("• Los archivos numerados (1*.md, 2*.md, etc.) contienen las interpretaciones")
    print("• El archivo 'Títulos Numerados tropico.md' contiene los títulos objetivo")
    print("• El sistema filtra eventos según estos títulos para generar interpretaciones")
    print("• Para ejecutar el interpretador completo, usar: python interpretador_refactored.py")

if __name__ == "__main__":
    main()
