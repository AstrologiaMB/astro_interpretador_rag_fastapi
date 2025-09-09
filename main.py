import os
import sys # Import sys for exit()
import pandas as pd
import json
import re # Added for parsing titles
from pathlib import Path
from dotenv import load_dotenv

from llama_index import SimpleDirectoryReader, GPTVectorStoreIndex, ServiceContext
from llama_index.llms import OpenAI
from llama_index.embeddings import OpenAIEmbedding
from llama_index.prompts import PromptTemplate

# 🔐 Cargar las claves API desde el archivo .env
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
xai_key = os.getenv("XAI_API_KEY")

# 🤖 Selección del LLM a utilizar
llm_choice = input("🤖 Seleccione el LLM a utilizar (1: OpenAI, 2: Grok): ").strip()
while llm_choice not in ["1", "2"]:
    llm_choice = input("⚠️ Opción inválida. Seleccione (1: OpenAI, 2: Grok): ").strip()

# ⚙️ Configurar el modelo de lenguaje y embeddings (Base para RAG)
if llm_choice == "1":
    llm_name = "openai"
    llm_rag = OpenAI(api_key=openai_key, temperature=0.0, model="gpt-3.5-turbo")
    # Siempre usar OpenAI para embeddings
    embed_model = OpenAIEmbedding(api_key=openai_key)
    service_context_rag = ServiceContext.from_defaults(llm=llm_rag, embed_model=embed_model)
else:
    llm_name = "grok"
    # Para Grok, necesitamos usar directamente la API sin llama_index debido a compatibilidad
    print("🔄 Configurando Grok como LLM...")
    
    # Importar las bibliotecas necesarias para usar Grok directamente
    from openai import OpenAI as DirectOpenAI
    
    # Crear cliente directo para Grok
    grok_client = DirectOpenAI(
        api_key=xai_key,
        base_url="https://api.x.ai/v1"
    )
    
    # Usar OpenAI para embeddings y RAG
    embed_model = OpenAIEmbedding(api_key=openai_key)
    
    # Usar gpt-3.5-turbo para RAG pero guardaremos que estamos usando Grok para el rewriter
    llm_rag = OpenAI(api_key=openai_key, temperature=0.0, model="gpt-3.5-turbo")
    service_context_rag = ServiceContext.from_defaults(llm=llm_rag, embed_model=embed_model)

# 📂 Leer el archivo de interpretaciones MARKDOWN específico desde la carpeta /data
try:
    # Cargar archivos numerados (1 - *.md hasta 19 - *.md)
    interpretaciones_dir = Path("data")
    md_files = sorted([f for f in interpretaciones_dir.glob("[0-9]*.md")])  # Solo archivos que empiecen con número
    
    if not md_files:
        print(f"❌ Error: No se encontraron archivos de interpretaciones numerados en: {interpretaciones_dir}")
        print("📋 Archivos .md encontrados:")
        all_md_files = list(interpretaciones_dir.glob("*.md"))
        for f in all_md_files:
            print(f"  - {f.name}")
        sys.exit(1)
    
    print(f"📄 Cargando {len(md_files)} archivos modulares de interpretaciones:")
    for f in md_files:
        print(f"  - {f.name}")
    
    documents = SimpleDirectoryReader(input_files=md_files).load_data()
    if not documents:
        print(f"❌ Error: No se pudieron cargar los documentos desde los archivos modulares")
        sys.exit(1)
    
    print(f"📊 Total de documentos cargados: {len(documents)}")
    index = GPTVectorStoreIndex.from_documents(documents, service_context=service_context_rag)
except Exception as e:
    print(f"❌ Error al cargar o indexar los archivos Markdown de interpretaciones: {e}")
    sys.exit(1)


# 🧠 Definir prompt BASE en español (respuesta breve, clara y basada ESTRICTAMENTE en el texto proporcionado)
base_custom_prompt_template = PromptTemplate(
    "IMPORTANTE: Responde EXCLUSIVAMENTE en idioma español. Basa tu respuesta ÚNICAMENTE en la información proporcionada a continuación. No añadas información externa.\n"
    "Contexto Astrológico:\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Consulta Específica: {query_str}\n"
    "Interpretación Breve (en español):"
)

# --- Carga y Procesamiento de Datos de Eventos ---

def load_and_extract_events(file_path_str):
    """Carga datos de un archivo CSV o JSON y extrae eventos estandarizados."""
    file_path = Path(file_path_str)
    if not file_path.is_file():
        print(f"❌ Error: El archivo no existe en la ruta: {file_path}")
        return None, None, None, None # Devolver cuatro Nones

    standardized_events = []
    file_type = file_path.suffix.lower()
    chart_name = None
    raw_json_data = None # Para guardar los datos crudos del JSON

    try:
        if file_type == ".csv":
            df = pd.read_csv(file_path)
            print(f"📄 Leyendo archivo CSV: {file_path.name}")
            for _, row in df.iterrows():
                event = {
                    "tipo": row["tipo_evento"],
                    "descripcion_original": row.to_dict()
                }
                if event["tipo"] == "Aspecto":
                    event["planeta1"] = row["planeta1"]
                    event["aspecto"] = row["tipo_aspecto"]
                    event["planeta2"] = row["planeta2"]
                elif event["tipo"] == "PlanetaEnSigno":
                    event["planeta"] = row.get("planeta", row.get("descripcion", "").split(" en ")[0])
                    event["signo"] = row.get("signo", row.get("descripcion", "").split(" en ")[-1])
                elif event["tipo"] == "PlanetaEnCasa":
                    event["planeta"] = row.get("planeta", row.get("descripcion", "").split(" en ")[0])
                    event["casa"] = row.get("casa", row.get("descripcion", "").split(" en ")[-1])
                standardized_events.append(event)

        elif file_type == ".json":
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            raw_json_data = data # Guardar datos crudos para cálculo de casas
            print(f"📄 Leyendo archivo JSON: {file_path.name}")
            chart_name = data.get("nombre", file_path.stem)

            if "points" in data:
                for name, details in data["points"].items():
                    if "sign" in details:
                         event_data = {
                             "tipo": "PlanetaEnSigno",
                             "planeta": name,
                             "signo": details["sign"],
                             "grados": details.get("degrees")
                         }
                         standardized_events.append(event_data)
                         if details.get("retrograde", False):
                             standardized_events.append({
                                 "tipo": "PlanetaRetrogrado",
                                 "planeta": name
                             })
            if "houses" in data:
                 for house_num, details in data["houses"].items():
                     if "sign" in details:
                         standardized_events.append({
                             "tipo": "CasaEnSigno",
                             "casa": house_num,
                             "signo": details["sign"]
                         })
            if "aspects" in data:
                for aspect_details in data["aspects"]:
                    standardized_events.append({
                        "tipo": "Aspecto",
                        "planeta1": aspect_details["point1"],
                        "aspecto": aspect_details["aspect"],
                        "planeta2": aspect_details["point2"]
                    })
        else:
            print(f"❌ Error: Tipo de archivo no soportado: {file_type}")
            return None, None, None, None

        print(f"📊 Total de eventos iniciales extraídos: {len(standardized_events)}")
        return standardized_events, chart_name, raw_json_data, file_type

    except Exception as e:
        print(f"❌ Error al procesar el archivo {file_path.name}: {e}")
        return None, None, None, None

# --- Traducciones y Generación de Consultas ---

PLANET_TRANSLATIONS_ES = {
    "Sun": "Sol", "Moon": "Luna", "Mercury": "Mercurio", "Venus": "Venus", "Mars": "Marte",
    "Jupiter": "Júpiter", "Saturn": "Saturno", "Uranus": "Urano", "Neptune": "Neptuno",
    "Pluto": "Plutón", "Asc": "Ascendente", "MC": "Medio Cielo", "Ic": "Fondo del Cielo",
    "Dsc": "Descendente", "True North Node": "Nodo Norte Verdadero",
    "Lilith": "Lilith", "Chiron": "Quirón",
    "Part of Fortune": "Parte de la Fortuna", "Vertex": "Vertex"
}

# Mapeo especial para generar consultas de nodos que coincidan con los títulos
NODE_QUERY_MAPPING = {
    "True North Node": "nodo"  # Para generar consultas como "nodo en géminis"
}
SIGN_TRANSLATIONS_ES = {
    "Aries": "Aries", "Taurus": "Tauro", "Gemini": "Géminis", "Cancer": "Cáncer",
    "Leo": "Leo", "Virgo": "Virgo", "Libra": "Libra", "Scorpio": "Escorpio",
    "Sagittarius": "Sagitario", "Capricorn": "Capricornio", "Aquarius": "Acuario",
    "Pisces": "Piscis"
}
ASPECT_TRANSLATIONS_ES = {
    "Conjunción": "Conjunción", "Oposición": "Oposición", "Cuadratura": "Cuadratura",
    "Trígono": "Trígono", "Sextil": "Sextil"
}

def translate(term, translation_dict):
    return translation_dict.get(term, term)

def format_degrees(decimal_degrees):
    if decimal_degrees is None: return ""
    degrees = int(decimal_degrees)
    minutes = int(round((decimal_degrees - degrees) * 60))
    return f"{degrees}° {minutes:02d}'"

def generar_consulta_estandarizada(evento):
    # Generate queries in lowercase to match normalized target titles
    tipo = evento.get("tipo")
    if tipo == "Aspecto":
        p1_es = translate(evento.get('planeta1'), PLANET_TRANSLATIONS_ES)
        asp_es = translate(evento.get('aspecto'), ASPECT_TRANSLATIONS_ES)
        p2_es = translate(evento.get('planeta2'), PLANET_TRANSLATIONS_ES)
        # Ensure aspect query matches lowercase format like "aspecto sol conjunción a venus"
        # Added " a " before the second planet
        return f"aspecto {p1_es.lower()} {asp_es.lower()} a {p2_es.lower()}"
    elif tipo == "PlanetaEnSigno":
        planeta_orig = evento.get('planeta')
        # Usar mapeo especial para nodos si aplica
        if planeta_orig in NODE_QUERY_MAPPING:
            planeta_query = NODE_QUERY_MAPPING[planeta_orig]
        else:
            planeta_es = translate(planeta_orig, PLANET_TRANSLATIONS_ES)
            planeta_query = planeta_es.lower()
        
        signo_es = translate(evento.get('signo'), SIGN_TRANSLATIONS_ES)
        return f"{planeta_query} en {signo_es.lower()}"
    elif tipo == "PlanetaEnCasa":
        planeta_orig = evento.get('planeta')
        # Usar mapeo especial para nodos si aplica
        if planeta_orig in NODE_QUERY_MAPPING:
            planeta_query = NODE_QUERY_MAPPING[planeta_orig]
        else:
            planeta_es = translate(planeta_orig, PLANET_TRANSLATIONS_ES)
            planeta_query = planeta_es.lower()
        
        # Ensure house query matches lowercase format like "sol en casa 9"
        return f"{planeta_query} en casa {evento.get('casa')}"
    elif tipo == "CasaEnSigno":
        signo_es = translate(evento.get('signo'), SIGN_TRANSLATIONS_ES)
        # Ensure cusp query matches lowercase format like "casa 1 en piscis"
        return f"casa {evento.get('casa')} en {signo_es.lower()}"
    elif tipo == "PlanetaRetrogrado":
        planeta_orig = evento.get('planeta')
        # Usar mapeo especial para nodos si aplica
        if planeta_orig in NODE_QUERY_MAPPING:
            planeta_query = NODE_QUERY_MAPPING[planeta_orig]
        else:
            planeta_es = translate(planeta_orig, PLANET_TRANSLATIONS_ES)
            planeta_query = planeta_es.lower()
        
        # Ensure retrograde query matches lowercase format like "mercurio retrógrado"
        return f"{planeta_query} retrógrado"
    else:
        if "descripcion_original" in evento and isinstance(evento["descripcion_original"], dict):
             if evento["descripcion_original"].get("tipo_evento") != "Aspecto":
                 return f"{evento['descripcion_original'].get('tipo_evento')} {evento['descripcion_original'].get('descripcion')}"
        return f"Evento {tipo}: {evento}"

# --- Cálculo de Casas ---

def calculate_house_placements(planets_data, houses_data):
    """Calcula en qué casa cae cada planeta usando longitudes."""
    if not planets_data or not houses_data:
        return {}

    cusps_lon = {}
    for i in range(1, 13):
        house_num_str = str(i)
        if house_num_str in houses_data:
            cusps_lon[i] = houses_data[house_num_str]['longitude']
        else:
            print(f"⚠️ Advertencia: Faltan datos para la cúspide de la casa {i}")
            return {}

    if len(cusps_lon) != 12:
         print(f"⚠️ Advertencia: Se encontraron {len(cusps_lon)} cúspides en lugar de 12.")
         return {}

    house_placements = {}
    # Iterar sobre planetas y puntos relevantes (excluir Asc, MC, etc. que definen casas)
    relevant_points = {k: v for k, v in planets_data.items() if k not in ["Asc", "MC", "Ic", "Dsc", "Vertex", "Part of Fortune"]}

    for planet_name, planet_details in relevant_points.items():
        planet_lon = planet_details.get('longitude')
        if planet_lon is None:
            continue

        assigned_house = None
        for i in range(1, 13):
            house_num = i
            next_house_num = (i % 12) + 1

            start_lon = cusps_lon[house_num]
            end_lon = cusps_lon[next_house_num]

            crosses_aries_point = end_lon < start_lon

            if crosses_aries_point:
                if planet_lon >= start_lon or planet_lon < end_lon:
                    assigned_house = house_num
                    break
            else:
                if planet_lon >= start_lon and planet_lon < end_lon:
                    assigned_house = house_num
                    break

        if assigned_house is not None:
            house_placements[planet_name] = assigned_house
        # else:
             # print(f"⚠️ Advertencia: No se pudo determinar la casa para {planet_name} (lon: {planet_lon})")

    return house_placements

# --- Cargar Títulos Requeridos ---

def load_target_titles(filepath="Títulos Numerados tropico.md"):
    """Lee el archivo Markdown, extrae y normaliza títulos, expandiendo aspectos compuestos."""
    target_titles = set()
    # Define possible aspect keywords found in compound titles
    aspect_keywords = ["conjunción", "oposición", "cuadratura", "trígono", "sextil"]
    try:
        # Use pathlib for more robust path handling
        path_obj = Path(filepath)
        if not path_obj.is_file():
             # Raise FileNotFoundError explicitly if Path object confirms non-existence
             raise FileNotFoundError(f"Path object reports file not found: {filepath}")

        with path_obj.open('r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Updated regex to capture text after numbering like "### 1.1.8 " or "#### 1.3.9.1 "
                match_header = re.match(r"^(?:### |#### )\s*\d+(?:\.\d+)*\s+(.*)", line)
                # Also capture ## headers for retrograde planets (like "## 5.1 MERCURIO RETRÓGRADO")
                match_retrograde = re.match(r"^## \d+\.\d+\s+([A-ZÁÉÍÓÚÜÑ]+\s+RETRÓGRADO)", line)
                title_to_process = None

                if match_header:
                    title_to_process = match_header.group(1).strip()
                elif match_retrograde:
                    title_to_process = match_retrograde.group(1).strip()
                elif re.match(r"^[A-Z\s]+ RETRÓGRADO", line): # Handle uppercase RETROGRADE lines, assumes no number
                    title_to_process = line.strip()

                if title_to_process:
                    # Basic normalization
                    normalized_title = re.sub(r'\s*\(\d+°.*?\)', '', title_to_process) # Remove degrees
                    normalized_title = re.sub(r':.*', '', normalized_title) # Remove conditions after ':'
                    normalized_title = normalized_title.lower() # Convert to lowercase
                    normalized_title = re.sub(r'\s+', ' ', normalized_title).strip() # Collapse multiple spaces

                    # Convert number words in house references (add more if needed)
                    normalized_title = normalized_title.replace(" en casa dos", " en casa 2")
                    # Add other number words if they appear in titles, e.g.:
                    # normalized_title = normalized_title.replace(" en casa tres", " en casa 3")


                    # Check if it's a relevant type BEFORE potentially expanding aspects
                    is_relevant = (
                        normalized_title.startswith("aspecto ") or
                        " en " in normalized_title or
                        normalized_title.endswith(" retrógrado") or
                        " en el ascendente" in normalized_title
                    )

                    if is_relevant:
                        # Expand compound aspects
                        if normalized_title.startswith("aspecto "):
                            # Extract parts: "aspecto planet1 aspects... a planet2"
                            match_aspect = re.match(r"aspecto\s+([a-záéíóúüñ]+)\s+(.*?)\s+a\s+([a-záéíóúüñ]+)", normalized_title)
                            if match_aspect:
                                planet1 = match_aspect.group(1)
                                aspect_part = match_aspect.group(2)
                                planet2 = match_aspect.group(3)

                                # Find individual aspect keywords within the compound part
                                found_aspects = [kw for kw in aspect_keywords if kw in aspect_part.split()]

                                if found_aspects:
                                    # Add each specific aspect combination
                                     for asp in found_aspects:
                                         specific_title = f"aspecto {planet1} {asp} a {planet2}"
                                         target_titles.add(specific_title)
                                else:
                                    # If no keywords found, assume it's already specific or malformed, add as is
                                    target_titles.add(normalized_title)
                            else:
                                # If regex doesn't match expected aspect format, add as is
                                target_titles.add(normalized_title)
                        else:
                            # Add non-aspect titles directly
                            target_titles.add(normalized_title)

        print(f"🎯 Títulos objetivo cargados, normalizados y expandidos desde '{filepath}': {len(target_titles)}")
        if not target_titles:
             print(f"⚠️ Advertencia: No se extrajeron títulos de '{filepath}'. El informe estará vacío.")
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo de títulos: {filepath}")
        target_titles = None # Indicar error
    except Exception as e:
        print(f"❌ Error al leer o procesar el archivo de títulos '{filepath}': {e}")
        target_titles = None # Indicar error
    return target_titles

# --- Funciones para Aspectos Complejos ---

def check_aspect_exists(eventos, planeta1, aspectos_lista, planeta2):
    """Verifica si existe un aspecto específico entre dos planetas."""
    for evento in eventos:
        if evento.get("tipo") == "Aspecto":
            p1 = evento.get("planeta1")
            p2 = evento.get("planeta2")
            aspecto = evento.get("aspecto")
            
            # Verificar ambas direcciones del aspecto
            if ((p1 == planeta1 and p2 == planeta2) or (p1 == planeta2 and p2 == planeta1)) and aspecto in aspectos_lista:
                return True, aspecto
    return False, None

def check_planet_in_angular_houses(planets_in_houses, planetas_lista):
    """Verifica si algún planeta de la lista está en casas angulares (1, 4, 7, 10)."""
    casas_angulares = [1, 4, 7, 10]
    for planeta in planetas_lista:
        casa = planets_in_houses.get(planeta)
        if casa in casas_angulares:
            return True, planeta, casa
    return False, None, None

def check_planet_conjunct_to_personals(eventos, planetas_lista):
    """Verifica si algún planeta de la lista está en conjunción con planetas personales."""
    planetas_personales = ["Sun", "Moon", "Mercury", "Venus", "Mars"]
    for planeta in planetas_lista:
        for personal in planetas_personales:
            exists, _ = check_aspect_exists(eventos, planeta, ["Conjunción"], personal)
            if exists:
                return True, planeta, personal
    return False, None, None

def check_planet_square_to_personals(eventos, planetas_lista):
    """Verifica si algún planeta de la lista está en cuadratura con planetas personales."""
    planetas_personales = ["Sun", "Moon", "Mercury", "Venus", "Mars"]
    for planeta in planetas_lista:
        for personal in planetas_personales:
            exists, _ = check_aspect_exists(eventos, planeta, ["Cuadratura"], personal)
            if exists:
                return True, planeta, personal
    return False, None, None

def check_ascendant_sign(raw_json_data, signo_objetivo):
    """Verifica si el Ascendente está en un signo específico."""
    if not raw_json_data or "points" not in raw_json_data:
        return False
    
    asc_data = raw_json_data["points"].get("Asc", {})
    asc_sign = asc_data.get("sign")
    return asc_sign == signo_objetivo

def check_planet_in_house(planets_in_houses, planeta, casa_objetivo):
    """Verifica si un planeta específico está en una casa específica."""
    casa = planets_in_houses.get(planeta)
    return casa == casa_objetivo

def check_planet_conjunct_to_specific(eventos, planeta, planetas_objetivo):
    """Verifica si un planeta está en conjunción con alguno de los planetas objetivo."""
    for objetivo in planetas_objetivo:
        exists, _ = check_aspect_exists(eventos, planeta, ["Conjunción"], objetivo)
        if exists:
            return True, objetivo
    return False, None

def check_exclusions_not_met(planets_in_houses, eventos, exclusions):
    """Verifica que NINGUNA de las condiciones de exclusión se cumplan."""
    for exclusion in exclusions:
        if exclusion["type"] == "planet_in_house":
            if check_planet_in_house(planets_in_houses, exclusion["planet"], exclusion["house"]):
                return False  # Exclusión se cumple, no usar el aspecto
        elif exclusion["type"] == "aspect_exists":
            exists, _ = check_aspect_exists(eventos, exclusion["planet1"], [exclusion["aspect"]], exclusion["planet2"])
            if exists:
                return False  # Exclusión se cumple, no usar el aspecto
    return True  # Ninguna exclusión se cumple, usar el aspecto

def generate_specific_complex_title(base_title, detected_conditions):
    """Genera un título específico basado en las condiciones detectadas."""
    title = base_title
    
    # Reemplazar aspectos genéricos con específicos
    if "detected_aspect" in detected_conditions:
        aspect = detected_conditions["detected_aspect"]
        title = title.replace("conjunción, cuadratura u oposición", aspect.lower())
    
    # Reemplazar planetas genéricos con específicos
    if "detected_planet" in detected_conditions:
        planet = detected_conditions["detected_planet"]
        planet_es = translate(planet, PLANET_TRANSLATIONS_ES)
        if "Saturno o Plutón" in title:
            title = title.replace("Saturno o Plutón", planet_es)
    
    # Reemplazar casas genéricas con específicas
    if "detected_house" in detected_conditions:
        house = detected_conditions["detected_house"]
        title = title.replace("casa 1, 4, 7 o 10", f"casa {house}")
    
    # Reemplazar planetas personales genéricos con específicos
    if "detected_personal" in detected_conditions:
        personal = detected_conditions["detected_personal"]
        personal_es = translate(personal, PLANET_TRANSLATIONS_ES)
        if "Sol, la Luna, Mercurio, Venus o Marte" in title:
            title = title.replace("Sol, la Luna, Mercurio, Venus o Marte", personal_es)
    
    return title

def evaluate_complex_aspects(eventos, planets_in_houses, raw_json_data):
    """Evalúa aspectos complejos y retorna eventos adicionales si se cumplen las condiciones."""
    complex_events = []
    
    print("🔍 Evaluando aspectos complejos...")
    
    # GRUPO 1: Sol-Júpiter con condiciones adicionales
    sol_jupiter_exists, sol_jupiter_aspect = check_aspect_exists(eventos, "Sun", ["Conjunción", "Cuadratura", "Oposición"], "Jupiter")
    
    if sol_jupiter_exists:
        print(f"✓ Encontrado aspecto Sol-Júpiter: {sol_jupiter_aspect}")
        
        # 1.3.9: Sol-Júpiter + Saturno/Plutón en casas angulares
        angular_exists, angular_planet, angular_house = check_planet_in_angular_houses(planets_in_houses, ["Saturn", "Pluto"])
        if angular_exists:
            base_title = "Aspecto Sol en conjunción, cuadratura u oposición a Júpiter y Saturno o Plutón están en casa 1, 4, 7 o 10"
            conditions = {
                "detected_aspect": sol_jupiter_aspect,
                "detected_planet": angular_planet,
                "detected_house": angular_house
            }
            specific_title = generate_specific_complex_title(base_title, conditions)
            complex_events.append({
                "tipo": "AspectoComplejo",
                "titulo_especifico": specific_title,
                "descripcion": f"Sol {sol_jupiter_aspect} Júpiter y {translate(angular_planet, PLANET_TRANSLATIONS_ES)} en casa {angular_house}"
            })
            print(f"✓ Detectado: {specific_title}")
        
        # 1.3.10: Sol-Júpiter + Saturno/Plutón conjunción a personales
        conjunct_exists, conjunct_planet, conjunct_personal = check_planet_conjunct_to_personals(eventos, ["Saturn", "Pluto"])
        if conjunct_exists:
            base_title = "Aspecto Sol en conjunción, cuadratura u oposición a Júpiter y Saturno o Plutón están en conjunción al Sol, la Luna, Mercurio, Venus o Marte"
            conditions = {
                "detected_aspect": sol_jupiter_aspect,
                "detected_planet": conjunct_planet,
                "detected_personal": conjunct_personal
            }
            specific_title = generate_specific_complex_title(base_title, conditions)
            complex_events.append({
                "tipo": "AspectoComplejo",
                "titulo_especifico": specific_title,
                "descripcion": f"Sol {sol_jupiter_aspect} Júpiter y {translate(conjunct_planet, PLANET_TRANSLATIONS_ES)} conjunción {translate(conjunct_personal, PLANET_TRANSLATIONS_ES)}"
            })
            print(f"✓ Detectado: {specific_title}")
        
        # 1.3.11: Sol-Júpiter + Saturno/Plutón cuadratura a personales
        square_exists, square_planet, square_personal = check_planet_square_to_personals(eventos, ["Saturn", "Pluto"])
        if square_exists:
            base_title = "Aspecto Sol en conjunción, cuadratura u oposición a Júpiter y Saturno o Plutón están en cuadratura al Sol, la Luna, Mercurio, Venus o Marte"
            conditions = {
                "detected_aspect": sol_jupiter_aspect,
                "detected_planet": square_planet,
                "detected_personal": square_personal
            }
            specific_title = generate_specific_complex_title(base_title, conditions)
            complex_events.append({
                "tipo": "AspectoComplejo",
                "titulo_especifico": specific_title,
                "descripcion": f"Sol {sol_jupiter_aspect} Júpiter y {translate(square_planet, PLANET_TRANSLATIONS_ES)} cuadratura {translate(square_personal, PLANET_TRANSLATIONS_ES)}"
            })
            print(f"✓ Detectado: {specific_title}")
        
        # 1.3.12: Sol-Júpiter + aspecto Saturno-Plutón
        saturn_pluto_exists, saturn_pluto_aspect = check_aspect_exists(eventos, "Saturn", ["Conjunción", "Cuadratura", "Oposición"], "Pluto")
        if saturn_pluto_exists:
            base_title = "Aspecto Sol en conjunción, cuadratura u oposición a Júpiter y hay conjunción, cuadratura u oposición entre Saturno y Plutón"
            specific_title = f"Aspecto Sol {sol_jupiter_aspect.lower()} a Júpiter y hay {saturn_pluto_aspect.lower()} entre Saturno y Plutón"
            complex_events.append({
                "tipo": "AspectoComplejo",
                "titulo_especifico": specific_title,
                "descripcion": f"Sol {sol_jupiter_aspect} Júpiter y Saturno {saturn_pluto_aspect} Plutón"
            })
            print(f"✓ Detectado: {specific_title}")
    
    # GRUPO 2: Luna-Júpiter con condiciones adicionales
    luna_jupiter_exists, luna_jupiter_aspect = check_aspect_exists(eventos, "Moon", ["Conjunción", "Cuadratura", "Oposición"], "Jupiter")
    
    if luna_jupiter_exists:
        print(f"✓ Encontrado aspecto Luna-Júpiter: {luna_jupiter_aspect}")
        
        # 2.3.10: Luna-Júpiter + Saturno/Plutón en casas angulares
        angular_exists, angular_planet, angular_house = check_planet_in_angular_houses(planets_in_houses, ["Saturn", "Pluto"])
        if angular_exists:
            base_title = "Aspecto Luna en conjunción, cuadratura u oposición a Júpiter y Saturno o Plutón están en casa 1, 4, 7 o 10"
            conditions = {
                "detected_aspect": luna_jupiter_aspect,
                "detected_planet": angular_planet,
                "detected_house": angular_house
            }
            specific_title = generate_specific_complex_title(base_title, conditions)
            complex_events.append({
                "tipo": "AspectoComplejo",
                "titulo_especifico": specific_title,
                "descripcion": f"Luna {luna_jupiter_aspect} Júpiter y {translate(angular_planet, PLANET_TRANSLATIONS_ES)} en casa {angular_house}"
            })
            print(f"✓ Detectado: {specific_title}")
        
        # 2.3.11: Luna-Júpiter + Saturno/Plutón conjunción a personales
        conjunct_exists, conjunct_planet, conjunct_personal = check_planet_conjunct_to_personals(eventos, ["Saturn", "Pluto"])
        if conjunct_exists:
            base_title = "Aspecto Luna en conjunción, cuadratura u oposición a Júpiter y Saturno o Plutón están en conjunción al Sol, la Luna, Mercurio, Venus o Marte"
            conditions = {
                "detected_aspect": luna_jupiter_aspect,
                "detected_planet": conjunct_planet,
                "detected_personal": conjunct_personal
            }
            specific_title = generate_specific_complex_title(base_title, conditions)
            complex_events.append({
                "tipo": "AspectoComplejo",
                "titulo_especifico": specific_title,
                "descripcion": f"Luna {luna_jupiter_aspect} Júpiter y {translate(conjunct_planet, PLANET_TRANSLATIONS_ES)} conjunción {translate(conjunct_personal, PLANET_TRANSLATIONS_ES)}"
            })
            print(f"✓ Detectado: {specific_title}")
        
        # 2.3.12: Luna-Júpiter + Saturno/Plutón cuadratura a personales
        square_exists, square_planet, square_personal = check_planet_square_to_personals(eventos, ["Saturn", "Pluto"])
        if square_exists:
            base_title = "Aspecto Luna en conjunción, cuadratura u oposición a Júpiter y Saturno o Plutón están en cuadratura al Sol, la Luna, Mercurio, Venus o Marte"
            conditions = {
                "detected_aspect": luna_jupiter_aspect,
                "detected_planet": square_planet,
                "detected_personal": square_personal
            }
            specific_title = generate_specific_complex_title(base_title, conditions)
            complex_events.append({
                "tipo": "AspectoComplejo",
                "titulo_especifico": specific_title,
                "descripcion": f"Luna {luna_jupiter_aspect} Júpiter y {translate(square_planet, PLANET_TRANSLATIONS_ES)} cuadratura {translate(square_personal, PLANET_TRANSLATIONS_ES)}"
            })
            print(f"✓ Detectado: {specific_title}")
        
        # 2.3.13: Luna-Júpiter + aspecto Saturno-Plutón
        saturn_pluto_exists, saturn_pluto_aspect = check_aspect_exists(eventos, "Saturn", ["Conjunción", "Cuadratura", "Oposición"], "Pluto")
        if saturn_pluto_exists:
            base_title = "Aspecto Luna en conjunción, cuadratura u oposición a Júpiter y hay conjunción, cuadratura u oposición entre Saturno y Plutón"
            specific_title = f"Aspecto Luna {luna_jupiter_aspect.lower()} a Júpiter y hay {saturn_pluto_aspect.lower()} entre Saturno y Plutón"
            complex_events.append({
                "tipo": "AspectoComplejo",
                "titulo_especifico": specific_title,
                "descripcion": f"Luna {luna_jupiter_aspect} Júpiter y Saturno {saturn_pluto_aspect} Plutón"
            })
            print(f"✓ Detectado: {specific_title}")
    
    # GRUPO 3: Luna-Urano con condiciones adicionales
    luna_urano_exists, luna_urano_aspect = check_aspect_exists(eventos, "Moon", ["Conjunción", "Cuadratura", "Oposición"], "Uranus")
    
    if luna_urano_exists:
        print(f"✓ Encontrado aspecto Luna-Urano: {luna_urano_aspect}")
        
        # 2.3.17: Luna-Urano + Saturno en casas angulares
        saturn_angular = check_planet_in_angular_houses(planets_in_houses, ["Saturn"])
        if saturn_angular[0]:
            base_title = "Aspecto Luna en conjunción, cuadratura u oposición a Urano y Saturno está en casa 1, 4, 7 o 10"
            specific_title = f"Aspecto Luna {luna_urano_aspect.lower()} a Urano y Saturno en casa {saturn_angular[2]}"
            complex_events.append({
                "tipo": "AspectoComplejo",
                "titulo_especifico": specific_title,
                "descripcion": f"Luna {luna_urano_aspect} Urano y Saturno en casa {saturn_angular[2]}"
            })
            print(f"✓ Detectado: {specific_title}")
        
        # 2.3.18: Luna-Urano + Saturno conjunción a personales
        saturn_conjunct_exists, saturn_conjunct_personal = check_planet_conjunct_to_specific(eventos, "Saturn", ["Sun", "Moon", "Mercury", "Venus", "Mars"])
        if saturn_conjunct_exists:
            base_title = "Aspecto Luna en conjunción, cuadratura u oposición a Urano y Saturno está en conjunción al Sol, la Luna, Mercurio, Venus o Marte"
            specific_title = f"Aspecto Luna {luna_urano_aspect.lower()} a Urano y Saturno conjunción {translate(saturn_conjunct_personal, PLANET_TRANSLATIONS_ES)}"
            complex_events.append({
                "tipo": "AspectoComplejo",
                "titulo_especifico": specific_title,
                "descripcion": f"Luna {luna_urano_aspect} Urano y Saturno conjunción {translate(saturn_conjunct_personal, PLANET_TRANSLATIONS_ES)}"
            })
            print(f"✓ Detectado: {specific_title}")
        
        # 2.3.19: Luna-Urano + Saturno cuadratura a personales
        saturn_square_exists, saturn_square_personal = check_planet_square_to_personals(eventos, ["Saturn"])
        if saturn_square_exists:
            base_title = "Aspecto Luna en conjunción, cuadratura u oposición a Urano y Saturno está en cuadratura al Sol, la Luna, Mercurio, Venus o Marte"
            specific_title = f"Aspecto Luna {luna_urano_aspect.lower()} a Urano y Saturno cuadratura {translate(saturn_square_personal, PLANET_TRANSLATIONS_ES)}"
            complex_events.append({
                "tipo": "AspectoComplejo",
                "titulo_especifico": specific_title,
                "descripcion": f"Luna {luna_urano_aspect} Urano y Saturno cuadratura {translate(saturn_square_personal, PLANET_TRANSLATIONS_ES)}"
            })
            print(f"✓ Detectado: {specific_title}")
    
    # GRUPO 4: Ascendente en Tauro con condiciones adicionales
    asc_tauro = check_ascendant_sign(raw_json_data, "Taurus")
    
    if asc_tauro:
        print("✓ Encontrado Ascendente en Tauro")
        
        # 4.1.3: Ascendente Tauro + Marte en casas angulares
        mars_angular = check_planet_in_angular_houses(planets_in_houses, ["Mars"])
        if mars_angular[0]:
            specific_title = f"Ascendente en Tauro y Marte en casa {mars_angular[2]}"
            complex_events.append({
                "tipo": "AspectoComplejo",
                "titulo_especifico": specific_title,
                "descripcion": f"Ascendente Tauro y Marte en casa {mars_angular[2]}"
            })
            print(f"✓ Detectado: {specific_title}")
        
        # 4.1.4: Ascendente Tauro + Marte conjunción Sol/Luna
        mars_conjunct_sol_luna, conjunct_target = check_planet_conjunct_to_specific(eventos, "Mars", ["Sun", "Moon"])
        if mars_conjunct_sol_luna:
            specific_title = f"Ascendente en Tauro y Marte conjunción {translate(conjunct_target, PLANET_TRANSLATIONS_ES)}"
            complex_events.append({
                "tipo": "AspectoComplejo",
                "titulo_especifico": specific_title,
                "descripcion": f"Ascendente Tauro y Marte conjunción {translate(conjunct_target, PLANET_TRANSLATIONS_ES)}"
            })
            print(f"✓ Detectado: {specific_title}")
    
    # GRUPO 5: Planetas en el ascendente (Casa 1)
    planetas_ascendente = ["Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]
    
    for planeta in planetas_ascendente:
        if check_planet_in_house(planets_in_houses, planeta, 1):
            planeta_es = translate(planeta, PLANET_TRANSLATIONS_ES)
            specific_title = f"{planeta_es} en el ascendente"
            complex_events.append({
                "tipo": "AspectoComplejo",
                "titulo_especifico": specific_title,
                "descripcion": f"{planeta_es} en Casa 1"
            })
            print(f"✓ Detectado: {specific_title}")
    
    # GRUPO 6: Mercurio-Urano con condiciones adicionales
    mercurio_urano_exists, mercurio_urano_aspect = check_aspect_exists(eventos, "Mercury", ["Conjunción", "Cuadratura", "Oposición"], "Uranus")
    
    if mercurio_urano_exists:
        print(f"✓ Encontrado aspecto Mercurio-Urano: {mercurio_urano_aspect}")
        
        # 5.4.9: Mercurio-Urano + Urano en casas angulares
        urano_angular = check_planet_in_angular_houses(planets_in_houses, ["Uranus"])
        if urano_angular[0]:
            specific_title = f"Aspecto Mercurio {mercurio_urano_aspect.lower()} a Urano y Urano en casa {urano_angular[2]}"
            complex_events.append({
                "tipo": "AspectoComplejo",
                "titulo_especifico": specific_title,
                "descripcion": f"Mercurio {mercurio_urano_aspect} Urano y Urano en casa {urano_angular[2]}"
            })
            print(f"✓ Detectado: {specific_title}")
        
        # 5.4.10: Mercurio-Urano + Urano conjunción Sol/Luna
        urano_conjunct_sol_luna, conjunct_target = check_planet_conjunct_to_specific(eventos, "Uranus", ["Sun", "Moon"])
        if urano_conjunct_sol_luna:
            specific_title = f"Aspecto Mercurio {mercurio_urano_aspect.lower()} a Urano y Urano conjunción {translate(conjunct_target, PLANET_TRANSLATIONS_ES)}"
            complex_events.append({
                "tipo": "AspectoComplejo",
                "titulo_especifico": specific_title,
                "descripcion": f"Mercurio {mercurio_urano_aspect} Urano y Urano conjunción {translate(conjunct_target, PLANET_TRANSLATIONS_ES)}"
            })
            print(f"✓ Detectado: {specific_title}")
    
    # GRUPO 7: Venus en casa 4 con exclusiones
    venus_casa_4 = check_planet_in_house(planets_in_houses, "Venus", 4)
    
    if venus_casa_4:
        print("✓ Encontrado Venus en casa 4, verificando exclusiones...")
        
        # Definir exclusiones
        exclusions = [
            {"type": "planet_in_house", "planet": "Saturn", "house": 4},
            {"type": "planet_in_house", "planet": "Pluto", "house": 4},
            {"type": "aspect_exists", "planet1": "Venus", "aspect": "Conjunción", "planet2": "Saturn"},
            {"type": "aspect_exists", "planet1": "Venus", "aspect": "Conjunción", "planet2": "Pluto"}
        ]
        
        # Verificar que ninguna exclusión se cumpla
        if check_exclusions_not_met(planets_in_houses, eventos, exclusions):
            specific_title = "Venus en la casa 4"
            complex_events.append({
                "tipo": "AspectoComplejo",
                "titulo_especifico": specific_title,
                "descripcion": "Venus en casa 4 sin exclusiones"
            })
            print(f"✓ Detectado: {specific_title} (sin exclusiones)")
        else:
            print("✗ Venus en casa 4 excluido por condiciones restrictivas")
    
    # GRUPO 8: Aspectos complejos Saturno-Urano
    saturn_angular = check_planet_in_angular_houses(planets_in_houses, ["Saturn"])
    urano_angular = check_planet_in_angular_houses(planets_in_houses, ["Uranus"])
    saturn_conjunct_personals = check_planet_conjunct_to_personals(eventos, ["Saturn"])
    urano_conjunct_personals = check_planet_conjunct_to_personals(eventos, ["Uranus"])
    saturn_urano_aspect_exists, saturn_urano_aspect = check_aspect_exists(eventos, "Saturn", ["Conjunción", "Cuadratura", "Oposición"], "Uranus")
    
    # 13.3.10: Saturno y Urano ambos en casas angulares
    if saturn_angular[0] and urano_angular[0]:
        specific_title = f"Saturno en casa {saturn_angular[2]} y Urano en casa {urano_angular[2]}"
        complex_events.append({
            "tipo": "AspectoComplejo",
            "titulo_especifico": specific_title,
            "descripcion": f"Saturno en casa {saturn_angular[2]} y Urano en casa {urano_angular[2]}"
        })
        print(f"✓ Detectado: {specific_title}")
    
    # 13.3.11: Saturno en angulares + Urano conjunción a personales
    if saturn_angular[0] and urano_conjunct_personals[0]:
        specific_title = f"Saturno en casa {saturn_angular[2]} y Urano conjunción {translate(urano_conjunct_personals[2], PLANET_TRANSLATIONS_ES)}"
        complex_events.append({
            "tipo": "AspectoComplejo",
            "titulo_especifico": specific_title,
            "descripcion": f"Saturno en casa {saturn_angular[2]} y Urano conjunción {translate(urano_conjunct_personals[2], PLANET_TRANSLATIONS_ES)}"
        })
        print(f"✓ Detectado: {specific_title}")
    
    # 13.3.12: Saturno en angulares + aspecto Saturno-Urano
    if saturn_angular[0] and saturn_urano_aspect_exists:
        specific_title = f"Saturno en casa {saturn_angular[2]} y hay {saturn_urano_aspect.lower()} entre Saturno y Urano"
        complex_events.append({
            "tipo": "AspectoComplejo",
            "titulo_especifico": specific_title,
            "descripcion": f"Saturno en casa {saturn_angular[2]} y Saturno {saturn_urano_aspect} Urano"
        })
        print(f"✓ Detectado: {specific_title}")
    
    # 13.3.13: Saturno conjunción a personales + Urano en angulares
    if saturn_conjunct_personals[0] and urano_angular[0]:
        specific_title = f"Saturno conjunción {translate(saturn_conjunct_personals[2], PLANET_TRANSLATIONS_ES)} y Urano en casa {urano_angular[2]}"
        complex_events.append({
            "tipo": "AspectoComplejo",
            "titulo_especifico": specific_title,
            "descripcion": f"Saturno conjunción {translate(saturn_conjunct_personals[2], PLANET_TRANSLATIONS_ES)} y Urano en casa {urano_angular[2]}"
        })
        print(f"✓ Detectado: {specific_title}")
    
    # 13.3.14: Saturno y Urano ambos conjunción a personales
    if saturn_conjunct_personals[0] and urano_conjunct_personals[0]:
        specific_title = f"Saturno conjunción {translate(saturn_conjunct_personals[2], PLANET_TRANSLATIONS_ES)} y Urano conjunción {translate(urano_conjunct_personals[2], PLANET_TRANSLATIONS_ES)}"
        complex_events.append({
            "tipo": "AspectoComplejo",
            "titulo_especifico": specific_title,
            "descripcion": f"Saturno conjunción {translate(saturn_conjunct_personals[2], PLANET_TRANSLATIONS_ES)} y Urano conjunción {translate(urano_conjunct_personals[2], PLANET_TRANSLATIONS_ES)}"
        })
        print(f"✓ Detectado: {specific_title}")
    
    # 13.3.15: Saturno conjunción a personales + aspecto Saturno-Urano
    if saturn_conjunct_personals[0] and saturn_urano_aspect_exists:
        specific_title = f"Saturno conjunción {translate(saturn_conjunct_personals[2], PLANET_TRANSLATIONS_ES)} y hay {saturn_urano_aspect.lower()} entre Saturno y Urano"
        complex_events.append({
            "tipo": "AspectoComplejo",
            "titulo_especifico": specific_title,
            "descripcion": f"Saturno conjunción {translate(saturn_conjunct_personals[2], PLANET_TRANSLATIONS_ES)} y Saturno {saturn_urano_aspect} Urano"
        })
        print(f"✓ Detectado: {specific_title}")
    
    # GRUPO 9: Polaridad plutoniana
    pluton_conjunct_sol, _ = check_aspect_exists(eventos, "Pluto", ["Conjunción", "Cuadratura", "Oposición"], "Sun")
    pluton_casa_1 = check_planet_in_house(planets_in_houses, "Pluto", 1)
    
    if pluton_conjunct_sol or pluton_casa_1:
        if pluton_conjunct_sol and pluton_casa_1:
            specific_title = "Polaridad plutoniana: Plutón con el Sol y en casa 1"
            descripcion = "Plutón conjunción Sol y Plutón en casa 1"
        elif pluton_conjunct_sol:
            specific_title = "Polaridad plutoniana: Plutón con el Sol"
            descripcion = "Plutón conjunción Sol"
        else:
            specific_title = "Polaridad plutoniana: Plutón en casa 1"
            descripcion = "Plutón en casa 1"
        
        complex_events.append({
            "tipo": "AspectoComplejo",
            "titulo_especifico": specific_title,
            "descripcion": descripcion
        })
        print(f"✓ Detectado: {specific_title}")
    
    print(f"📊 Total aspectos complejos detectados: {len(complex_events)}")
    return complex_events

# --- Ejecución Principal ---

if __name__ == "__main__":
    input_file_path = input("➡️ Introduce la ruta completa al archivo de eventos (CSV o JSON): ")
    eventos, chart_name, raw_json_data, file_type = load_and_extract_events(input_file_path)

    if eventos:
        input_path_obj = Path(input_file_path)
        # file_type ya viene de load_and_extract_events

        # --- Calcular Planetas en Casas (Solo para JSON) ---
        if file_type == ".json" and raw_json_data:
            planets_in_houses = calculate_house_placements(raw_json_data.get('points', {}), raw_json_data.get('houses', {}))
            print(f"🏠 Planetas en Casas calculados: {planets_in_houses}")
            # Añadir eventos de PlanetaEnCasa a la lista principal
            for planet, house in planets_in_houses.items():
                eventos.append({
                    "tipo": "PlanetaEnCasa",
                    "planeta": planet,
                    "casa": house
                })
            print(f"📊 Total de eventos (incluyendo casas): {len(eventos)}")


        # --- Determinar Género y Crear Prompt Final (Solo para JSON) ---
        final_prompt_template_rag = base_custom_prompt_template
        genero_instruccion = ""
        persona_instruccion = ""

        if file_type == ".json":
            genero_input = ""
            while genero_input.lower() not in ['hombre', 'mujer']:
                genero_input = input(f"👤 El informe es para '{chart_name}'. ¿Es 'Hombre' o 'Mujer'? ").strip()

            if genero_input.lower() == 'mujer':
                genero_instruccion = "Instrucción adicional: Redacta usando el género gramatical femenino."
            elif genero_input.lower() == 'hombre':
                 genero_instruccion = "Instrucción adicional: Redacta usando el género gramatical masculino."

            persona_instruccion = "Instrucción adicional: Dirígete directamente a la persona usando la segunda persona singular (Tú)."
            instrucciones_adicionales = f"{genero_instruccion}\n{persona_instruccion}".strip()

            if instrucciones_adicionales:
                 prompt_template_str = (
                     f"{instrucciones_adicionales}\n"
                     + base_custom_prompt_template.template
                 )
                 final_prompt_template_rag = PromptTemplate(prompt_template_str)

        # --- Crear Motor de Consulta RAG con el Prompt Final ---
        query_engine_rag = index.as_query_engine(
            similarity_top_k=1, # Obtener solo la interpretación más relevante
            text_qa_template=final_prompt_template_rag
        )

        # --- Cargar Títulos Objetivo ---
        # Use absolute path to avoid potential issues with relative paths during execution
        # Corrected path to include the 'data' subdirectory
        titles_file_abs_path = "/Users/apple/astro_interpretador_rag/data/Títulos Numerados tropico.md"
        target_titles_set = load_target_titles(titles_file_abs_path)
        if target_titles_set is None: # Comprobar si hubo error al cargar
             print("🔴 Error al cargar títulos objetivo. Abortando.")
             sys.exit(1)
        if not target_titles_set:
             print("🔴 No se cargaron títulos objetivo (archivo vacío o sin títulos válidos?). Abortando.")
             sys.exit(1)

        # --- Evaluar Aspectos Complejos ---
        if file_type == ".json" and raw_json_data and planets_in_houses:
            complex_events = evaluate_complex_aspects(eventos, planets_in_houses, raw_json_data)
            # Agregar eventos complejos a la lista principal
            eventos.extend(complex_events)
            print(f"📊 Total de eventos (incluyendo aspectos complejos): {len(eventos)}")

        # --- Filtrar Eventos Basados en Títulos Objetivo ---
        eventos_filtrados = []
        print("\n🔍 Filtrando eventos según títulos objetivo...")
        consultas_generadas_para_eventos = {} # Guardar consulta para reutilizar

        # --- TODO: Implementar Lógica Condicional Compleja ---
        # Los siguientes comentarios detallan la lógica necesaria para evaluar títulos
        # marcados como "REQUIERE LÓGICA ADICIONAL" en validation_report_corrected.md.
        # Esta lógica debería ejecutarse aquí o en una función dedicada,
        # potencialmente añadiendo eventos/flags específicos a 'eventos_filtrados'
        # o modificando las consultas generadas si se cumplen las condiciones complejas.

        # TODO: Implement logic for 'Aspecto Sol conjunción, cuadratura u oposición a Júpiter y Saturno o Plutón están en casa 1, 4, 7 o 10.'
        # Conditions: 1. Check aspect: Sol-Jupiter (conj/sq/opp) exists. 2. Check house: Saturn in 1/4/7/10 OR Pluto in 1/4/7/10.
        # Data needed: 'eventos', 'planets_in_houses'. Action: Add specific query/flag if met.

        # TODO: Implement logic for 'Aspecto Sol conjunción, cuadratura u oposición a Júpiter y Saturno o Plutón están en conjunción al Sol, la Luna, Mercurio, Venus o Marte.'
        # Conditions: 1. Check aspect: Sol-Jupiter (conj/sq/opp) exists. 2. Check aspect: Saturn conjunct (Sol/Moon/Merc/Venus/Mars) OR Pluto conjunct (Sol/Moon/Merc/Venus/Mars) exists.
        # Data needed: 'eventos'. Action: Add specific query/flag if met.

        # TODO: Implement logic for 'Aspecto Sol conjunción, cuadratura u oposición a Júpiter y Saturno o Plutón están en cuadratura al Sol, la Luna, Mercurio, Venus o Marte.'
        # Conditions: 1. Check aspect: Sol-Jupiter (conj/sq/opp) exists. 2. Check aspect: Saturn square (Sol/Moon/Merc/Venus/Mars) OR Pluto square (Sol/Moon/Merc/Venus/Mars) exists.
        # Data needed: 'eventos'. Action: Add specific query/flag if met.

        # TODO: Implement logic for 'Aspecto Sol conjunción, cuadratura u oposición a Júpiter y hay conjunción, cuadratura u oposición entre Saturno y Plutón.'
        # Conditions: 1. Check aspect: Sol-Jupiter (conj/sq/opp) exists. 2. Check aspect: Saturn-Pluto (conj/sq/opp) exists.
        # Data needed: 'eventos'. Action: Add specific query/flag if met.

        # TODO: Implement logic for 'Aspecto Luna conjunción, cuadratura u oposición a Júpiter y Saturno o Plutón están en casa 1, 4, 7 o 10.'
        # Conditions: 1. Check aspect: Moon-Jupiter (conj/sq/opp) exists. 2. Check house: Saturn in 1/4/7/10 OR Pluto in 1/4/7/10.
        # Data needed: 'eventos', 'planets_in_houses'. Action: Add specific query/flag if met.

        # TODO: Implement logic for 'Aspecto Luna conjunción, cuadratura u oposición a Júpiter y Saturno o Plutón están en conjunción al Sol, la Luna, Mercurio, Venus o Marte.'
        # Conditions: 1. Check aspect: Moon-Jupiter (conj/sq/opp) exists. 2. Check aspect: Saturn conjunct (Sol/Moon/Merc/Venus/Mars) OR Pluto conjunct (Sol/Moon/Merc/Venus/Mars) exists.
        # Data needed: 'eventos'. Action: Add specific query/flag if met.

        # TODO: Implement logic for 'Aspecto Luna conjunción, cuadratura u oposición a Júpiter y Saturno o Plutón están en cuadratura al Sol, la Luna, Mercurio, Venus o Marte.'
        # Conditions: 1. Check aspect: Moon-Jupiter (conj/sq/opp) exists. 2. Check aspect: Saturn square (Sol/Moon/Merc/Venus/Mars) OR Pluto square (Sol/Moon/Merc/Venus/Mars) exists.
        # Data needed: 'eventos'. Action: Add specific query/flag if met.

        # TODO: Implement logic for 'Aspecto Luna conjunción, cuadratura u oposición a Júpiter y hay conjunción, cuadratura u oposición entre Saturno y Plutón.'
        # Conditions: 1. Check aspect: Moon-Jupiter (conj/sq/opp) exists. 2. Check aspect: Saturn-Pluto (conj/sq/opp) exists.
        # Data needed: 'eventos'. Action: Add specific query/flag if met.

        # TODO: Implement logic for 'Aspecto Luna en conjunción, cuadratura u oposición a Urano y Saturno está en casa 1, 4, 7 o 10.'
        # Conditions: 1. Check aspect: Moon-Uranus (conj/sq/opp) exists. 2. Check house: Saturn in 1/4/7/10.
        # Data needed: 'eventos', 'planets_in_houses'. Action: Add specific query/flag if met.

        # TODO: Implement logic for 'Aspecto Luna en conjunción, cuadratura u oposición a Urano y Saturno está en conjunción al Sol, la Luna, Mercurio, Venus o Marte.'
        # Conditions: 1. Check aspect: Moon-Uranus (conj/sq/opp) exists. 2. Check aspect: Saturn conjunct (Sol/Moon/Merc/Venus/Mars) exists.
        # Data needed: 'eventos'. Action: Add specific query/flag if met.

        # TODO: Implement logic for 'Aspecto Luna en conjunción, cuadratura u oposición a Urano y Saturno está en cuadratura al Sol, la Luna, Mercurio, Venus o Marte.'
        # Conditions: 1. Check aspect: Moon-Uranus (conj/sq/opp) exists. 2. Check aspect: Saturn square (Sol/Moon/Merc/Venus/Mars) exists.
        # Data needed: 'eventos'. Action: Add specific query/flag if met.

        # TODO: Implement logic for 'Ascendente en Tauro y Marte está en casa 1, 4, 7 o 10.'
        # Conditions: 1. Check Asc sign: Ascendant is Taurus. 2. Check house: Mars in 1/4/7/10.
        # Data needed: 'raw_json_data', 'planets_in_houses'. Action: Add specific query/flag if met.

        # TODO: Implement logic for 'Ascendente en Tauro y Marte está en conjunción al Sol o la Luna.'
        # Conditions: 1. Check Asc sign: Ascendant is Taurus. 2. Check aspect: Mars conjunct Sol OR Mars conjunct Moon exists.
        # Data needed: 'raw_json_data', 'eventos'. Action: Add specific query/flag if met.

        # TODO: Implement logic for 'Luna en el ascendente'
        # Conditions: Check if Moon is in House 1 (Casa 1).
        # Data needed: 'planets_in_houses["Moon"] == 1'. Action: Add specific query/flag if met.

        # TODO: Implement logic for 'Mercurio en el ascendente'
        # Conditions: Check if Mercury is in House 1 (Casa 1).
        # Data needed: 'planets_in_houses["Mercury"] == 1'. Action: Add specific query/flag if met.

        # TODO: Implement logic for 'Venus en el ascendente'
        # Conditions: Check if Venus is in House 1 (Casa 1).
        # Data needed: 'planets_in_houses["Venus"] == 1'. Action: Add specific query/flag if met.

        # TODO: Implement logic for 'Marte en el ascendente'
        # Conditions: Check if Mars is in House 1 (Casa 1).
        # Data needed: 'planets_in_houses["Mars"] == 1'. Action: Add specific query/flag if met.

        # TODO: Implement logic for 'Júpiter en el ascendente'
        # Conditions: Check if Jupiter is in House 1 (Casa 1).
        # Data needed: 'planets_in_houses["Jupiter"] == 1'. Action: Add specific query/flag if met.

        # TODO: Implement logic for 'Saturno en el ascendente'
        # Conditions: Check if Saturn is in House 1 (Casa 1).
        # Data needed: 'planets_in_houses["Saturn"] == 1'. Action: Add specific query/flag if met.

        # TODO: Implement logic for 'Urano en el ascendente'
        # Conditions: Check if Uranus is in House 1 (Casa 1).
        # Data needed: 'planets_in_houses["Uranus"] == 1'. Action: Add specific query/flag if met.

        # TODO: Implement logic for 'Neptuno en el ascendente'
        # Conditions: Check if Neptune is in House 1 (Casa 1).
        # Data needed: 'planets_in_houses["Neptune"] == 1'. Action: Add specific query/flag if met.

        # TODO: Implement logic for 'Plutón en el ascendente'
        # Conditions: Check if Pluto is in House 1 (Casa 1).
        # Data needed: 'planets_in_houses["Pluto"] == 1'. Action: Add specific query/flag if met.

        # TODO: Implement logic for 'Aspecto Mercurio en conjunción, cuadratura u oposición a Urano y Urano está en casa 1, 4, 7 o 10.'
        # Conditions: 1. Check aspect: Mercury-Uranus (conj/sq/opp) exists. 2. Check house: Uranus in 1/4/7/10.
        # Data needed: 'eventos', 'planets_in_houses'. Action: Add specific query/flag if met.

        # TODO: Implement logic for 'Aspecto Mercurio en conjunción, cuadratura u oposición a Urano y Urano está en conjunción al Sol o la Luna.'
        # Conditions: 1. Check aspect: Mercury-Uranus (conj/sq/opp) exists. 2. Check aspect: Uranus conjunct Sol OR Uranus conjunct Moon exists.
        # Data needed: 'eventos'. Action: Add specific query/flag if met.

        # TODO: Implement logic for 'Venus en la casa 4: usar solo si no se dan las siguientes condiciones: Saturno en casa 4 o Plutón en casa 4 o Venus conjunción Saturno o Venus conjunción Plutón'
        # Conditions: 1. Check primary: Venus in house 4. 2. Check exclusions: a) Saturn NOT in house 4. b) Pluto NOT in house 4. c) Venus-Saturn conjunction NOT exist. d) Venus-Pluto conjunction NOT exist.
        # Data needed: 'planets_in_houses', 'eventos'. Action: Add specific query/flag if primary is true AND all exclusions are true.

        # TODO: Implement logic for 'Aspecto: Saturno está en casa 1, 4, 7 o 10 y Urano está en casa 1, 4, 7 o 10.'
        # Conditions: 1. Check house: Saturn in 1/4/7/10. 2. Check house: Uranus in 1/4/7/10.
        # Data needed: 'planets_in_houses'. Action: Add specific query/flag if met.

        # TODO: Implement logic for 'Aspecto: Saturno está en casa 1, 4, 7 o 10 y Urano está en conjunción al Sol, la Luna, Mercurio, Venus o Marte.'
        # Conditions: 1. Check house: Saturn in 1/4/7/10. 2. Check aspect: Uranus conjunct (Sol/Moon/Merc/Venus/Mars) exists.
        # Data needed: 'planets_in_houses', 'eventos'. Action: Add specific query/flag if met.

        # TODO: Implement logic for 'Aspecto: Saturno está en casa 1, 4, 7 o 10 y hay conjunción, cuadratura u oposición entre Saturno y Urano.'
        # Conditions: 1. Check house: Saturn in 1/4/7/10. 2. Check aspect: Saturn-Uranus (conj/sq/opp) exists.
        # Data needed: 'planets_in_houses', 'eventos'. Action: Add specific query/flag if met.

        # TODO: Implement logic for 'Aspecto: Saturno está en conjunción al Sol, la Luna, Mercurio, Venus o Marte y Urano está en casa 1, 4, 7 o 10.'
        # Conditions: 1. Check aspect: Saturn conjunct (Sol/Moon/Merc/Venus/Mars) exists. 2. Check house: Uranus in 1/4/7/10.
        # Data needed: 'eventos', 'planets_in_houses'. Action: Add specific query/flag if met.

        # TODO: Implement logic for 'Aspecto: Saturno está en conjunción al Sol, la Luna, Mercurio, Venus o Marte y Urano está en conjunción al Sol, la Luna, Mercurio, Venus o Marte.'
        # Conditions: 1. Check aspect: Saturn conjunct (Sol/Moon/Merc/Venus/Mars) exists. 2. Check aspect: Uranus conjunct (Sol/Moon/Merc/Venus/Mars) exists.
        # Data needed: 'eventos'. Action: Add specific query/flag if met.

        # TODO: Implement logic for 'Aspecto: Saturno está en conjunción al Sol, la Luna, Mercurio, Venus o Marte y hay conjunción, cuadratura u oposición entre Saturno y Urano.'
        # Conditions: 1. Check aspect: Saturn conjunct (Sol/Moon/Merc/Venus/Mars) exists. 2. Check aspect: Saturn-Uranus (conj/sq/opp) exists.
        # Data needed: 'eventos'. Action: Add specific query/flag if met.

        # TODO: Implement logic for 'POLARIDAD PLUTONIANA CUANDO PLUTÓN ESTÁ CON EL SOL O EN CASA 1'
        # Conditions: 1. Check aspect: Pluto conjunct Sol exists OR 2. Check house: Pluto in house 1.
        # Data needed: 'eventos', 'planets_in_houses'. Action: Add specific query/flag if met.

        # --- Existing Filtering Loop ---
        for evento in eventos:
            # Manejar eventos complejos de manera especial
            if evento.get("tipo") == "AspectoComplejo":
                titulo_especifico = evento.get("titulo_especifico", "").lower()
                # Para aspectos complejos, usar el título específico como consulta
                consulta_potencial = titulo_especifico
                consultas_generadas_para_eventos[consulta_potencial] = evento
                # Siempre incluir aspectos complejos ya que fueron detectados específicamente
                eventos_filtrados.append(evento)
                print(f"✓ Incluido aspecto complejo: {titulo_especifico}")
            else:
                consulta_potencial = generar_consulta_estandarizada(evento)
                consultas_generadas_para_eventos[consulta_potencial] = evento # Usar consulta como clave
                # Consulta ya está en minúsculas por la función modificada
                consulta_normalizada = consulta_potencial # Ya está normalizada a minúsculas

                # Comprobar si la consulta normalizada (lowercase) está en los títulos objetivo (lowercase)
                if consulta_normalizada in target_titles_set:
                    eventos_filtrados.append(evento)
                # else:
                    # print(f"DEBUG [Filter]: Skipped event for '{consulta_normalizada}'") # Uncomment for debugging

        print(f"📊 Eventos filtrados para interpretar: {len(eventos_filtrados)} (de {len(eventos)} iniciales)")

        if not eventos_filtrados:
            print("🔴 No hay eventos que coincidan con los títulos objetivo. No se generará informe.")
            sys.exit(1)

        # --- Procesamiento y Guardado ---
        if file_type == ".csv":
            # --- Lógica CSV Adaptada para Filtrar (Opcional) ---
            # Si se desea que el CSV también respete los títulos, adaptar aquí.
            # Por simplicidad, mantenemos la lógica original que usa TODOS los eventos.
            # Si se quiere filtrar, reemplazar 'eventos' con 'eventos_filtrados' en el bucle.
            resultados_csv = []
            print("\n✨ Iniciando interpretaciones para CSV (Usando todos los eventos originales)...")
            for i, evento in enumerate(eventos): # Usando eventos originales para CSV
                consulta = generar_consulta_estandarizada(evento)
                print(f"🔍 Consultando ({i+1}/{len(eventos)}): {consulta}")
                try:
                    respuesta = query_engine_rag.query(consulta)
                    interpretacion = respuesta.response.strip() if respuesta.response else "N/A"
                    fuente = respuesta.source_nodes[0].get_content().strip() if respuesta.source_nodes else "N/A"
                    resultados_csv.append({
                        "consulta_generada": consulta,
                        "interpretacion": interpretacion,
                        "fuente_interpretacion": fuente,
                        "evento_original": evento
                    })
                except Exception as e:
                     print(f"⚠️ Error al consultar para '{consulta}': {e}")
                     resultados_csv.append({
                        "consulta_generada": consulta,
                        "interpretacion": f"Error: {e}",
                        "fuente_interpretacion": "N/A",
                        "evento_original": evento
                    })
            output_filename_csv = f"{input_path_obj.stem}_con_interpretacion_{llm_name}.csv"
            output_path_csv = input_path_obj.parent / output_filename_csv
            df_resultados = pd.DataFrame(resultados_csv)
            df_resultados.to_csv(output_path_csv, index=False, encoding='utf-8')
            print(f"\n✅ Archivo CSV generado con éxito: {output_path_csv}")

        elif file_type == ".json":
            report_title = f"Informe Astrológico para {chart_name}"
            interpretaciones_individuales_con_header = []
            report_content_individual = f"{report_title}\n{'=' * len(report_title)}\n\n"

            print("\n✨ Obteniendo interpretaciones individuales...")
            # Ordenar eventos FILTRADOS para un flujo más lógico
            eventos_filtrados.sort(key=lambda x: (
                0 if x['tipo'] == 'PlanetaEnSigno' else
                1 if x['tipo'] == 'PlanetaEnCasa' else
                2 if x['tipo'] == 'CasaEnSigno' else
                3 if x['tipo'] == 'Aspecto' else
                4 if x['tipo'] == 'PlanetaRetrogrado' else 5 # Asumiendo que estos tipos existen
            ))

            # DEBUG: Crear archivo para logging del RAG
            debug_rag_file = "/Users/apple/debug_rag_procesamiento.txt"
            with open(debug_rag_file, 'w', encoding='utf-8') as f:
                f.write("🔍 DEBUG PROCESAMIENTO RAG\n")
                f.write(f"Fecha: {__import__('datetime').datetime.now().isoformat()}\n\n")
                f.write(f"Total eventos a procesar: {len(eventos_filtrados)}\n\n")

            for i, evento in enumerate(eventos_filtrados): # <--- USAR EVENTOS FILTRADOS
                # Generar la consulta para este evento
                consulta = generar_consulta_estandarizada(evento)

                print(f"🔍 Consultando RAG ({i+1}/{len(eventos_filtrados)}): {consulta}")

                # DEBUG: Log de la consulta al RAG
                with open(debug_rag_file, 'a', encoding='utf-8') as f:
                    f.write(f"--- Consulta {i+1} ---\n")
                    f.write(f"Consulta generada: {consulta}\n")
                    f.write(f"Tipo evento: {evento.get('tipo', 'N/A')}\n")
                    f.write(f"Evento completo: {evento}\n\n")

                # Generar Header basado en el evento actual, no solo la consulta base
                header = f"### {consulta}" # Default header
                tipo = evento.get("tipo")
                planeta_orig = evento.get('planeta')
                planeta_es = translate(planeta_orig, PLANET_TRANSLATIONS_ES)

                if tipo == "PlanetaEnSigno":
                    signo_es = translate(evento.get('signo'), SIGN_TRANSLATIONS_ES)
                    grados = evento.get('grados')
                    grados_formateados = format_degrees(grados)
                    if grados_formateados:
                        header = f"### Tu {planeta_es} se encuentra a {grados_formateados} de {signo_es}"
                    else:
                        header = f"### Tu {planeta_es} en {signo_es}"
                elif tipo == "PlanetaEnCasa":
                     header = f"### Tu {planeta_es} en Casa {evento.get('casa')}" # Encabezado para Planeta en Casa
                elif tipo == "PlanetaRetrogrado":
                     header = f"### Tu {planeta_es} está Retrógrado"
                elif tipo == "Aspecto":
                    p1_es = translate(evento.get('planeta1'), PLANET_TRANSLATIONS_ES)
                    asp_es = translate(evento.get('aspecto'), ASPECT_TRANSLATIONS_ES)
                    p2_es = translate(evento.get('planeta2'), PLANET_TRANSLATIONS_ES)
                    header = f"### Aspecto: Tu {p1_es} en {asp_es} con tu {p2_es}"
                elif tipo == "CasaEnSigno":
                    signo_es = translate(evento.get('signo'), SIGN_TRANSLATIONS_ES)
                    header = f"### La Cúspide de tu Casa {evento.get('casa')} está en {signo_es}"
                elif tipo == "AspectoComplejo":
                    # Para aspectos complejos, usar el título específico como header
                    titulo_especifico = evento.get("titulo_especifico", "")
                    descripcion = evento.get("descripcion", "")
                    header = f"### {titulo_especifico}"
                    # Usar la descripción como consulta para el RAG
                    consulta = descripcion.lower()

                try:
                    respuesta = query_engine_rag.query(consulta)
                    interpretacion = respuesta.response.strip() if respuesta.response else "No se encontró interpretación específica."

                    # DEBUG: Log de la respuesta del RAG
                    with open(debug_rag_file, 'a', encoding='utf-8') as f:
                        f.write(f"Respuesta RAG: {interpretacion[:500]}...\n")  # Primeros 500 caracteres
                        f.write(f"Longitud respuesta: {len(interpretacion)} caracteres\n")
                        if respuesta.source_nodes:
                            f.write(f"Fuente utilizada: {respuesta.source_nodes[0].get_content()[:200]}...\n")
                        f.write(f"--- Fin Consulta {i+1} ---\n\n")

                except Exception as e:
                     print(f"⚠️ Error al consultar RAG para '{consulta}': {e}")
                     interpretacion = f"Error al obtener interpretación: {e}"

                     # DEBUG: Log del error
                     with open(debug_rag_file, 'a', encoding='utf-8') as f:
                         f.write(f"ERROR: {str(e)}\n")
                         f.write(f"--- Fin Consulta {i+1} (ERROR) ---\n\n")

                report_content_individual += header + "\n" + interpretacion + "\n\n"
                interpretaciones_individuales_con_header.append(f"{header}\n{interpretacion}")

            # Guardar el informe individual en formato TXT
            output_filename_individual_txt = f"{input_path_obj.stem}_interpretada_individual_{llm_name}.txt"
            output_path_individual_txt = input_path_obj.parent / output_filename_individual_txt
            try:
                with open(output_path_individual_txt, 'w', encoding='utf-8') as f:
                    f.write(report_content_individual)
                print(f"\n✅ Informe Individual TXT generado con éxito: {output_path_individual_txt}")
            except Exception as e:
                print(f"❌ Error al guardar el informe TXT individual: {e}")
                
            # Generar y guardar el informe individual en formato JSON
            try:
                # Crear estructura JSON para interpretaciones individuales
                interpretaciones_json = []
                for i, evento in enumerate(eventos_filtrados):
                    # Obtener la interpretación correspondiente
                    header = None
                    interpretacion = None
                    if i < len(interpretaciones_individuales_con_header):
                        partes = interpretaciones_individuales_con_header[i].split('\n', 1)
                        if len(partes) == 2:
                            header = partes[0].replace('### ', '')
                            interpretacion = partes[1].strip()
                    
                    if header and interpretacion:
                        # Extraer información adicional del evento
                        tipo = evento.get("tipo", "")
                        item_json = {
                            "titulo": header,
                            "tipo": tipo,
                            "interpretacion": interpretacion
                        }
                        
                        # Añadir detalles específicos según el tipo de evento
                        if tipo == "PlanetaEnSigno":
                            planeta_orig = evento.get('planeta', '')
                            planeta_es = translate(planeta_orig, PLANET_TRANSLATIONS_ES)
                            signo_es = translate(evento.get('signo', ''), SIGN_TRANSLATIONS_ES)
                            grados = evento.get('grados')
                            grados_formateados = format_degrees(grados) if grados else ""
                            
                            item_json["planeta"] = planeta_es
                            item_json["signo"] = signo_es
                            if grados_formateados:
                                item_json["grados"] = grados_formateados
                                
                        elif tipo == "PlanetaEnCasa":
                            planeta_orig = evento.get('planeta', '')
                            planeta_es = translate(planeta_orig, PLANET_TRANSLATIONS_ES)
                            casa = evento.get('casa', '')
                            
                            item_json["planeta"] = planeta_es
                            item_json["casa"] = casa
                            
                        elif tipo == "PlanetaRetrogrado":
                            planeta_orig = evento.get('planeta', '')
                            planeta_es = translate(planeta_orig, PLANET_TRANSLATIONS_ES)
                            
                            item_json["planeta"] = planeta_es
                            
                        elif tipo == "Aspecto":
                            p1_orig = evento.get('planeta1', '')
                            p2_orig = evento.get('planeta2', '')
                            asp = evento.get('aspecto', '')
                            
                            p1_es = translate(p1_orig, PLANET_TRANSLATIONS_ES)
                            p2_es = translate(p2_orig, PLANET_TRANSLATIONS_ES)
                            asp_es = translate(asp, ASPECT_TRANSLATIONS_ES)
                            
                            item_json["planeta1"] = p1_es
                            item_json["planeta2"] = p2_es
                            item_json["aspecto"] = asp_es
                            
                        elif tipo == "CasaEnSigno":
                            casa = evento.get('casa', '')
                            signo_es = translate(evento.get('signo', ''), SIGN_TRANSLATIONS_ES)
                            
                            item_json["casa"] = casa
                            item_json["signo"] = signo_es
                        
                        interpretaciones_json.append(item_json)
                
                # Crear estructura JSON completa
                informe_json = {
                    "titulo": report_title,
                    "tipo": "individual",
                    "llm": llm_name,
                    "interpretaciones": interpretaciones_json
                }
                
                # Guardar en archivo JSON
                output_filename_individual_json = f"{input_path_obj.stem}_interpretada_individual_{llm_name}.json"
                output_path_individual_json = input_path_obj.parent / output_filename_individual_json
                
                with open(output_path_individual_json, 'w', encoding='utf-8') as f:
                    json.dump(informe_json, f, ensure_ascii=False, indent=2)
                    
                print(f"✅ Informe Individual JSON generado con éxito: {output_path_individual_json}")
            except Exception as e:
                print(f"❌ Error al guardar el informe JSON individual: {e}")

            # Preparar y ejecutar la re-escritura narrativa
            if interpretaciones_individuales_con_header:
                print(f"\n✍️ Iniciando re-escritura narrativa con {llm_name}...")
                try:
                    if llm_choice == "1":
                        llm_rewriter = OpenAI(api_key=openai_key, temperature=0.7, model="gpt-4-turbo-preview")
                    else:
                        llm_rewriter = OpenAI(
                            api_key=xai_key, 
                            temperature=0.7, 
                            model="grok-3",
                            base_url="https://api.x.ai/v1"
                        )
                except Exception as e:
                    print(f"❌ Error al instanciar gpt-4-turbo-preview: {e}. No se puede continuar con la re-escritura.")
                    sys.exit(1)

                interpretaciones_combinadas = "\n\n".join(interpretaciones_individuales_con_header)
                instrucciones_adicionales_reescritura = f"{genero_instruccion}\n{persona_instruccion}".strip()

                # Proposed new prompt string (replace the old one)
                rewrite_prompt_str = (
                    f"{instrucciones_adicionales_reescritura}\n" # Keep gender/persona instructions
                    f"Eres un astrólogo experto y un excelente escritor. Tu tarea es tomar las siguientes interpretaciones astrológicas individuales (separadas por '###') de una CARTA NATAL y re-escribirlas como un informe narrativo unificado, fluido y detallado, dirigido directamente a la persona (usando 'Tú').\n"
                    "**REGLAS CRÍTICAS:**\n"
                    "1.  **INCLUYE TODO:** Debes incorporar la información específica de CADA interpretación proporcionada. Esto incluye OBLIGATORIAMENTE: Planetas en Signo (con grados si están), Planetas en Casa, Cúspides de Casa en Signo, Aspectos (mencionando el tipo: Conjunción, Oposición, Cuadratura, Trígono, Sextil), Planetas Retrógrados, y otros puntos como Nodos, Lilith, Quirón, Parte de la Fortuna, Vertex.\n"
                    "2.  **MANTÉN DETALLE:** NO resumas excesivamente. Preserva los matices y detalles específicos de cada interpretación individual mientras los tejes en la narrativa.\n"
                    "3.  **ENFOQUE NATAL:** Todas las interpretaciones se refieren a la CARTA NATAL base. NO las describas como 'tránsitos' a menos que el texto original lo indique explícitamente.\n"
                    "4.  **FLUJO COHERENTE:** Conecta las ideas de forma lógica. Puedes agrupar temas (ej: identidad central, relaciones, carrera, desafíos) pero asegúrate de que todas las piezas individuales estén presentes en la narrativa final.\n"
                    "5.  **ESTILO:** Mantén un tono personal y empático. No repitas el nombre de la persona en el cuerpo del texto. Organiza en párrafos claros.\n"
                    "6.  **IDIOMA:** Responde EXCLUSIVAMENTE en idioma español.\n\n"
                    "Interpretaciones individuales NATALES a re-escribir:\n"
                    "--------------------------------------------------\n"
                    f"{interpretaciones_combinadas}\n"
                    "--------------------------------------------------\n"
                    "Informe Narrativo Detallado:"
                )

                try:
                    print(f"🔄 Enviando solicitud de re-escritura al LLM ({llm_name})...")
                    if llm_choice == "1":
                        narrative_response = llm_rewriter.complete(rewrite_prompt_str)
                        final_narrative_content = narrative_response.text.strip()
                    else:
                        # Usar el cliente directo de Grok para la reescritura
                        response = grok_client.chat.completions.create(
                            model="grok-3",
                            messages=[
                                {"role": "system", "content": "Eres un astrólogo experto y un excelente escritor."},
                                {"role": "user", "content": rewrite_prompt_str}
                            ],
                            temperature=0.7
                        )
                        final_narrative_content = response.choices[0].message.content.strip()
                    print("✅ Respuesta de re-escritura recibida.")
                except Exception as e:
                    print(f"❌ Error durante la re-escritura narrativa con {llm_name}: {e}")
                    final_narrative_content = f"Error al generar el informe narrativo: {e}\n\n(No se pudo generar la versión narrativa.)"

                report_content_narrative = f"{report_title}\n{'=' * len(report_title)}\n\n{final_narrative_content}"
                output_filename_narrative_txt = f"{input_path_obj.stem}_interpretada_narrativa_{llm_name}.txt"
                output_path_narrative_txt = input_path_obj.parent / output_filename_narrative_txt
                try:
                    with open(output_path_narrative_txt, 'w', encoding='utf-8') as f:
                        f.write(report_content_narrative)
                    print(f"\n✅ Informe Narrativo TXT generado con éxito: {output_path_narrative_txt}")
                    
                    # Generar y guardar el informe narrativo en formato JSON
                    informe_narrativo_json = {
                        "titulo": report_title,
                        "tipo": "narrativa",
                        "llm": llm_name,
                        "contenido": final_narrative_content
                    }
                    
                    output_filename_narrative_json = f"{input_path_obj.stem}_interpretada_narrativa_{llm_name}.json"
                    output_path_narrative_json = input_path_obj.parent / output_filename_narrative_json
                    
                    with open(output_path_narrative_json, 'w', encoding='utf-8') as f:
                        json.dump(informe_narrativo_json, f, ensure_ascii=False, indent=2)
                        
                    print(f"✅ Informe Narrativo JSON generado con éxito: {output_path_narrative_json}")
                except Exception as e:
                    print(f"❌ Error al guardar los informes narrativos: {e}")
            else:
                 print("🔴 No se obtuvieron interpretaciones individuales para intentar la re-escritura.")
    else:
        print("🔴 No se pudieron procesar los eventos.")
