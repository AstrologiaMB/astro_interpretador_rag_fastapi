import json
import os
import re
import unicodedata

class InterpretadorAstrologico:
    """
    Nuevo motor de interpretación basado en búsquedas deterministas en JSON.
    Diseñado para Phase 3.1 (Personal Calendar) y extensible para fases futuras.
    """

    def __init__(self, data_dir: str = None):
        if data_dir is None:
            # Use path relative to the current file
            import pathlib
            self.data_dir = str(pathlib.Path(__file__).parent / "data")
        else:
            self.data_dir = data_dir
            
        self.TRANSLATIONS = {
            "sun": "Sol", "moon": "Luna", "mercury": "Mercurio", "venus": "Venus", 
            "mars": "Marte", "jupiter": "Júpiter", "saturn": "Saturno", 
            "uranus": "Urano", "neptune": "Neptuno", "pluto": "Plutón",
            "north node": "Nodo", "northnode": "Nodo", "south node": "Nodo Sur",
            "asc": "Ascendente", "midheaven": "Medio Cielo", "mc": "Medio Cielo",
            "conjunction": "Conjunción", "opposition": "Oposición", 
            "square": "Cuadratura", "trine": "Trígono", "sextile": "Sextil",
            "aries": "Aries", "taurus": "Tauro", "gemini": "Géminis",
            "cancer": "Cáncer", "leo": "Leo", "virgo": "Virgo",
            "libra": "Libra", "scorpio": "Escorpio", "sagittarius": "Sagitario",
            "capricorn": "Capricornio", "aquarius": "Acuario", "pisces": "Piscis"
        }

        # Cargar mapa de tránsitos
        self.transits_map = self._load_json("transitos.json")
        print(f"✅ InterpretadorAstrologico: Cargadas {len(self.transits_map)} interpretaciones de Tránsitos.")

        # Cargar mapa dracónico
        self.draco_map = self._load_json("draco.json")
        print(f"✅ InterpretadorAstrologico: Cargadas {len(self.draco_map)} interpretaciones Dracónicas.")

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
        
        # 3. Replace spaces with underscores
        text = text.replace(" ", "_")

        # 4. Replace common variations
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

    def _translate(self, text: str) -> str:
        text = text.lower().strip()
        return self.TRANSLATIONS.get(text, text)

    def get_draconic_interpretations(self, chart_data: dict) -> list[dict]:
        """
        Genera interpretaciones para la carta dracónica.
        chart_data espera:
        {
            "planets": { "Sun": { "sign": "Aries", ... }, ... },
            "houses": { "1": { "degree": 0.0, "sign": "Aries" }, ... }, # Draco Houses
            "tropical_houses": { "1": { "degree": 0.0 }, ... } # Tropical Houses for superposition
            "contacts": [ { "p1": "Sun", "p2": "Sun", "aspect": "Conjunction" }, ... ]
        }
        """
        interpretations = []
        
        # 1. Planetas en Signos (Dracónicos)
        # Support both 'planets' (generic) and 'points' (API format)
        planets = chart_data.get("planets") or chart_data.get("points") or {}
        
        for planet, data in planets.items():
            sign = data.get("sign", "")
            if not sign: continue
            
            # Generate Key
            # Logic from audit_draco.py / generate_draco_json.py
            # Planets: Sun, Moon, Ascendant (treated as planet here?)
            
            # Generate Key
            # Logic from audit_draco.py / generate_draco_json.py
            # Planets: Sun, Moon, Ascendant (treated as planet here?)
            
            p_norm = self._normalize_key(self._translate(planet))
            s_norm = self._normalize_key(self._translate(sign))
            
            key = ""
            if p_norm == "sol":
                key = f"el_sol_draconico_en_los_signos_que_es_el_sol_draconico_sol_draconico_en_{s_norm}"
            elif p_norm == "luna":
                # Try variations found in audit
                k1 = f"la_luna_draconica_en_los_signos_que_es_la_luna_draconica_luna_draconica_en_{s_norm}"
                k2 = f"la_luna_draconica_en_los_signos_luna_draconica_en_{s_norm}"
                if k1 in self.draco_map: key = k1
                elif k2 in self.draco_map: key = k2
            elif p_norm == "ascendente":
                # Key format from debug: el_ascendente_draconico_en_los_signos_que_es_el_ascendente_draconico_ascendente_draconico_en_tauro
                key = f"el_ascendente_draconico_en_los_signos_que_es_el_ascendente_draconico_ascendente_draconico_en_{s_norm}"
            
            # print(f"DEBUG LOOP: Planet={planet} Norm={p_norm} Sign={sign} Key={key} Found={key in self.draco_map}")
                
            if key and key in self.draco_map:
                planet_es = self._translate(planet)
                sign_es = self._translate(sign)
                interpretations.append({
                    "titulo": f"{planet_es} Dracónico en {sign_es}",
                    "texto": self.draco_map[key],
                    "etiquetas": ["draconica", "planeta", planet.lower()]
                })

        # 2. Superposición de Casas (Draco Cusp -> Tropical House)
        # Necesitamos saber en qué casa TROPICAL cae la cúspide DRACÓNICA.
        # chart_data debe proveer esta info ya calculada: 'house_overlaps': { "1": 12, "2": 1, ... }
        # Significa: La cúspide de Casa 1 Dracónica cae en Casa 12 Trópica.
        
        overlaps = chart_data.get("house_overlaps", {})
        if not overlaps and "houses" in chart_data and "tropical_houses" in chart_data:
            overlaps = self._calculate_house_overlaps(chart_data["houses"], chart_data["tropical_houses"])
            
        for d_metrics, t_house in overlaps.items():
            # d_metrics is house number (1-12)
            try:
                d_num = int(d_metrics)
                t_num = int(t_house)
            except:
                continue
                
            # Key Generation Logic (Validated by Audit)
            p1 = "superposicion_de_casas_draconicas_con_casas_tropicas"
            p2 = self._normalize_key(f"significado de la casa {d_num} draconica")
            if d_num == 1:
                p3 = self._normalize_key("la cuspide del ascendente draconico en relacion con la carta tropica")
                p4 = self._normalize_key(f"la cuspide del ascendente draconico superpuesto a la casa {t_num} tropica")
            else:
                p3 = self._normalize_key(f"la cuspide de la casa {d_num} draconica en relacion con la carta tropica")
                p4 = self._normalize_key(f"la cuspide de la casa {d_num} draconica superpuesta a la casa {t_num} tropica")
                
            full_key = f"{p1}_{p2}_{p3}_{p4}"
            # print(f"DEBUG: Checking Overlap Key: {full_key}")
            
            if full_key in self.draco_map:
                interpretations.append({
                    "titulo": f"Casa {d_num} Dracónica en Casa {t_num} Trópica",
                    "texto": self.draco_map[full_key],
                    "etiquetas": ["draconica", "casa", "superposicion"]
                })
            else:
                # Debug only
                # print(f"Missing Draco Key: {full_key}")
                pass

        # 3. Contactos (Draco Planet -> Tropical Planet)
        contacts = chart_data.get("contacts", [])
        for contact in contacts:
            p1 = contact.get("p1", "") # Draco Planet
            p2 = contact.get("p2", "") # Tropical Planet
            aspect = contact.get("aspect", "")
            
            if not p1 or not p2 or not aspect: continue
            
            
            if not p1 or not p2 or not aspect: continue
            
            p1_n = self._normalize_key(self._translate(p1))
            p2_n = self._normalize_key(self._translate(p2))
            asp_n = self._normalize_key(self._translate(aspect))
            
            # Pattern: contactos_entre_planetas_draconicos_y_tropicos_{aspect}_de_{p1}_draconico_con_{p2}_tropico
            key = f"contactos_entre_planetas_draconicos_y_tropicos_{asp_n}_de_{p1_n}_draconico_con_{p2_n}_tropico"

            p1_es = self._translate(p1)
            p2_es = self._translate(p2)
            aspect_es = self._translate(aspect)

            if key in self.draco_map:
                interpretations.append({
                    "titulo": f"{p1_es} Dracónico {aspect_es} {p2_es} Trópico",
                    "texto": self.draco_map[key],
                    "etiquetas": ["draconica", "contacto", aspect]
                })

        return interpretations

    def _calculate_house_overlaps(self, draco_houses: dict, tropical_houses: dict) -> dict:
        """
        Calcula en qué casa trópica cae cada cúspide dracónica.
        """
        overlaps = {}
        
        # Convert tropical houses to list of (house_num, degree) sorted by house num
        # However, houses might not be sorted by degree if interception?
        # Standard approach: Sort by degree?
        # But we need to know "House 1 starts at X".
        
        # Structure expected: { "1": 23.5, "2": 56.7 ... } OR { "1": {"degree": 23.5}, ... }
        t_cusps = []
        try:
            for h in range(1, 13):
                h_str = str(h)
                if h_str not in tropical_houses: return {}
                
                val = tropical_houses[h_str]
                if isinstance(val, dict):
                    deg = val.get("degree", 0.0)
                else:
                    deg = float(val)
                t_cusps.append((h, deg))
        except:
            return {}

        # Function to check if degree is between cusp1 and cusp2
        def is_between(deg, cusp1, cusp2):
            if cusp1 < cusp2:
                return cusp1 <= deg < cusp2
            else: # Wrap around 360/0
                return (cusp1 <= deg < 360) or (0 <= deg < cusp2)

        for h in range(1, 13):
            h_str = str(h)
            if h_str not in draco_houses: continue
            
            val = draco_houses[h_str]
            if isinstance(val, dict):
                d_deg = val.get("degree", 0.0)
            else:
                d_deg = float(val)
                
            # Find which tropical house contains d_deg
            found_t = None
            for i in range(12):
                curr_h, curr_deg = t_cusps[i]
                next_h, next_deg = t_cusps[(i+1)%12]
                
                if is_between(d_deg, curr_deg, next_deg):
                    found_t = curr_h
                    break
            
            if found_t:
                overlaps[str(h)] = found_t
                
        return overlaps

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

    # --- TROPICAL CHART IMPLEMENTATION (Phase 3.2) ---

    def load_natal_map(self, filepath: str = "natal_map.json"):
        """
        Carga el mapa de interpretaciones de la Carta Natal.
        Si no existe, intenta generarlo desde el Markdown maestro.
        """
        full_path = os.path.join(self.data_dir, filepath)
        
        if os.path.exists(full_path):
            self.natal_map = self._load_json(filepath)
            print(f"✅ InterpretadorAstrologico: Cargadas {len(self.natal_map)} interpretaciones natales.")
        else:
            print(f"⚠️ No se encontró {filepath}, intentando generar desde Markdown...")
            # Aquí podríamos llamar a un parser interno, o asumir que el proceso de build
            # ya debió haber corrido. Por ahora, si no está, logueamos error.
            self.natal_map = {}
            print(f"❌ Error: {filepath} no encontrado. Ejecuta el script de parsing primero.")

    def get_natal_interpretations(self, carta_natal: dict) -> list:
        """
        Genera la lista completa de interpretaciones para una carta natal dada.
        Usa lógica determinista (JSON Lookup) + Evaluador Complejo.
        """
        try:
            from .complex_evaluator import ComplexAspectEvaluator
        except ImportError:
            from complex_evaluator import ComplexAspectEvaluator
        evaluator = ComplexAspectEvaluator()
        
        interpretations = []
        
        # 1. Extraer Eventos Simples (Planetas en Signos y Casas)
        simple_events = self._extract_simple_events(carta_natal)
        
        # 2. Obtener Eventos Complejos (Super Claves)
        complex_keys = evaluator.evaluate(carta_natal, simple_events)
        
        # 3. Obtener Filtros Negativos (Qué NO mostrar)
        negative_filters = evaluator.get_negative_filters(carta_natal, simple_events)
        
        # --- DEBUG KEY LOGGING ---
        print(f"🔑 KEYS GENERADAS ({len(simple_events)} simples + {len(complex_keys)} complejos):")
        for e in simple_events:
            print(f"   - {e['key']}")
        for k in complex_keys:
             print(f"   - {k} (Complex)")
        # -------------------------

        # 4. Procesar Eventos Simples
        for event in simple_events:
            key = event['key']
            
            # Aplicar filtro negativo
            if key in negative_filters:
                # print(f"🚫 Filtrando evento bloqueado: {key}")
                continue
                
            # Buscar datos
            data = self._find_text_for_key(key)
                
            if data and isinstance(data, dict) and "texto" in data:
                interpretations.append({
                    "titulo": event['titulo'],
                    "texto": data["texto"],
                    "tipo": event['tipo'],
                    "key": key
                })
            elif data and isinstance(data, str):
                 interpretations.append({
                    "titulo": event['titulo'],
                    "texto": data,
                    "tipo": event['tipo'],
                    "key": key
                })
        
        # 5. Procesar Eventos Complejos
        for key in complex_keys:
            data = self._find_text_for_key(key)
            if data and isinstance(data, dict) and "texto" in data:
                 interpretations.append({
                    "titulo": key.capitalize(), # O algún título mejor formateado si tenemos
                    "texto": data["texto"],
                    "tipo": "AspectoComplejo",
                    "key": key
                })
            elif data and isinstance(data, str):
                 interpretations.append({
                    "titulo": key.capitalize(),
                    "texto": data,
                    "tipo": "AspectoComplejo",
                    "key": key
                })
                
        return interpretations

    def _calculate_house_placements(self, points: dict, houses: dict) -> dict:
        """Calcula posiciones de casas si no vienen en el payload"""
        placements = {}
        
        # Mapa de cúspides
        cusps = {}
        for h_num, h_data in houses.items():
            cusps[int(h_num)] = h_data['longitude']
            
        if len(cusps) != 12: 
            return {}

        for name, data in points.items():
            if name in ["Asc", "MC", "Ic", "Dsc", "Vertex", "Part of Fortune"]: continue
            
            lon = data.get('longitude')
            if lon is None: continue
            
            # Encontrar casa
            for i in range(1, 13):
                start = cusps[i]
                next_h = (i % 12) + 1
                end = cusps[next_h]
                
                # Caso cruce Aries (350 -> 10)
                if end < start:
                   if lon >= start or lon < end:
                       placements[name] = i
                       break
                else:
                   if lon >= start and lon < end:
                       placements[name] = i
                       break
        return placements

    def _extract_simple_events(self, carta: dict) -> list:
        """Genera lista de keys estándar para búsqueda"""
        events = []
        points = carta.get('points', {})
        houses = carta.get('houses', {})
        
        # Calcular casas manualmente si no vienen
        house_placements = self._calculate_house_placements(points, houses)
        
        # Planetas en Signos
        for name, data in points.items():
            # Traducir signo
            sign_raw = data.get('sign_name', data.get('sign', ''))
            sign = self._translate_sign(sign_raw)
            
            # 1. Ángulos (Ascendente)
            if name == "Asc":
                key = f"ascendente (ángulo) en {sign}"
                events.append({
                    "key": key,
                    "titulo": f"Ascendente en {sign.capitalize()}",
                    "tipo": "AnguloEnSigno"
                })
                continue
                
            # 2. MC, Ic, Dsc (Ignorar por ahora si no hay keys)
            if name in ["MC", "Ic", "Dsc", "Vertex", "Part of Fortune"]: 
                continue

            # 3. Nodos (True North Node -> nodo)
            if "North Node" in name:
                key = f"nodo en {sign}"
                events.append({
                    "key": key,
                    "titulo": f"Nodo en {sign.capitalize()}",
                    "tipo": "PlanetaEnSigno"
                })
                continue
            
            # 4. Planetas Normales
            planet = self._translate_planet(name).lower()
            key = f"{planet} en {sign}"
            events.append({
                "key": key,
                "titulo": f"{planet.capitalize()} en {sign.capitalize()}",
                "tipo": "PlanetaEnSigno"
            })
            
        # Planetas en Casas
        # 1. Intentar usar datos directos del payload
        for name, data in points.items():
            if 'house' in data:
                house = data['house']
                if "North Node" in name:
                    planet = "nodo"
                else:
                    planet = self._translate_planet(name).lower()
                
                key = f"{planet} en casa {house}"
                events.append({
                    "key": key,
                    "titulo": f"{planet.capitalize()} en Casa {house}",
                    "tipo": "PlanetaEnCasa"
                })
        
        # 2. Si no hubo datos directos, usar calculados
        # (Para evitar duplicados, verificamos si ya agregamos eventos de casa para este planeta? 
        #  O simplemente asumimos que si house_placements tiene datos es porque validamos)
        if house_placements:
             for name, house in house_placements.items():
                # Normalización específica para Nodos en Casas ("nodo en casa X")
                if "North Node" in name:
                    planet = "nodo"
                else:
                    planet = self._translate_planet(name).lower()
                
                key = f"{planet} en casa {house}"
                
                # Chequear duplicados muy básico
                if not any(e['key'] == key for e in events):
                    events.append({
                        "key": key,
                        "titulo": f"{planet.capitalize()} en Casa {house}",
                        "tipo": "PlanetaEnCasa"
                    })

                
        # Aspectos Simples
        aspects = carta.get('aspects', [])
        for asp in aspects:
            # Soporte para p1_name (legacy) vs point1 (nuevo)
            p1_raw = asp.get('p1_name', asp.get('point1'))
            p2_raw = asp.get('p2_name', asp.get('point2'))
            
            if not p1_raw or not p2_raw:
                continue
                
            p1 = self._translate_planet(p1_raw).lower()
            p2 = self._translate_planet(p2_raw).lower()
            
            # Normalizar tipo de aspecto
            # Soporte para type (legacy) vs aspect (nuevo)
            iso_type = asp.get('type', asp.get('aspect', ''))
            tipo_es = self._translate_aspect_type(iso_type)
            
            if tipo_es:
                # Key: "sol conjunción a luna"
                # Nota: El Markdown usa "a" o "al" o nada, hay que normalizar en _find_text_for_key
                # La key canónica será: "{p1} {aspecto} a {p2}"
                key = f"{p1} {tipo_es} a {p2}"
                events.append({
                    "key": key,
                    "titulo": f"{p1.capitalize()} {tipo_es.capitalize()} a {p2.capitalize()}",
                    "tipo": "Aspecto"
                })
        return events

    def _find_text_for_key(self, key: str) -> str:
        """Busca el texto, probando normalizaciones"""
        # 1. Búsqueda exacta
        if key in self.natal_map:
            return self.natal_map[key]
            
        # 2. Normalización de espacios
        norm_key = " ".join(key.split())
        if norm_key in self.natal_map:
            return self.natal_map[norm_key]
            
        # 3. Variaciones comunes de preposiciones en aspectos
        # "sol conjunción a luna" vs "sol conjunción luna" vs "sol conjunción a la luna"
        # Esto es costoso, idealmente el JSON ya está limpio.
        # Pero podemos probar quitar " a "
        if " a " in norm_key:
            alt_key = norm_key.replace(" a ", " ")
            if alt_key in self.natal_map: return self.natal_map[alt_key]
            
        return None

    def _translate_planet(self, english_name: str) -> str:
        mapa = {
            "Sun": "sol", "Moon": "luna", "Mercury": "mercurio", "Venus": "venus", "Mars": "marte",
            "Jupiter": "júpiter", "Saturn": "saturno", "Uranus": "urano", "Neptune": "neptuno", 
            "Pluto": "plutón", "North Node": "nodo norte", "South Node": "nodo sur",
            "Chiron": "quirón", "Lilith": "lilith"
        }
        return mapa.get(english_name, english_name.lower())

    def _translate_sign(self, english_name: str) -> str:
        mapa = {
            "aries": "aries", "taurus": "tauro", "gemini": "géminis", "cancer": "cáncer",
            "leo": "leo", "virgo": "virgo", "libra": "libra", "scorpio": "escorpio",
            "sagittarius": "sagitario", "capricorn": "capricornio", "aquarius": "acuario",
            "pisces": "piscis",
            "ar": "aries", "ta": "tauro", "ge": "géminis", "cn": "cáncer",
            "le": "leo", "vi": "virgo", "li": "libra", "sc": "escorpio",
            "sa": "sagitario", "cp": "capricornio", "aq": "acuario", "pi": "piscis"
        }
        return mapa.get(english_name.lower(), english_name.lower())

    def _translate_aspect_type(self, iso_type: str) -> str:
        if not iso_type:
            return None
            
        iso_type = iso_type.lower()
        
        mapa = {
            # Ingles
            "conjunction": "conjunción",
            "opposition": "oposición",
            "square": "cuadratura",
            "trine": "trígono",
            "sextile": "sextil",
            
            # Español (variaciones que pueden venir del payload)
            "conjunción": "conjunción",
            "conjuncion": "conjunción",
            "oposición": "oposición",
            "oposicion": "oposición",
            "cuadratura": "cuadratura",
            "trígono": "trígono",
            "trigono": "trígono",
            "sextil": "sextil"
        }
        return mapa.get(iso_type, None)
