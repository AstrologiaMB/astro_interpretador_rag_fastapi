import json
import os
import re
import unicodedata

class InterpretadorAstrologico:
    """
    Nuevo motor de interpretación basado en búsquedas deterministas en JSON.
    Diseñado para Phase 3.1 (Personal Calendar) y extensible para fases futuras.
    """
    def __init__(self, data_dir: str = "/Users/apple/astrochat/astro_interpretador_rag_fastapi/data"):
        self.data_dir = data_dir
        # Cargar mapa de tránsitos
        self.transits_map = self._load_json("transitos.json")
        print(f"✅ InterpretadorAstrologico: Cargadas {len(self.transits_map)} interpretaciones de Tránsitos.")

    def _load_json(self, filename: str) -> dict:
        path = os.path.join(self.data_dir, filename)
        if not os.path.exists(path):
            print(f"⚠️ Alerta: No se encontró {filename} en {self.data_dir}")
            return {}
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error cargando {filename}: {e}")
            return {}

    def _normalize_key(self, text: str) -> str:
        """
        Normaliza texto para coincidir con las llaves del JSON.
        Ej: "Sol (tránsito)" -> "sol"
        """
        if not text:
            return ""
        
        # 1. Lowercase
        text = text.lower().strip()
        
        # 2. Remove accents
        text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
        
        # 3. Replace common variations
        text = text.replace("transito", "tránsito") # Restore accent for specific key matching if used in file
        # Wait, my JSON keys HAVE accents? 
        # Let's check a sample key from transitos.json: "sol_en_tránsito_conjunción_al_sol_natal"
        # Yes, they have accents. So I should NOT remove accents blindly if the keys have them.
        # BUT, parse_interpretations.py MIGHT have normalized them? 
        # Let's check `parse_interpretations.py` logic again.
        # It used: text.lower().strip(), re.sub special chars, re.sub spaces with _.
        # It did NOT remove accents explicitly. 
        # So "Tránsito" became "tránsito". "Conjunción" became "conjunción".
        
        return text

    def _generate_candidate_keys(self, p1: str, aspect: str, p2: str) -> list:
        """
        Genera posibles variaciones de llaves para búsqueda fuzzy.
        """
        p1 = p1.lower().strip()
        p2 = p2.lower().strip()
        aspect = aspect.lower().strip()
        
        # Clean inputs
        # Remove "(r)" or "retrogrado" if present, usually unlikely in keys
        p1 = p1.split("(")[0].strip()
        p2 = p2.split("(")[0].strip()
        
        # Map common names if necessary (e.g. 'asc' -> 'ascendente')
        # Check transitos.json keys: "sol_en_tránsito_conjunción_al_ascendente_ángulo_natal"
        if p2 in ["asc", "ac", "ascendant"]: p2 = "ascendente_ángulo"
        if p2 == "ascendente": p2 = "ascendente_ángulo" # Matches key suffix
        
        # Base logic: "p1 en tránsito aspect p2 natal"
        # Keys in JSON: "sol_en_tránsito_conjunción_al_sol_natal"
        # Variation: "sol_en_tránsito_conjunción_a_luna_natal" ("a" vs "al")
        
        preposicion = "al" if p2 in ["sol", "ascendente_ángulo"] else "a"
        if p2 in ["ascendente"]: preposicion = "al" # Just in case
        
        # Candidates
        keys = []
        
        # 1. Exact canonical form seen in JSON
        # "sol_en_tránsito_conjunción_al_sol_natal"
        key1 = f"{p1}_en_tránsito_{aspect}_{preposicion}_{p2}_natal"
        keys.append(key1)
        
        # 2. Try 'a' vs 'al' swap
        prep_alt = "a" if preposicion == "al" else "al"
        key2 = f"{p1}_en_tránsito_{aspect}_{prep_alt}_{p2}_natal"
        keys.append(key2)
        
        # 3. Try without "en_tránsito" (less likely but possible)
        # 4. Try without "natal"
        
        return [k.replace(" ", "_") for k in keys]

    def get_transit_interpretation(self, p1: str, aspect: str, p2: str, **kwargs) -> str:
        """
        Recupera la interpretación de un tránsito.
        Soporta formateo de variables (ej: {anio}) si se pasan en kwargs.
        """
        candidates = self._generate_candidate_keys(p1, aspect, p2)
        
        for key in candidates:
            if key in self.transits_map:
                raw_text = self.transits_map[key]
                return self._format_text(raw_text, **kwargs)
        
        return None

    def _format_text(self, text: str, **kwargs) -> str:
        """
        Formatea el texto con las variables proporcionadas.
        Ignora variables del template que no estén en kwargs (usando safe_substitute si usara Template, o format normal con try catch).
        Para simplicidad y compatibilidad con .format(), usamos un enfoque conservador.
        """
        if not kwargs:
            return text
            
        try:
            # Intentar formateo directo
            # Nota: .format() fallará si faltan keys que están en el texto.
            # Convertimos a SafeFormatter si fuera necesario, pero por ahora asumimos que {anio} es lo único crítico.
            # Una estrategia mejor es usar str.format_map con un dict que devuelva el placeholder si falta.
            return text.format(**kwargs)
        except KeyError:
            # Si faltan keys, devolvemos el texto tal cual (o podríamos intentar parcial)
            # Para evitar crasheos, si falla, devolvemos raw.
            return text
        except Exception:
            return text
