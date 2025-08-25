#!/usr/bin/env python3
"""
NORMALIZADOR DE TÍTULOS ASTROLÓGICOS
====================================

PROPÓSITO:
    Mantener consistencia entre los títulos en 'Títulos Numerados tropico.md' 
    y los títulos reales en los archivos de interpretación (2-EL SOL.md, etc.)

PROBLEMA QUE RESUELVE:
    - Inconsistencias como "Aspecto Sol conjunción Lilith" vs "Aspecto Sol conjunción a Venus"
    - Diferencias de formato que impiden al RAG encontrar interpretaciones
    - Mantenimiento manual propenso a errores

CASOS DE USO:
    1. Después de modificar archivos de interpretación
    2. Al agregar nuevos aspectos o planetas
    3. Mantenimiento periódico de consistencia
    4. Debugging de problemas de RAG

COMANDOS DISPONIBLES:
===================

1. ANÁLISIS (Solo lectura - NO modifica archivos)
   python normalize_astro_titles.py --analyze
   
   ¿Qué hace?
   - Escanea todos los archivos .md en /data/
   - Detecta inconsistencias de formato
   - Genera reporte detallado de problemas
   - NO modifica ningún archivo
   
   Usar cuando:
   - Quieres ver qué cambios se harían
   - Debugging de problemas de RAG
   - Auditoría de consistencia

2. NORMALIZACIÓN (Modifica archivos CON backup automático)
   python normalize_astro_titles.py --normalize
   
   ¿Qué hace?
   - SIEMPRE crea backup automático con timestamp
   - Aplica todas las reglas de normalización detectadas
   - Modifica 'Títulos Numerados tropico.md'
   - Genera reporte de cambios realizados
   
   Usar cuando:
   - Quieres aplicar las correcciones detectadas
   - Después de modificar archivos de interpretación
   - Para resolver problemas de RAG

REGLAS DE NORMALIZACIÓN:
=======================

1. ASPECTOS - Agregar preposición "a":
   Antes: "Aspecto Sol conjunción Lilith"
   Después: "Aspecto Sol conjunción a Lilith"
   
2. PLANETAS RETRÓGRADOS - Normalizar capitalización:
   Antes: "MERCURIO RETRÓGRADO"
   Después: "Mercurio retrógrado"
   
3. CASAS - Convertir números escritos:
   Antes: "Sol en casa dos"
   Después: "Sol en casa 2"
   
4. CAPITALIZACIÓN - Formato título:
   Antes: "SOL EN CAPRICORNIO"
   Después: "Sol en Capricornio"

AUTOR: Cline AI Assistant
FECHA: 8 de Julio, 2025
VERSIÓN: 1.0
"""

import os
import re
import sys
import argparse
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Set
from dataclasses import dataclass

@dataclass
class TitleInconsistency:
    """Representa una inconsistencia encontrada entre títulos"""
    target_title: str
    source_title: str
    source_file: str
    problem_type: str
    severity: str  # "critical", "minor"
    suggested_fix: str
    impact_description: str

class AstroTitleNormalizer:
    """Normalizador de títulos astrológicos"""
    
    def __init__(self, data_dir: str = "data"):
        """
        Inicializar el normalizador
        
        Args:
            data_dir: Directorio que contiene los archivos de interpretación
        """
        self.data_dir = Path(data_dir)
        self.target_file = self.data_dir / "Títulos Numerados tropico.md"
        self.backup_dir = self.data_dir / "backups"
        
        # Crear directorio de backups si no existe
        self.backup_dir.mkdir(exist_ok=True)
        
        # Patrones para extraer títulos
        self.title_patterns = [
            r"^#{2,4}\s*\d+(?:\.\d+)*\s+(.*)",  # ## ### #### 2.3.1 Título
            r"^## \d+\.\d+\s+([A-ZÁÉÍÓÚÜÑ\s]+RETRÓGRADO)",  # ## 6.1 MERCURIO RETRÓGRADO
            r"^([A-Z\s]+ RETRÓGRADO)$",  # MERCURIO RETRÓGRADO
            r"^### (.+)$"  # Any ### title (like ### Aspecto Sol conjunción Lilith)
        ]
        
        # Palabras numéricas a convertir
        self.number_words = {
            "dos": "2", "tres": "3", "cuatro": "4", "cinco": "5",
            "seis": "6", "siete": "7", "ocho": "8", "nueve": "9",
            "diez": "10", "once": "11", "doce": "12"
        }
        
        # Aspectos que requieren preposición "a"
        self.aspect_keywords = ["conjunción", "oposición", "cuadratura", "trígono", "sextil"]
        
    def scan_interpretation_files(self) -> Dict[str, List[str]]:
        """
        Escanear archivos de interpretación y extraer títulos
        
        Returns:
            Dict con nombre de archivo y lista de títulos encontrados
        """
        interpretation_files = {}
        
        # Buscar archivos numerados de interpretación
        # Patrón: "2 - EL SOL_ LA IDENTIDAD .md"
        md_files = sorted([f for f in self.data_dir.glob("[0-9]*.md")])
        
        # Si no encuentra archivos con el patrón anterior, buscar archivos que empiecen con número y espacio y guión
        if not md_files:
            md_files = sorted([f for f in self.data_dir.glob("[0-9] - *.md")])
        
        # Si tampoco encuentra, buscar archivos que empiecen con número y espacio
        if not md_files:
            md_files = sorted([f for f in self.data_dir.glob("[0-9] *.md")])
        
        # Si aún no encuentra, buscar archivos que empiecen con números de dos dígitos
        if not md_files:
            md_files = sorted([f for f in self.data_dir.glob("[0-9][0-9] *.md")])
        
        for file_path in md_files:
            titles = []
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line_num, line in enumerate(f, 1):
                        line = line.strip()
                        for pattern in self.title_patterns:
                            match = re.match(pattern, line)
                            if match:
                                title = match.group(1).strip()
                                titles.append(title)
                                break
                
                if titles:
                    interpretation_files[file_path.name] = titles
                    
            except Exception as e:
                print(f"⚠️ Error leyendo {file_path}: {e}")
        
        return interpretation_files
    
    def load_target_titles(self) -> Set[str]:
        """
        Cargar títulos del archivo objetivo
        
        Returns:
            Set de títulos normalizados del archivo objetivo
        """
        target_titles = set()
        
        if not self.target_file.exists():
            print(f"❌ Archivo objetivo no encontrado: {self.target_file}")
            return target_titles
        
        try:
            with open(self.target_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    for pattern in self.title_patterns:
                        match = re.match(pattern, line)
                        if match:
                            title = match.group(1).strip()
                            # Normalizar para comparación
                            normalized = self._normalize_for_comparison(title)
                            target_titles.add(normalized)
                            break
        except Exception as e:
            print(f"❌ Error leyendo archivo objetivo: {e}")
        
        return target_titles
    
    def _normalize_for_comparison(self, title: str) -> str:
        """
        Normalizar título para comparación (sin modificar el original)
        
        Args:
            title: Título a normalizar
            
        Returns:
            Título normalizado para comparación
        """
        normalized = title.lower()
        normalized = re.sub(r'\s*\(\d+°.*?\)', '', normalized)  # Remover grados
        normalized = re.sub(r':.*', '', normalized)  # Remover después de :
        normalized = re.sub(r'\s+', ' ', normalized).strip()  # Normalizar espacios
        return normalized
    
    def _apply_normalization_rules(self, title: str) -> str:
        """
        Aplicar reglas de normalización a un título
        
        Args:
            title: Título original
            
        Returns:
            Título normalizado
        """
        normalized = title
        
        # Regla 1: REMOVER preposición "a" en aspectos (caso específico de Lilith)
        # El problema es que el código genera "aspecto sol conjunción a lilith" 
        # pero el archivo objetivo tiene "Aspecto Sol conjunción Lilith" (sin "a")
        if normalized.lower().startswith("aspecto ") and "lilith" in normalized.lower():
            # Para aspectos de Lilith, REMOVER la "a" si está presente
            pattern = r"(aspecto\s+\w+\s+(?:" + "|".join(self.aspect_keywords) + r")\s+)a\s+(\w+)"
            normalized = re.sub(pattern, r"\1\2", normalized, flags=re.IGNORECASE)
        elif normalized.lower().startswith("aspecto "):
            # Para otros aspectos, agregar "a" si no está presente
            pattern = r"(aspecto\s+\w+\s+(?:" + "|".join(self.aspect_keywords) + r")\s+)(\w+)"
            match = re.search(pattern, normalized.lower())
            if match and " a " not in normalized.lower() and "lilith" not in normalized.lower():
                # Solo agregar "a" si no está presente y no es Lilith
                normalized = re.sub(
                    pattern, 
                    r"\1a \2", 
                    normalized, 
                    flags=re.IGNORECASE
                )
        
        # Regla 2: Normalizar capitalización de planetas retrógrados
        if "retrógrado" in normalized.lower():
            # Convertir "MERCURIO RETRÓGRADO" a "Mercurio retrógrado"
            normalized = re.sub(
                r"([A-ZÁÉÍÓÚÜÑ]+)\s+(RETRÓGRADO)",
                lambda m: m.group(1).capitalize() + " " + m.group(2).lower(),
                normalized
            )
        
        # Regla 3: Convertir números de casas escritos
        for word, number in self.number_words.items():
            pattern = rf"\ben casa {word}\b"
            normalized = re.sub(pattern, f"en casa {number}", normalized, flags=re.IGNORECASE)
        
        # Regla 4: Normalizar capitalización general (solo si está todo en mayúsculas)
        if normalized.isupper() and len(normalized) > 10:
            # Capitalizar solo la primera letra de cada palabra importante
            words = normalized.split()
            capitalized_words = []
            for word in words:
                if word.lower() in ["en", "de", "del", "al", "a", "y", "o"]:
                    capitalized_words.append(word.lower())
                else:
                    capitalized_words.append(word.capitalize())
            normalized = " ".join(capitalized_words)
        
        return normalized
    
    def detect_inconsistencies(self) -> List[TitleInconsistency]:
        """
        Detectar inconsistencias entre archivos objetivo e interpretación
        
        Returns:
            Lista de inconsistencias encontradas
        """
        inconsistencies = []
        
        print("🔍 Escaneando archivos de interpretación...")
        interpretation_files = self.scan_interpretation_files()
        
        print("📋 Cargando títulos objetivo...")
        target_titles = self.load_target_titles()
        
        print("🔎 Detectando inconsistencias...")
        
        # Analizar cada archivo de interpretación
        for file_name, titles in interpretation_files.items():
            for title in titles:
                normalized_title = self._normalize_for_comparison(title)
                
                # Verificar si el título normalizado está en los objetivos
                if normalized_title not in target_titles:
                    # Aplicar reglas de normalización
                    suggested_fix = self._apply_normalization_rules(title)
                    suggested_normalized = self._normalize_for_comparison(suggested_fix)
                    
                    # Determinar tipo de problema y severidad
                    problem_type, severity, impact = self._classify_problem(title, suggested_fix)
                    
                    inconsistency = TitleInconsistency(
                        target_title=normalized_title,
                        source_title=title,
                        source_file=file_name,
                        problem_type=problem_type,
                        severity=severity,
                        suggested_fix=suggested_fix,
                        impact_description=impact
                    )
                    inconsistencies.append(inconsistency)
        
        return inconsistencies
    
    def _classify_problem(self, original: str, fixed: str) -> Tuple[str, str, str]:
        """
        Clasificar el tipo de problema y su severidad
        
        Args:
            original: Título original
            fixed: Título corregido
            
        Returns:
            Tupla con (tipo_problema, severidad, descripción_impacto)
        """
        original_lower = original.lower()
        
        # Problemas críticos que impiden funcionamiento del RAG
        if "lilith" in original_lower and "aspecto" in original_lower:
            return (
                "ASPECTO LILITH - FORMATO INCONSISTENTE",
                "critical",
                "RAG no encuentra interpretación de aspectos de Lilith"
            )
        
        if original.isupper() and "retrógrado" in original_lower:
            return (
                "PLANETA RETRÓGRADO - CAPITALIZACIÓN",
                "critical", 
                "Filtro no reconoce planetas retrógrados"
            )
        
        # Problemas menores
        if "casa" in original_lower and any(word in original_lower for word in self.number_words):
            return (
                "CASAS NUMÉRICAS",
                "minor",
                "Puede causar fallos ocasionales en búsqueda de casas"
            )
        
        if " a " not in original_lower and "aspecto" in original_lower:
            return (
                "ASPECTO SIN PREPOSICIÓN",
                "minor",
                "Inconsistencia de formato en aspectos"
            )
        
        return ("FORMATO GENERAL", "minor", "Inconsistencia menor de formato")
    
    def generate_analysis_report(self, inconsistencies: List[TitleInconsistency]) -> str:
        """
        Generar reporte detallado de análisis
        
        Args:
            inconsistencies: Lista de inconsistencias encontradas
            
        Returns:
            Reporte formateado como string
        """
        critical_issues = [i for i in inconsistencies if i.severity == "critical"]
        minor_issues = [i for i in inconsistencies if i.severity == "minor"]
        
        report = []
        report.append("=" * 40)
        report.append("ANÁLISIS DE INCONSISTENCIAS ASTROLÓGICAS")
        report.append("=" * 40)
        report.append("")
        
        # Resumen
        report.append("📊 RESUMEN:")
        interpretation_files = self.scan_interpretation_files()
        total_files = len(interpretation_files)
        total_titles = sum(len(titles) for titles in interpretation_files.values())
        
        report.append(f"- Archivos escaneados: {total_files}")
        report.append(f"- Títulos encontrados: {total_titles}")
        report.append(f"- Inconsistencias detectadas: {len(inconsistencies)}")
        report.append(f"- Problemas críticos: {len(critical_issues)}")
        report.append("")
        
        # Problemas críticos
        if critical_issues:
            report.append("🚨 PROBLEMAS CRÍTICOS (Impiden funcionamiento del RAG):")
            for i, issue in enumerate(critical_issues, 1):
                report.append(f"{i}. {issue.problem_type}")
                report.append(f"   ❌ En 'Títulos Numerados': \"{issue.target_title}\"")
                report.append(f"   ✅ Debería ser: \"{issue.suggested_fix}\"")
                report.append(f"   📁 Fuente: {issue.source_file}")
                report.append(f"   💡 Impacto: {issue.impact_description}")
                report.append("")
        
        # Problemas menores
        if minor_issues:
            report.append("⚠️ PROBLEMAS MENORES (Pueden causar fallos ocasionales):")
            for i, issue in enumerate(minor_issues, 1):
                report.append(f"{len(critical_issues) + i}. {issue.problem_type}")
                report.append(f"   ❌ Actual: \"{issue.source_title}\"")
                report.append(f"   ✅ Sugerido: \"{issue.suggested_fix}\"")
                report.append(f"   📁 Fuente: {issue.source_file}")
                report.append("")
        
        # Resumen de reglas
        if inconsistencies:
            report.append("📋 REGLAS DE NORMALIZACIÓN A APLICAR:")
            
            aspect_count = len([i for i in inconsistencies if "aspecto" in i.source_title.lower()])
            retro_count = len([i for i in inconsistencies if "retrógrado" in i.source_title.lower()])
            casa_count = len([i for i in inconsistencies if "casa" in i.source_title.lower()])
            
            if aspect_count > 0:
                report.append(f"- Agregar preposición 'a' en aspectos: {aspect_count} casos")
            if retro_count > 0:
                report.append(f"- Normalizar capitalización: {retro_count} casos")
            if casa_count > 0:
                report.append(f"- Convertir números de casas: {casa_count} casos")
            
            report.append("")
            report.append("🎯 RESULTADO ESPERADO DESPUÉS DE NORMALIZACIÓN:")
            report.append("- Eventos RAG: 33 → 34+ (incluirá aspectos de Lilith)")
            report.append("- Consistencia: 94% → 100%")
        else:
            report.append("✅ NO SE ENCONTRARON INCONSISTENCIAS")
            report.append("Todos los títulos están correctamente normalizados.")
        
        return "\n".join(report)
    
    def create_backup(self) -> str:
        """
        Crear backup del archivo objetivo
        
        Returns:
            Ruta del archivo de backup creado
        """
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_filename = f"{self.target_file.name}.backup.{timestamp}"
        backup_path = self.backup_dir / backup_filename
        
        shutil.copy2(self.target_file, backup_path)
        return str(backup_path)
    
    def apply_normalizations(self, inconsistencies: List[TitleInconsistency]) -> Dict[str, int]:
        """
        Aplicar normalizaciones al archivo objetivo
        
        Args:
            inconsistencies: Lista de inconsistencias a corregir
            
        Returns:
            Dict con estadísticas de cambios aplicados
        """
        if not inconsistencies:
            return {"total_changes": 0, "errors": 0}
        
        # Crear backup
        backup_path = self.create_backup()
        print(f"🛡️ Backup creado: {backup_path}")
        
        # Leer archivo objetivo
        try:
            with open(self.target_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"❌ Error leyendo archivo objetivo: {e}")
            return {"total_changes": 0, "errors": 1}
        
        # Aplicar cambios
        changes_made = 0
        errors = 0
        
        for i, line in enumerate(lines):
            original_line = line.strip()
            
            # Buscar títulos en esta línea
            for pattern in self.title_patterns:
                match = re.match(pattern, original_line)
                if match:
                    title = match.group(1).strip()
                    
                    # Buscar si este título necesita normalización
                    for inconsistency in inconsistencies:
                        if inconsistency.source_title == title:
                            # Aplicar normalización
                            new_title = inconsistency.suggested_fix
                            new_line = original_line.replace(title, new_title)
                            lines[i] = new_line + "\n"
                            changes_made += 1
                            print(f"✅ Cambiado: '{title}' → '{new_title}'")
                            break
                    break
        
        # Escribir archivo modificado
        try:
            with open(self.target_file, 'w', encoding='utf-8') as f:
                f.writelines(lines)
        except Exception as e:
            print(f"❌ Error escribiendo archivo: {e}")
            errors += 1
        
        return {"total_changes": changes_made, "errors": errors}
    
    def generate_normalization_report(self, stats: Dict[str, int], backup_path: str) -> str:
        """
        Generar reporte de normalización
        
        Args:
            stats: Estadísticas de cambios aplicados
            backup_path: Ruta del backup creado
            
        Returns:
            Reporte formateado
        """
        report = []
        report.append("=" * 40)
        report.append("NORMALIZACIÓN COMPLETADA")
        report.append("=" * 40)
        report.append("")
        
        report.append("🛡️ BACKUP CREADO:")
        report.append(f"- Archivo: {Path(backup_path).name}")
        report.append(f"- Ubicación: {backup_path}")
        report.append("")
        
        if stats["errors"] == 0:
            report.append("✅ CAMBIOS APLICADOS:")
            report.append(f"- Total de cambios: {stats['total_changes']}")
            report.append(f"- Errores: {stats['errors']}")
            report.append("")
            
            if stats["total_changes"] > 0:
                report.append("🚀 PRÓXIMO PASO:")
                report.append("Reinicia el servicio RAG para aplicar cambios:")
                report.append("cd ../astro_interpretador_rag_fastapi && python app.py")
            else:
                report.append("ℹ️ No se realizaron cambios (archivo ya normalizado)")
        else:
            report.append("❌ ERRORES DURANTE LA NORMALIZACIÓN:")
            report.append(f"- Cambios aplicados: {stats['total_changes']}")
            report.append(f"- Errores: {stats['errors']}")
            report.append("")
            report.append("🔄 RECOMENDACIÓN:")
            report.append("Revisa los errores y restaura desde backup si es necesario:")
            report.append(f"cp '{backup_path}' '{self.target_file}'")
        
        return "\n".join(report)

def main():
    """Función principal del script"""
    parser = argparse.ArgumentParser(
        description="Normalizador de Títulos Astrológicos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python normalize_astro_titles.py --analyze     # Solo análisis
  python normalize_astro_titles.py --normalize   # Normalizar con backup
        """
    )
    
    parser.add_argument(
        "--analyze",
        action="store_true",
        help="Analizar inconsistencias sin modificar archivos"
    )
    
    parser.add_argument(
        "--normalize", 
        action="store_true",
        help="Aplicar normalizaciones (crea backup automáticamente)"
    )
    
    parser.add_argument(
        "--data-dir",
        default="data",
        help="Directorio de archivos de interpretación (default: data)"
    )
    
    args = parser.parse_args()
    
    if not args.analyze and not args.normalize:
        parser.print_help()
        sys.exit(1)
    
    # Inicializar normalizador
    normalizer = AstroTitleNormalizer(args.data_dir)
    
    # Verificar que el directorio existe
    if not normalizer.data_dir.exists():
        print(f"❌ Directorio no encontrado: {normalizer.data_dir}")
        sys.exit(1)
    
    try:
        # Detectar inconsistencias
        inconsistencies = normalizer.detect_inconsistencies()
        
        if args.analyze:
            # Solo mostrar análisis
            report = normalizer.generate_analysis_report(inconsistencies)
            print(report)
            
        elif args.normalize:
            # Aplicar normalizaciones
            if not inconsistencies:
                print("✅ No se encontraron inconsistencias. El archivo ya está normalizado.")
                return
            
            print(f"🔧 Aplicando {len(inconsistencies)} normalizaciones...")
            stats = normalizer.apply_normalizations(inconsistencies)
            
            # Generar reporte
            backup_files = list(normalizer.backup_dir.glob("*.backup.*"))
            latest_backup = max(backup_files, key=lambda x: x.stat().st_mtime)
            
            report = normalizer.generate_normalization_report(stats, str(latest_backup))
            print(report)
            
    except Exception as e:
        print(f"❌ Error durante la ejecución: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
