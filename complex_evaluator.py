from typing import Dict, Any, List, Optional
import logging

class ComplexAspectEvaluator:
    """
    Evaluador de reglas de negocio astrológicas complejas.
    Diseñado para detectar "Super Claves" que dependen de múltiples factores
    (Posición + Aspecto + Estado de otro planeta).
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def evaluate(self, chart_data: Dict[str, Any], simple_events: List[Dict[str, Any]]) -> List[str]:
        """
        Evalúa todas las reglas complejas contra los datos de la carta.
        Retorna una lista de 'titulos' (keys) que se cumplieron.
        """
        detected_keys = []
        
        # 1. Extraer datos para fácil acceso
        planets = chart_data.get('points', {})
        houses = chart_data.get('houses', {})
        aspects = chart_data.get('aspects', [])
        
        # Mapa rápido de planeta -> casa
        planet_house_map = self._build_planet_house_map(planets, houses)

        # 2. Evaluar reglas específicas (hardcoded business logic)
        
        # --- SOL ---
        # Regla: Sol en Casa 4 (pero con bloqueos)
        # "venus en casa 4: usar solo si no se dan las siguientes condiciones..." 
        # (Esta regla es para Venus, no Sol, pero el patrón es el mismo si existe para Sol)
        # Revisando auditoría: Sol en casas no tiene bloqueos complejos, son directos.
        
        # Regla: Aspectos complejos del Sol
        # "sol en conjunción o cuadratura u oposición a júpiter y saturno o plutón están en casa 1 o 4 o 7 o 10"
        if self._check_sun_jupiter_saturn_pluto_angles(planets, aspects, planet_house_map):
            detected_keys.append("sol en conjunción o cuadratura u oposición a júpiter y saturno o plutón están en casa 1 o 4 o 7 o 10")

        # --- LUNA ---
        # "luna en conjunción... a júpiter y saturno... en casa 1..."
        if self._check_moon_jupiter_saturn_pluto_angles(planets, aspects, planet_house_map):
             detected_keys.append("luna en conjunción o cuadratura u oposición a júpiter y saturno o plutón están en casa 1 o 4 o 7 o 10")

        # --- VENUS ---
        # Regla: Venus en Casa 4 (Bloqueo)
        # "venus en casa 4: usar solo si no se dan las siguientes condiciones: saturno en casa 4 o plutón en casa 4..."
        # --- VENUS ---
        # Regla: Venus en Casa 4 (Bloqueo)
        # La lógica de bloqueo se maneja en get_negative_filters, no aquí.
        # Aquí solo agregaríamos keys nuevas si fuera necesario.

            
        # Regla: Venus aspectos complejos
        # "venus en conjunción... a neptuno. no usar si venus está en el signo de piscis"
        if self._check_venus_neptune_pisces(planets, aspects):
            # Si Pasa el check (no está en piscis), devolvemos la key del aspecto.
            # La key en el json/markdown es larga?
            # Key: "venus en conjunción o cuadratura u oposición a neptuno. no usar si venus está en el signo de piscis"
            # Si se cumple el aspecto Y NO está en Piscis, retornamos esta key para que se busque el texto.
            detected_keys.append("venus en conjunción o cuadratura u oposición a neptuno. no usar si venus está en el signo de piscis")

        # --- ASCENDENTE ---
        # "ascendente (ángulo) en tauro y marte está en casa 1 o 4 o 7 o 10"
        if self._check_asc_taurus_mars_angles(planets, planet_house_map):
             detected_keys.append("ascendente (ángulo) en tauro y marte está en casa 1 o 4 o 7 o 10")
             
        # "ascendente (ángulo) en tauro y marte está en conjunción al sol o la luna"
        if self._check_asc_taurus_mars_aspects(planets, aspects):
            detected_keys.append("ascendente (ángulo) en tauro y marte está en conjunción al sol o la luna")

        return detected_keys

    # --- Helpers ---

    def _build_planet_house_map(self, planets, houses):
        # Mapeo simplificado, asumiendo que ya tenemos calculada la casa de cada planeta
        # Si no viene pre-calculado, tendríamos que calcularlo aquí.
        # Por ahora asumimos que `InterpretadorAstrologico` nos pasa el mapa o `chart_data` lo tiene.
        # En `interpretador_refactored.py`, se calcula `planets_in_houses`.
        # Vamos a asumir que `chart_data['points'][planet]['house']` existe o lo pasamos aparte.
        # Para ser robustos, recalculamos o extraemos.
        pm = {}
        for name, data in planets.items():
            if 'house' in data:
                pm[name] = data['house']
        return pm

    def _has_aspect(self, aspects: list, p1: str, p2: str, types: list) -> bool:
        """Helper para verificar si existe un aspecto entre dos planetas"""
        p1 = p1.lower()
        p2 = p2.lower()
        types = [t.lower() for t in types]
        
        for asp in aspects:
            # Soporte legacy/nuevo
            a_p1 = (asp.get('p1_name') or asp.get('point1', '')).lower()
            a_p2 = (asp.get('p2_name') or asp.get('point2', '')).lower()
            a_type = (asp.get('type') or asp.get('aspect', '')).lower()
            
            # Verificar planetas (orden indistinto)
            match_planets = (a_p1 == p1 and a_p2 == p2) or (a_p1 == p2 and a_p2 == p1)
            
            if match_planets:
                # Verificar tipo (comprobando si está en la lista de tipos permitidos)
                # El tipo puede venir como "Conjunction" o "conjunción", "Square" o "cuadratura"
                # Necesitamos ser flexibles.
                
                # Mapeo rápido de inglés a español si es necesario, o check parcial
                if a_type in types:
                    return True
                
                # Check translated
                # (Asumimos que 'types' viene en inglés base o español base según quien llame)
                # Por ahora, simple string match
                for t in types:
                    if t in a_type: 
                        return True
                        
        return False

    # --- Logic Implementations ---

    def _check_sun_jupiter_saturn_pluto_angles(self, planets, aspects, pm):
        # 1. Sol aspecto Júpiter (Conj, Cuad, Opos)
        if not self._has_aspect(aspects, "Sun", "Jupiter", ["conjunction", "square", "opposition"]):
            return False
            
        # 2. Y (Saturno O Plutón) en Casas (1, 4, 7, 10)
        saturn_h = pm.get("Saturn")
        pluto_h = pm.get("Pluto")
        angles = [1, 4, 7, 10]
        
        condition_2 = (saturn_h in angles) or (pluto_h in angles)
        return condition_2

    def _check_moon_jupiter_saturn_pluto_angles(self, planets, aspects, pm):
        # 1. Luna aspecto Júpiter
        if not self._has_aspect(aspects, "Moon", "Jupiter", ["conjunction", "square", "opposition"]):
            return False
            
        # 2. Y (Saturno O Plutón) en Casas Angulares
        saturn_h = pm.get("Saturn")
        pluto_h = pm.get("Pluto")
        angles = [1, 4, 7, 10]
        
        return (saturn_h in angles) or (pluto_h in angles)

    def _check_venus_neptune_pisces(self, planets, aspects):
        # 1. Venus aspecto Neptuno
        if not self._has_aspect(aspects, "Venus", "Neptune", ["conjunction", "square", "opposition"]):
            return False
            
        # 2. NO usar si Venus está en Piscis
        venus_data = planets.get("Venus", {})
        venus_sign = venus_data.get("sign_name", "").lower() # "Pisces" o "Piscis"
        # Asegurar normalización
        if "pisc" in venus_sign: # Catch Pisces/Piscis
            return False
            
        return True

    def _check_asc_taurus_mars_angles(self, planets, pm):
        # 1. Ascendente en Tauro
        asc = planets.get("Asc", {})
        asc_sign = asc.get("sign_name", "").lower()
        if "tauro" not in asc_sign and "taurus" not in asc_sign:
            return False
            
        # 2. Marte en Casas Angulares
        mars_h = pm.get("Mars")
        return mars_h in [1, 4, 7, 10]

    def _check_asc_taurus_mars_aspects(self, planets, aspects):
        # 1. Ascendente en Tauro
        asc = planets.get("Asc", {})
        asc_sign = asc.get("sign_name", "").lower()
        if "tauro" not in asc_sign and "taurus" not in asc_sign:
            return False
            
        # 2. Marte conjunción Sol O Luna
        mars_sun = self._has_aspect(aspects, "Mars", "Sun", ["conjunction"])
        mars_moon = self._has_aspect(aspects, "Mars", "Moon", ["conjunction"])
        
        return mars_sun or mars_moon

    def get_negative_filters(self, chart_data, simple_events):
        """
        Retorna una lista de keys SIMPLES que deben ser ignoradas
        porque una regla compleja las invalida.
        """
        blocked = []
        planets = chart_data.get('points', {})
        houses = chart_data.get('houses', {})
        aspects = chart_data.get('aspects', [])
        pm = self._build_planet_house_map(planets, houses)
        
        # Venus en Casa 4 BLOQUEADA SI:
        # Saturno en Casa 4 O Plutón en Casa 4 O Venus conjunción Saturno O Venus conjunción Plutón
        if pm.get("Venus") == 4:
            sat_h = pm.get("Saturn")
            plut_h = pm.get("Pluto")
            ven_sat = self._has_aspect(aspects, "Venus", "Saturn", ["conjunction"])
            ven_plut = self._has_aspect(aspects, "Venus", "Pluto", ["conjunction"])
            
            if (sat_h == 4) or (plut_h == 4) or ven_sat or ven_plut:
                blocked.append("venus en casa 4")
                
        return blocked
