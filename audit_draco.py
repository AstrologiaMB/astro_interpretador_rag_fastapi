import json
import os
import unicodedata
import re

class DraconicAudit:
    def __init__(self, json_path):
        self.json_path = json_path
        self.data = self._load_json()
        self.existing_keys = set(self.data.keys())
        self.missing_keys = []
        self.found_keys = []

    def _load_json(self):
        with open(self.json_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def normalize_key_part(self, text):
        # Determine strict normalization logic based on observation
        # It seems to preserve "ñ" as "n"? No, "conjunción" -> "conjuncion"?
        # Let's check existing keys: "conjuncion_de_sol..." (Line 201 in draco.json view)
        # Wait, the view showed: "contactos_entre..._conjuncion_de_sol..."?
        # Let me re-verify the accent situation in the key.
        # Line 201: "contactos_entre_planetas_draconicos_y_tropicos_conjuncion_de_sol_draconico_con_sol_tropico"
        # "dracónicos" -> "draconicos"? Yes.
        # "conjunción" -> "conjuncion"? Yes.
        # So accents ARE removed.
        
        text = text.lower().strip()
        text = unicodedata.normalize('NFD', text)
        text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
        text = text.replace(" ", "_")
        return text

    def generate_house_superposition_key(self, draco_house, tropical_house):
        # Logic to generate the expected key based on file structure
        # NOTE: We suspect an anomaly where Ascendant (House 1) is under House 12 header.
        # But for 'Standard' audit, we'll try to generate what we *expect* first.
        
        p1 = "superposicion_de_casas_draconicas_con_casas_tropicas"
        
        # H2 part
        # "significado_de_la_casa_{N}_draconica"
        p2 = self.normalize_key_part(f"significado de la casa {draco_house} draconica")
        
        # H3 and H4 parts
        if draco_house == 1:
            # Special case for Ascendant?
            p3 = self.normalize_key_part("la cuspide del ascendente draconico en relacion con la carta tropica")
            p4 = self.normalize_key_part(f"la cuspide del ascendente draconico superpuesto a la casa {tropical_house} tropica")
        else:
            p3 = self.normalize_key_part(f"la cuspide de la casa {draco_house} draconica en relacion con la carta tropica")
            p4 = self.normalize_key_part(f"la cuspide de la casa {draco_house} draconica superpuesta a la casa {tropical_house} tropica")
            
        full_key = f"{p1}_{p2}_{p3}_{p4}"
        return full_key

    def generate_planet_in_sign_key(self, planet, sign):
        # Pattern: el_sol_draconico_en_los_signos_que_es_el_sol_draconico_sol_draconico_en_aries
        # H1: el_sol_draconico_en_los_signos
        # H2: que_es_el_sol_draconico
        # H3: sol_draconico_en_{sign}
        
        # Wait, is "que_es_el_sol_draconico" constant?
        # Line 4: "el_sol_draconico_en_los_signos_que_es_el_sol_draconico" (Just H1_H2)
        # Line 5: "el_sol_draconico_en_los_signos_que_es_el_sol_draconico_sol_draconico_en_aries"
        
        # It seems distinct for Sol vs Luna vs Asc?
        # Let's parameterize.
        
        if planet == "sol":
            p1 = "el_sol_draconico_en_los_signos"
            p2 = "que_es_el_sol_draconico"
            p3 = f"sol_draconico_en_{sign}"
        elif planet == "luna":
            p1 = "la_luna_draconica_en_los_signos"
            # Line 17: "la_luna_draconica_en_los_signos_que_es_la_luna_draconica"
            # Line 18: "la_luna_draconica_en_los_signos_que_es_la_luna_draconica_luna_draconica_en_aries" (Wait!)
            # Line 20: "la_luna_draconica_en_los_signos_luna_draconica_en_geminis" (MISSING "que_es..."???)
            # This implies inconsistency in headers for Gemini?
            # Or maybe "que_es..." is H2, and Gemini is H2?
            # Let's try both variations.
            pass
            
        # Implementation for Sol as baseline
        full_key = f"{p1}_{p2}_{p3}"
        return full_key

    def audit_superpositions(self):
        print("\n--- Auditing House Superpositions ---")
        # Test Houses 1-12 superposed on 1-12
        for d in range(1, 13):
            for t in range(1, 13):
                key = self.generate_house_superposition_key(d, t)
                if key in self.existing_keys:
                    self.found_keys.append(key)
                else:
                    self.missing_keys.append(key)
                    # Try to find a partial match to diagnose
                    # e.g. same suffix
                    suffix = self.normalize_key_part(f"superpuesto a la casa {t} tropica")
                    matches = [k for k in self.existing_keys if suffix in k and str(d) in k]
                    if matches:
                        print(f"MISSING: {key}")
                        print(f"  -> FOUND ALTERNATIVE: {matches[0]}")
                    else:
                        pass 
                        # print(f"MISSING COMPLETELY: {key}")

    def audit_planets_signs(self):
        print("\n--- Auditing Planets in Signs ---")
        # Planets: Sol, Luna, Ascendente? (Ascendente is usually House 1, but might be treated as planet in signs?)
        # Based on file list:
        # 3 - El sol...
        # 4 - La luna...
        # 5 - El ascendente...
        
        planets = ["sol", "luna", "ascendente"]
        signs = ["aries", "tauro", "geminis", "cancer", "leo", "virgo", "libra", "escorpio", "sagitario", "capricornio", "acuario", "piscis"]
        
        for p in planets:
            for s in signs:
                # Generate expected key
                if p == "sol":
                     # el_sol_draconico_en_los_signos_que_es_el_sol_draconico_sol_draconico_en_aries
                     key = f"el_sol_draconico_en_los_signos_que_es_el_sol_draconico_sol_draconico_en_{s}"
                elif p == "luna":
                     # la_luna_draconica_en_los_signos_que_es_la_luna_draconica_luna_draconica_en_aries
                     # VARIATION SEEN: "la_luna_draconica_en_los_signos_luna_draconica_en_geminis" (Missing que_es part)
                     # We will check both
                     key1 = f"la_luna_draconica_en_los_signos_que_es_la_luna_draconica_luna_draconica_en_{s}"
                     key2 = f"la_luna_draconica_en_los_signos_luna_draconica_en_{s}"
                     if key1 in self.existing_keys:
                         key = key1
                     else:
                         key = key2
                elif p == "ascendente":
                     # el_ascendente_draconico_en_los_signos_que_es_el_ascendente_draconico_ascendente_draconico_en_aries
                     key = f"el_ascendente_draconico_en_los_signos_que_es_el_ascendente_draconico_ascendente_draconico_en_{s}"

                if key in self.existing_keys:
                    self.found_keys.append(key)
                else:
                    self.missing_keys.append(key)
                    # print(f"MISSING PLANET: {key}")

    def audit_contacts(self):
        print("\n--- Auditing Contacts ---")
        # Pattern: contactos_entre_planetas_draconicos_y_tropicos_{aspect}_de_{p1}_draconico_con_{p2}_tropico
        # Aspects: conjuncion, oposicion, cuadratura? (Draco is usually Conjunction/Opposition?)
        # Files say: "Contactos entre planetas dracónicos..."
        # Let's check available aspects in keys.
        
        aspects = ["conjuncion", "oposicion"] # Draco usually focuses on hard aspects or conjunctions to tropical.
        
        # Planets to check? 
        # Sol, Luna, Mercurio, Venus, Marte, Jupiter, Saturno, Urano, Neptuno, Pluton, Nodo Norte?
        planets = ["sol", "luna", "mercurio", "venus", "marte", "jupiter", "saturno", "urano", "neptuno", "pluton"]
        
        for p1 in planets:
            for p2 in ["sol"]: # Usually Draco Planet vs Tropical Sun/Moon/Angles?
                # The text usually describes: "Sol Dracónico con Sol Trópico", "Luna Dracónica con Sol Trópico"
                # It seems p2 is often the Tropical luminary or angle?
                # Let's iterate p1 (Draco) vs Sol (Tropical) as a baseline test.
                
                for asp in aspects:
                    key = f"contactos_entre_planetas_draconicos_y_tropicos_{asp}_de_{p1}_draconico_con_{p2}_tropico"
                    
                    if key in self.existing_keys:
                        self.found_keys.append(key)
                    elif p1 == "nodo_norte": 
                        pass # complicated
                    else:
                        self.missing_keys.append(key)
                        # print(f"MISSING CONTACT: {key}")

    def report(self):
        print(f"\nTotal Keys in JSON: {len(self.existing_keys)}")
        print(f"Audit Found: {len(self.found_keys)}")
        print(f"Audit Missing: {len(self.missing_keys)}")
        
if __name__ == "__main__":
    audit = DraconicAudit("data/draco.json")
    audit.audit_superpositions()
    audit.audit_planets_signs()
    audit.audit_contacts()
    audit.report()
