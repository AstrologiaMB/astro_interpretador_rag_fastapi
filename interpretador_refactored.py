"""
InterpretadorRAG Refactorizado - Versión API sin interactividad
- LLM fijo: OpenAI
- Datos directos del microservicio (no archivos)
- Dependencias actualizadas y compatibles
"""

import os
import json
import re
import time
import asyncio
import unicodedata
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, List, Any, Optional
from prompts import get_rag_extraction_prompt_str, get_tropical_narrative_prompt_str, get_draconian_narrative_prompt_str

# Usar versiones actualizadas de llama-index
try:
    from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
    from llama_index.llms.anthropic import Anthropic
    from llama_index.embeddings.openai import OpenAIEmbedding
    from llama_index.core.prompts import PromptTemplate
    LLAMA_INDEX_NEW = True
except ImportError:
    # Fallback a versiones anteriores
    from llama_index import SimpleDirectoryReader, GPTVectorStoreIndex as VectorStoreIndex, ServiceContext
    from llama_index.llms import OpenAI, Anthropic
    from llama_index.embeddings import OpenAIEmbedding
    from llama_index.prompts import PromptTemplate
    LLAMA_INDEX_NEW = False

class InterpretadorRAG:
    def __init__(self):
        """Inicializar el interpretador RAG"""
        # Cargar variables de entorno
        load_dotenv()
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        
        if not self.openai_key:
            raise ValueError("OPENAI_API_KEY no encontrada en variables de entorno")
            
        if not self.anthropic_key:
            # Fallback opcional o error, para esta migración asumimos que es necesaria
            print("⚠️ ANTHROPIC_API_KEY no encontrada. El stack de Claude fallará si se intenta usar.")
        
        # Feature flag para RAGs separados (False = sistema actual, True = RAGs separados)
        self.USE_SEPARATE_ENGINES = True
        
        # Configurar LLM y embeddings
        self._setup_llm_and_embeddings()
        
        # Cargar e indexar documentos de interpretaciones
        self._load_and_index_documents()
        
        # Cargar títulos objetivo
        self._load_target_titles()
        
        # Configurar prompt base
        self._setup_base_prompt()
        
        print("✅ InterpretadorRAG refactorizado inicializado correctamente")
        print(f"🔧 Feature Flag - RAGs Separados: {'ACTIVADO' if self.USE_SEPARATE_ENGINES else 'DESACTIVADO (sistema actual)'}")
    
    def _setup_llm_and_embeddings(self):
        """Configurar LLM y embeddings: Stack 100% Anthropic (Haiku + Sonnet)"""
        # Modelos
        MODEL_RAG = "claude-3-haiku-20240307"    # RAG rápido y eficiente
        MODEL_WRITER = "claude-3-5-sonnet-latest" # Redacción humana y cálida (versión más reciente)
        
        if LLAMA_INDEX_NEW:
            # Usar Settings globales (nueva API)
            # 1. Configurar RAG con Claude Haiku
            Settings.llm = Anthropic(api_key=self.anthropic_key, temperature=0.0, model=MODEL_RAG)
            
            # 2. Embeddings se mantienen con OpenAI (para no re-indexar vectores existentes)
            Settings.embed_model = OpenAIEmbedding(api_key=self.openai_key)
            self.service_context_rag = None
            
            # 3. Configurar Escritor con Claude Sonnet
            self.llm_rewriter = Anthropic(api_key=self.anthropic_key, temperature=0.7, model=MODEL_WRITER, max_tokens=4096)
        else:
            # Usar ServiceContext (versión anterior)
            # 1. Configurar RAG con Claude Haiku
            self.llm_rag = Anthropic(api_key=self.anthropic_key, temperature=0.0, model=MODEL_RAG)
            
            # 2. Configurar Escritor con Claude Sonnet
            self.llm_rewriter = Anthropic(api_key=self.anthropic_key, temperature=0.7, model=MODEL_WRITER, max_tokens=4096)
            
            # 3. Embeddings OpenAI
            self.embed_model = OpenAIEmbedding(api_key=self.openai_key)
            self.service_context_rag = ServiceContext.from_defaults(llm=self.llm_rag, embed_model=self.embed_model)
    
    def _load_and_index_documents(self):
        """Cargar y indexar los archivos de interpretaciones (tropical y draconic)"""
        try:
            # Paths to both tropical and draconic content (Railway-compatible local paths)
            tropical_dir = Path("data")
            draco_dir = Path("data/draco")

            # Load tropical files
            tropical_files = sorted([f for f in tropical_dir.glob("[0-9]*.md")])
            # print(f"📄 Cargando {len(tropical_files)} archivos tropicales")

            # Load draconic files
            draco_files = sorted([f for f in draco_dir.glob("[0-9]*.md")])
            # print(f"📄 Cargando {len(draco_files)} archivos dracónicos")

            if not tropical_files and not draco_files:
                raise FileNotFoundError("No se encontraron archivos de interpretaciones en ninguna ubicación")

            # print(f"📄 Total archivos encontrados: tropical: {len(tropical_files)}, draconic: {len(draco_files)}")

            # Crear todos los engines (mixto + separados)
            self._create_all_engines(tropical_files, draco_files)

        except Exception as e:
            raise Exception(f"Error al cargar o indexar los archivos Markdown de interpretaciones: {e}")
    
    def _create_all_engines(self, tropical_files: List[Path], draco_files: List[Path]):
        """Crear todos los engines RAG: mixto (actual) + separados (nuevo)"""
        try:
            # print("🔧 Creando engines RAG...")
            
            # 1. Crear índice mixto (sistema actual) - SIEMPRE se crea para compatibilidad
            all_files = tropical_files + draco_files
            if all_files:
                documents_mixed = SimpleDirectoryReader(input_files=all_files).load_data()
                if LLAMA_INDEX_NEW:
                    self.index = VectorStoreIndex.from_documents(documents_mixed)
                else:
                    self.index = VectorStoreIndex.from_documents(documents_mixed, service_context=self.service_context_rag)
                # print(f"✅ Índice RAG MIXTO creado: {len(documents_mixed)} documentos")
            else:
                raise ValueError("No hay archivos para crear el índice mixto")
            
            # 2. Crear índices separados (solo si USE_SEPARATE_ENGINES está activado o para preparación)
            # Los creamos siempre para estar listos, pero solo los usamos si el flag está activado
            
            # Índice tropical separado
            if tropical_files:
                documents_tropical = SimpleDirectoryReader(input_files=tropical_files).load_data()
                if LLAMA_INDEX_NEW:
                    self.tropical_index = VectorStoreIndex.from_documents(documents_tropical)
                else:
                    self.tropical_index = VectorStoreIndex.from_documents(documents_tropical, service_context=self.service_context_rag)
                # print(f"✅ Índice RAG TROPICAL creado: {len(documents_tropical)} documentos")
            else:
                self.tropical_index = None
                # print("⚠️ No se encontraron archivos tropicales, índice tropical = None")
            
            # Índice dracónico separado
            if draco_files:
                documents_draco = SimpleDirectoryReader(input_files=draco_files).load_data()
                if LLAMA_INDEX_NEW:
                    self.draco_index = VectorStoreIndex.from_documents(documents_draco)
                else:
                    self.draco_index = VectorStoreIndex.from_documents(documents_draco, service_context=self.service_context_rag)
                # print(f"✅ Índice RAG DRACÓNICO creado: {len(documents_draco)} documentos")
            else:
                self.draco_index = None
                # print("⚠️ No se encontraron archivos dracónicos, índice dracónico = None")
            
            # Resumen de engines creados
            # engines_created = []
            # if hasattr(self, 'index') and self.index:
            #     engines_created.append("MIXTO")
            # if hasattr(self, 'tropical_index') and self.tropical_index:
            #     engines_created.append("TROPICAL")
            # if hasattr(self, 'draco_index') and self.draco_index:
            #     engines_created.append("DRACÓNICO")
            
            # print(f"🎯 Engines RAG creados exitosamente: {', '.join(engines_created)}")
            
        except Exception as e:
            print(f"❌ Error en _create_all_engines: {e}")
            raise e
    
    def _load_target_titles(self):
        """Cargar títulos objetivo desde el archivo MD - por defecto tropical"""
        titles_file_path = "data/Títulos normalizados minusculas.txt"
        self.target_titles_set = self._load_target_titles_from_file(titles_file_path)

        if self.target_titles_set is None or not self.target_titles_set:
            print("❌ ERROR CRÍTICO: No se pudieron cargar los títulos objetivo, inicializando con set vacío")
            self.target_titles_set = set()
            return

        # print(f"🎯 Títulos objetivo cargados: {len(self.target_titles_set)}")

        # Debug: Mostrar títulos de planetas retrógrados específicos
        # retrograde_titles = [title for title in self.target_titles_set if "retrógrado" in title]
        # print(f"🔍 DEBUG: Títulos retrógrados en target_titles_set: {len(retrograde_titles)}")
        # for title in sorted(retrograde_titles):
        #     print(f"🔍 DEBUG: - '{title}'")

    def _load_target_titles_for_chart_type(self, chart_type: str):
        """Cargar títulos objetivo según el tipo de carta"""
        if chart_type.lower() == "draco":
            titles_file_path = "data/draco/Títulos normalizados minusculas.txt"
            # print(f"🔮 Cargando títulos dracónicos desde: {titles_file_path}")
        else:
            titles_file_path = "data/Títulos normalizados minusculas.txt"
            # print(f"🌞 Cargando títulos tropicales desde: {titles_file_path}")

        target_titles_set = self._load_target_titles_from_file(titles_file_path)

        if target_titles_set is None or not target_titles_set:
            # print(f"⚠️ No se pudieron cargar los títulos para {chart_type}, usando títulos tropicales por defecto")
            # Asegurar que siempre devolvemos un set válido, nunca None
            if self.target_titles_set is not None:
                return self.target_titles_set
            else:
                print(f"❌ ERROR CRÍTICO: target_titles_set también es None, devolviendo set vacío")
                return set()

        # print(f"🎯 Títulos {chart_type} cargados: {len(target_titles_set)}")
        return target_titles_set
    
    def _load_target_titles_from_file(self, filepath):
        """Carga títulos desde un archivo de texto plano, uno por línea."""
        target_titles = set()
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                for line in file:
                    title = line.strip()
                    if title:
                        target_titles.add(title)
        except FileNotFoundError:
            print(f"❌ ERROR CRÍTICO: No se encontró el archivo de títulos en {filepath}")
        except Exception as e:
            print(f"❌ Error cargando títulos desde {filepath}: {e}")
        
        # print(f"📊 DEBUG: Total de {len(target_titles)} títulos cargados desde '{filepath}'.")
        # Mostrar algunos ejemplos
        # sample_titles = list(target_titles)[:5]
        # for title in sample_titles:
        #     print(f"   📝 Ejemplo: '{title}'")
                
        return target_titles
    
    def _normalize_title(self, title: str) -> str:
        """Normalizar título para matching consistente"""
        # Remover paréntesis y contenido
        normalized = re.sub(r'\s*\([^)]*\)', '', title)
        # Remover dos puntos y contenido posterior
        normalized = re.sub(r':.*', '', normalized)
        # Convertir a minúsculas
        normalized = normalized.lower()
        # Normalizar espacios
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        # Normalizar "casa dos" -> "casa 2"
        normalized = normalized.replace(" en casa dos", " en casa 2")
        # Remover asteriscos de markdown
        normalized = re.sub(r'\*+', '', normalized).strip()
        
        return normalized
    
    def _is_relevant_title(self, title: str) -> bool:
        """Verificar si un título es relevante para interpretación"""
        return (
            title.startswith("aspecto ") or
            " en " in title or
            title.endswith(" retrógrado") or
            " en el ascendente" in title or
            " retrógrado" in title  # Captura adicional para retrógrados
        )
    
    def _process_aspect_title(self, title: str, aspect_keywords: List[str]) -> set:
        """Procesar títulos de aspectos complejos"""
        processed_aspects = set()
        
        match_aspect = re.match(r"aspecto\s+([a-záéíóúüñ]+)\s+(.*?)\s+a\s+([a-záéíóúüñ]+)", title)
        if match_aspect:
            planet1 = match_aspect.group(1)
            aspect_part = match_aspect.group(2)
            planet2 = match_aspect.group(3)

            found_aspects = [kw for kw in aspect_keywords if kw in aspect_part.split()]

            if found_aspects:
                for asp in found_aspects:
                    specific_title = f"aspecto {planet1} {asp} a {planet2}"
                    processed_aspects.add(specific_title)
            else:
                processed_aspects.add(title)
        else:
            processed_aspects.add(title)
            
        return processed_aspects
    
    def _remove_accents(self, text: str) -> str:
        """Remover acentos de un texto para matching más flexible"""
        return unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('ascii')
    
    def _get_query_engine(self, chart_type: str = "tropical", **kwargs):
        """
        Obtener el motor de consulta RAG apropiado según el tipo de carta y feature flag
        
        Args:
            chart_type: "tropical" o "draco"
            **kwargs: Argumentos adicionales para as_query_engine()
        
        Returns:
            Query engine configurado
        """
        try:
            # Si el feature flag está desactivado, usar siempre el índice mixto (sistema actual)
            if not self.USE_SEPARATE_ENGINES:
                # print(f"🔧 Usando índice MIXTO (feature flag desactivado)")
                return self.index.as_query_engine(**kwargs)
            
            # Si el feature flag está activado, usar índices separados
            # print(f"🔧 Feature flag activado - seleccionando índice para carta {chart_type}")
            
            if chart_type.lower() == "draco":
                if hasattr(self, 'draco_index') and self.draco_index is not None:
                    # print(f"✅ Usando índice DRACÓNICO separado")
                    return self.draco_index.as_query_engine(**kwargs)
                else:
                    # print(f"⚠️ Índice dracónico no disponible, fallback a índice mixto")
                    return self.index.as_query_engine(**kwargs)
            else:
                # chart_type == "tropical" o cualquier otro valor
                if hasattr(self, 'tropical_index') and self.tropical_index is not None:
                    # print(f"✅ Usando índice TROPICAL separado")
                    return self.tropical_index.as_query_engine(**kwargs)
                else:
                    # print(f"⚠️ Índice tropical no disponible, fallback a índice mixto")
                    return self.index.as_query_engine(**kwargs)
                    
        except Exception as e:
            print(f"❌ Error en _get_query_engine: {e}")
            # print(f"🔄 Fallback a índice mixto por error")
            return self.index.as_query_engine(**kwargs)
    
    def _setup_base_prompt(self):
        """Configurar prompt base para RAG"""
        prompt_str = get_rag_extraction_prompt_str()
        self.base_custom_prompt_template = PromptTemplate(prompt_str)
    
    async def generar_interpretacion_completa(self, carta_natal_data: Dict[str, Any], genero: str, tipo_carta: str = "tropical") -> Dict[str, Any]:
        """
        Generar interpretación completa (narrativa + individual)

        Args:
            carta_natal_data: Datos de carta natal del microservicio
            genero: "masculino" o "femenino"
            tipo_carta: "tropical" o "draco" para determinar qué títulos usar

        Returns:
            Dict con interpretacion_narrativa, interpretaciones_individuales, tiempo_generacion
        """
        try:
            start_time = time.time()

            # DEBUG: Ver qué datos recibe el RAG system
            # print(f"🔍 DEBUG PAYLOAD KEYS: {list(carta_natal_data.keys())}")
            # if 'cuspides_cruzadas' in carta_natal_data and carta_natal_data['cuspides_cruzadas'] is not None:
            #     print(f"🔮 DEBUG: ¡Cúspides cruzadas encontradas! Cantidad: {len(carta_natal_data['cuspides_cruzadas'])}")
            # else:
            #     print(f"❌ DEBUG: NO se encontraron cúspides cruzadas en el payload (None o ausente)")

            # DEBUG: Verificar estado de target_titles_set
            # print(f"🔍 DEBUG: self.target_titles_set type = {type(self.target_titles_set)}")
            # print(f"🔍 DEBUG: self.target_titles_set is None = {self.target_titles_set is None}")
            # if self.target_titles_set is not None:
            #     print(f"🔍 DEBUG: len(self.target_titles_set) = {len(self.target_titles_set)}")

            # Cargar títulos específicos para el tipo de carta
            # print(f"🔮 Configurando interpretación para carta {tipo_carta}")
            target_titles_for_chart = self._load_target_titles_for_chart_type(tipo_carta)

            # Adaptar datos del microservicio al formato RAG
            carta_adaptada = self._adaptar_datos_microservicio(carta_natal_data)

            # Extraer eventos de la carta natal
            eventos = self._extract_events_from_carta(carta_adaptada)

            # Calcular planetas en casas
            planets_in_houses = self._calculate_house_placements(
                carta_adaptada.get('points', {}),
                carta_adaptada.get('houses', {})
            )

            # Agregar eventos de planetas en casas
            for planet, house in planets_in_houses.items():
                eventos.append({
                    "tipo": "PlanetaEnCasa",
                    "planeta": planet,
                    "casa": house
                })

            # Evaluar aspectos complejos
            complex_events = self._evaluate_complex_aspects(eventos, planets_in_houses, carta_adaptada)
            eventos.extend(complex_events)
            # print(f"🐛 DEBUG: tipo_carta = {repr(tipo_carta)} antes de llamar _filter_events_by_target_titles_for_chart")
            # print(f"🐛 DEBUG: tipo_carta = {repr(tipo_carta)} antes de llamar _filter_events_by_target_titles_for_chart")        # Filtrar eventos según títulos objetivo específicos del tipo de carta
            eventos_filtrados = self._filter_events_by_target_titles_for_chart(eventos, target_titles_for_chart, tipo_carta)
            
            # print(f"📊 Eventos filtrados para interpretar: {len(eventos_filtrados)} (de {len(eventos)} iniciales)")
            
            # Configurar prompt con género
            final_prompt_template = self._create_gender_prompt(genero)
            
            # Crear motor de consulta RAG usando el método que selecciona el índice apropiado
            query_engine_rag = self._get_query_engine(
                chart_type=tipo_carta,
                similarity_top_k=1,
                text_qa_template=final_prompt_template
            )
            
            # Generar interpretaciones individuales usando concurrencia
            interpretaciones_individuales = await self._generar_interpretaciones_concurrentes(
                eventos_filtrados, query_engine_rag, tipo_carta
            )
            
            # Generar interpretación narrativa
            interpretacion_narrativa = await self._generar_interpretacion_narrativa(
                interpretaciones_individuales, genero, carta_adaptada.get('nombre', 'Usuario'), tipo_carta
            )
            
            end_time = time.time()
            tiempo_generacion = end_time - start_time
            
            return {
                "interpretacion_narrativa": interpretacion_narrativa,
                "interpretaciones_individuales": interpretaciones_individuales,
                "tiempo_generacion": tiempo_generacion
            }
        
        except Exception as e:
            import traceback
            print(f"❌ ERROR DETALLADO: {e}")
            print(f"📍 STACK TRACE:")
            traceback.print_exc()
            raise e
    
    def _adaptar_datos_microservicio(self, datos_microservicio: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adaptar datos del microservicio al formato que espera el RAG
        
        El microservicio envía datos en formato compatible, pero necesitamos
        asegurar que tenga la estructura exacta que espera el código RAG
        """
        # Si los datos ya vienen en el formato correcto, devolverlos tal como están
        if all(key in datos_microservicio for key in ['points', 'houses', 'aspects']):
            return datos_microservicio
        
        # Si no, adaptar el formato (esto sería para casos especiales)
        carta_adaptada = {
            "nombre": datos_microservicio.get("nombre", "Usuario"),
            "points": datos_microservicio.get("points", {}),
            "houses": datos_microservicio.get("houses", {}),
            "aspects": datos_microservicio.get("aspects", []),
            "location": datos_microservicio.get("location", {}),
            "fecha_hora_natal": datos_microservicio.get("fecha_hora_natal", ""),
            "tipo": datos_microservicio.get("tipo", "Tropical")
        }
        
        return carta_adaptada
    
    def _extract_events_from_carta(self, carta_natal_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extraer eventos de los datos de carta natal"""
        eventos = []
        
        # Definir ángulos astrológicos
        angulos = {"Asc": "Ascendente", "MC": "Medio Cielo", "Ic": "Fondo del Cielo", "Dsc": "Descendente"}
        
        # Planetas en signos y ángulos
        if "points" in carta_natal_data:
            for name, details in carta_natal_data["points"].items():
                if "sign" in details:
                    # Verificar si es un ángulo
                    if name in angulos:
                        eventos.append({
                            "tipo": "AnguloEnSigno",
                            "angulo": name,
                            "angulo_es": angulos[name],
                            "signo": details["sign"],
                            "grados": details.get("degrees")
                        })
                        # print(f"🔍 DEBUG: Ángulo detectado: {angulos[name]} en {details['sign']}")
                    else:
                        # Es un planeta normal
                        eventos.append({
                            "tipo": "PlanetaEnSigno",
                            "planeta": name,
                            "signo": details["sign"],
                            "grados": details.get("degrees")
                        })
                        
                        if details.get("retrograde", False):
                            # print(f"🔍 DEBUG: Planeta retrógrado detectado: {name} (retrograde: {details.get('retrograde')})")
                            eventos.append({
                                "tipo": "PlanetaRetrogrado",
                                "planeta": name,
                                "signo": details["sign"],
                                "grados": details.get("degrees")
                            })
        
        # Casas en signos
        if "houses" in carta_natal_data:
            for house_num, details in carta_natal_data["houses"].items():
                if "sign" in details:
                    eventos.append({
                        "tipo": "CasaEnSigno",
                        "casa": house_num,
                        "signo": details["sign"]
                    })
        
        # Aspectos
        if "aspects" in carta_natal_data:
            for aspect_details in carta_natal_data["aspects"]:
                eventos.append({
                    "tipo": "Aspecto",
                    "planeta1": aspect_details["point1"],
                    "aspecto": aspect_details["aspect"],
                    "planeta2": aspect_details["point2"]
                })
        
        # Cúspides Cruzadas (solo para cartas dracónicas)
        if "cuspides_cruzadas" in carta_natal_data and carta_natal_data["cuspides_cruzadas"] is not None:
            # print(f"🔮 DEBUG: Detectadas {len(carta_natal_data['cuspides_cruzadas'])} cúspides cruzadas")
            for cuspide_cruzada in carta_natal_data["cuspides_cruzadas"]:
                eventos.append({
                    "tipo": "CuspideCruzada",
                    "casa_draconica": cuspide_cruzada["casa_draconica"],
                    "casa_tropical": cuspide_cruzada["casa_tropical_ubicacion"],
                    "descripcion": cuspide_cruzada.get("descripcion", "")
                })
                # print(f"🔮 DEBUG: Cúspide cruzada: Casa {cuspide_cruzada['casa_draconica']} dracónica → Casa {cuspide_cruzada['casa_tropical_ubicacion']} tropical")
        
        # Aspectos Cruzados (solo para cartas dracónicas)
        if "aspectos_cruzados" in carta_natal_data and carta_natal_data["aspectos_cruzados"] is not None:
            # print(f"🔮 DEBUG: Detectados {len(carta_natal_data['aspectos_cruzados'])} aspectos cruzados")
            for aspecto_cruzado in carta_natal_data["aspectos_cruzados"]:
                eventos.append({
                    "tipo": "AspectoCruzado",
                    "planeta_draconico": aspecto_cruzado["punto_draconico"],
                    "planeta_tropical": aspecto_cruzado["punto_tropical"],
                    "tipo_aspecto": aspecto_cruzado["tipo_aspecto"],
                    "orbe": aspecto_cruzado.get("orbe", 0)
                })
                # print(f"🔮 DEBUG: Aspecto cruzado: {aspecto_cruzado['punto_draconico']} dracónico {aspecto_cruzado['tipo_aspecto']} {aspecto_cruzado['punto_tropical']} tropical")
        
        return eventos
    
    def _calculate_house_placements(self, planets_data: Dict[str, Any], houses_data: Dict[str, Any]) -> Dict[str, int]:
        """Calcular en qué casa cae cada planeta"""
        if not planets_data or not houses_data:
            return {}

        cusps_lon = {}
        for i in range(1, 13):
            house_num_str = str(i)
            if house_num_str in houses_data:
                cusps_lon[i] = houses_data[house_num_str]['longitude']
            else:
                return {}

        if len(cusps_lon) != 12:
            return {}

        house_placements = {}
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

        return house_placements
    
    def _evaluate_complex_aspects(self, eventos: List[Dict[str, Any]], planets_in_houses: Dict[str, int], raw_json_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Evaluar aspectos complejos - versión simplificada"""
        complex_events = []
        
        # Planetas en el ascendente (Casa 1)
        planetas_ascendente = ["Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]
        
        for planeta in planetas_ascendente:
            if planets_in_houses.get(planeta) == 1:
                planeta_es = self._translate_planet(planeta)
                complex_events.append({
                    "tipo": "AspectoComplejo",
                    "titulo_especifico": f"{planeta_es} en el ascendente",
                    "descripcion": f"{planeta_es} en Casa 1"
                })
        
        return complex_events
    
    def _flexible_title_match(self, consulta: str) -> bool:
        """
        Verificar si una consulta específica coincide con algún título objetivo usando lógica flexible.
        Maneja casos de aspectos simples y aspectos de tránsito complejos.
        Incluye normalización de acentos para matching más robusto.
        """
        # Verificar que target_titles_set no sea None
        if self.target_titles_set is None:
            print(f"❌ ERROR: target_titles_set es None en _flexible_title_match")
            return False

        # Normalizar la consulta removiendo acentos
        consulta_sin_acentos = self._remove_accents(consulta)

        # 🔮 DEBUG LOG: Diagnóstico para Sol Dracónico en Libra
        # if "sol" in consulta and "libra" in consulta and "draconico" in consulta_sin_acentos:
        #     print(f"🔮 DEBUG MATCH: Buscando '{consulta}' (sin acentos: '{consulta_sin_acentos}') en títulos")
        #     print(f"🔮 DEBUG MATCH: Total títulos disponibles: {len(self.target_titles_set)}")
        #     # Mostrar algunos títulos relevantes
        #     relevant_titles = [t for t in self.target_titles_set if "sol" in t and "libra" in t]
        #     print(f"🔮 DEBUG MATCH: Títulos relevantes encontrados: {relevant_titles}")
        
        # 1. Coincidencia exacta con normalización de acentos
        for titulo_objetivo in self.target_titles_set:
            titulo_sin_acentos = self._remove_accents(titulo_objetivo)
            if consulta_sin_acentos == titulo_sin_acentos:
                # if "sol" in consulta and "libra" in consulta and "draconico" in consulta_sin_acentos:
                #     print(f"✅ MATCH EXACTO (sin acentos) encontrado: '{consulta}' → '{titulo_objetivo}'")
                return True

        # 2. Lógica mejorada para aspectos de tránsito (ej: "urano en tránsito cuadratura a saturno natal")
        # La consulta generada siempre usa "a"
        match_consulta = re.search(r'(\w+)\s+en tránsito\s+(.*?)\s+a\s+(\w+)\s+natal', consulta)
        if match_consulta:
            p1_consulta = match_consulta.group(1)
            aspecto_consulta = match_consulta.group(2).strip()
            p2_consulta = match_consulta.group(3)

            for titulo_objetivo in self.target_titles_set:
                # Buscar solo en títulos que contengan los planetas para optimizar
                if p1_consulta in titulo_objetivo and p2_consulta in titulo_objetivo and "en tránsito" in titulo_objetivo:
                    
                    # Regex flexible para el título objetivo, que puede tener "a", "al", o "a la", y "por" opcionalmente.
                    match_objetivo = re.search(r'(\w+)\s+en tránsito(?:\s+por)?\s+(.*?)\s+(?:a|al|a la)\s+(\w+)\s+natal', titulo_objetivo)
                    
                    if match_objetivo:
                        p1_objetivo = match_objetivo.group(1)
                        aspectos_objetivo_str = match_objetivo.group(2).strip()
                        p2_objetivo = match_objetivo.group(3)

                        # Caso especial: si la regex captura el aspecto en el grupo 2, pero es un título simple como "oposición al sol natal"
                        # el grupo 2 puede quedar vacío. Hay que re-capturar el aspecto.
                        if not aspectos_objetivo_str:
                             temp_match = re.search(r'en tránsito\s+(?:por\s+)?(.*?)\s+(?:a|al)', titulo_objetivo)
                             if temp_match:
                                 aspectos_objetivo_str = temp_match.group(1).strip()


                        if p1_consulta == p1_objetivo and p2_consulta == p2_objetivo:
                            # La parte de los aspectos puede ser una lista ("conjunción o cuadratura") o un solo aspecto ("oposición")
                            lista_aspectos = re.split(r'\s+o\s+|\s+u\s+', aspectos_objetivo_str)
                            lista_aspectos_limpia = [a.strip() for a in lista_aspectos]
                            
                            if aspecto_consulta in lista_aspectos_limpia:
                                # print(f"✅ MATCH FLEXIBLE (TRÁNSITO): '{consulta}' coincide con '{titulo_objetivo}'")
                                return True
            # Si la lógica de tránsito no encuentra nada, no retornamos False aún, dejamos que la lógica general actúe

        # 3. Lógica general para otros aspectos (ej: "sol conjunción a luna")
        if " a " in consulta:
            parts = consulta.split(" a ")
            if len(parts) == 2:
                left_part = parts[0].strip()
                p2_consulta = parts[1].strip()
                
                left_words = left_part.split()
                if len(left_words) >= 2:
                    p1_consulta = left_words[0]
                    aspecto_consulta = " ".join(left_words[1:])

                    for titulo_objetivo in self.target_titles_set:
                        if " a " in titulo_objetivo and p1_consulta in titulo_objetivo and p2_consulta in titulo_objetivo:
                            # Lógica para títulos que agrupan aspectos (ej: "sol conjunción o cuadratura a luna")
                            titulo_parts = titulo_objetivo.split(" a ")
                            if len(titulo_parts) == 2:
                                titulo_left = titulo_parts[0].strip()
                                titulo_p2 = titulo_parts[1].strip()

                                if p2_consulta == titulo_p2:
                                    titulo_words = titulo_left.split()
                                    if len(titulo_words) >= 2 and titulo_words[0] == p1_consulta:
                                        titulo_aspectos_str = " ".join(titulo_words[1:])
                                        
                                        lista_aspectos = re.split(r'\s+o\s+|\s+u\s+', titulo_aspectos_str)
                                        lista_aspectos_limpia = [a.strip() for a in lista_aspectos]

                                        if aspecto_consulta in lista_aspectos_limpia:
                                            # print(f"✅ MATCH FLEXIBLE (ASPECTO GENERAL): '{consulta}' coincide con '{titulo_objetivo}'")
                                            return True
        
        return False
    
    def _filter_events_by_target_titles(self, eventos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filtrar eventos según títulos objetivo con matching flexible"""
        eventos_filtrados = []

        for evento in eventos:
            if evento.get("tipo") == "AspectoComplejo":
                eventos_filtrados.append(evento)
            else:
                consulta_potencial = self._generar_consulta_estandarizada(evento)
                consulta_normalizada = consulta_potencial.lower()

                # Debug específico para planetas retrógrados
                # if evento.get("tipo") == "PlanetaRetrogrado":
                #     print(f"🔍 DEBUG FILTRO: Planeta retrógrado - {evento.get('planeta')}")
                #     print(f"🔍 DEBUG FILTRO: Consulta generada: '{consulta_normalizada}'")

                # Debug específico para aspectos
                # if evento.get("tipo") == "Aspecto":
                #     print(f"🔍 DEBUG FILTRO: Aspecto - {evento.get('planeta1')} {evento.get('aspecto')} {evento.get('planeta2')}")
                #     print(f"🔍 DEBUG FILTRO: Consulta generada: '{consulta_normalizada}'")

                # Usar matching flexible
                if self._flexible_title_match(consulta_normalizada):
                    eventos_filtrados.append(evento)
                    # print(f"✅ EVENTO APROBADO: '{consulta_normalizada}'")
                else:
                    # print(f"❌ EVENTO RECHAZADO: '{consulta_normalizada}'")
                    pass

        return eventos_filtrados

    def _filter_events_by_target_titles_for_chart(self, eventos: List[Dict[str, Any]], target_titles_for_chart: set, chart_type: str = "tropical") -> List[Dict[str, Any]]:
        """Filtrar eventos según títulos objetivo específicos del tipo de carta"""
        eventos_filtrados = []

        # Guardar temporalmente los títulos objetivo originales
        original_titles = self.target_titles_set

        # Usar los títulos específicos de la carta
        self.target_titles_set = target_titles_for_chart

        try:
            for evento in eventos:
                if evento.get("tipo") == "AspectoComplejo":
                    eventos_filtrados.append(evento)
                else:
                    consulta_potencial = self._generar_consulta_estandarizada(evento, chart_type)
                    consulta_normalizada = consulta_potencial.lower()

                    # Debug específico para debugging
                    # if evento.get("tipo") == "PlanetaEnSigno":
                    #     print(f"🔍 DEBUG DRACO: Buscando '{consulta_normalizada}' en títulos dracónicos")

                    # Usar matching flexible con los títulos específicos
                    if self._flexible_title_match(consulta_normalizada):
                        eventos_filtrados.append(evento)
                        # print(f"✅ EVENTO DRACO APROBADO: '{consulta_normalizada}'")
                    else:
                        # print(f"❌ EVENTO DRACO RECHAZADO: '{consulta_normalizada}'")
                        pass
        finally:
            # Restaurar los títulos objetivo originales
            self.target_titles_set = original_titles

        return eventos_filtrados
    
    def _generar_consulta_estandarizada(self, evento: Dict[str, Any], chart_type: str = "tropical") -> str:
        """Generar consulta estandarizada para un evento"""
        tipo = evento.get("tipo")

        if tipo == "Aspecto":
            p1_es = self._translate_planet(evento.get('planeta1'))
            asp_es = self._translate_aspect(evento.get('aspecto'))
            p2_es = self._translate_planet(evento.get('planeta2'))
            return f"{p1_es.lower()} {asp_es.lower()} a {p2_es.lower()}"

        elif tipo == "PlanetaEnSigno":
            planeta_orig = evento.get('planeta')
            if planeta_orig == "True North Node":
                planeta_query = "nodo"
            else:
                planeta_es = self._translate_planet(planeta_orig)
                planeta_query = planeta_es.lower()

            signo_es = self._translate_sign(evento.get('signo'))

            # Agregar "dracónico/dracónica" para cartas dracónicas con género correcto
            if chart_type.lower() == "draco":
                # Luna usa forma femenina "dracónica"
                if planeta_orig == "Moon":
                    draconico_suffix = " dracónica"
                else:
                    draconico_suffix = " dracónico"
            else:
                draconico_suffix = ""
            
            consulta_final = f"{planeta_query}{draconico_suffix} en {signo_es.lower()}"
            return consulta_final

        elif tipo == "AnguloEnSigno":
            angulo_es = evento.get('angulo_es')  # "Ascendente", "Medio Cielo", etc.
            signo_es = self._translate_sign(evento.get('signo'))

            # Agregar "dracónico" para ángulos en cartas dracónicas (sin "(ángulo)")
            draconico_suffix = " dracónico" if chart_type.lower() == "draco" else ""
            if chart_type.lower() == "draco":
                return f"{angulo_es.lower()}{draconico_suffix} en {signo_es.lower()}"
            else:
                return f"{angulo_es.lower()}{draconico_suffix} (ángulo) en {signo_es.lower()}"

        elif tipo == "PlanetaEnCasa":
            planeta_orig = evento.get('planeta')
            if planeta_orig == "True North Node":
                planeta_query = "nodo"
            else:
                planeta_es = self._translate_planet(planeta_orig)
                planeta_query = planeta_es.lower()

            # Agregar "dracónico" para cartas dracónicas
            draconico_suffix = " dracónico" if chart_type.lower() == "draco" else ""
            return f"{planeta_query}{draconico_suffix} en casa {evento.get('casa')}"

        elif tipo == "CasaEnSigno":
            signo_es = self._translate_sign(evento.get('signo'))
            return f"casa {evento.get('casa')} en {signo_es.lower()}"

        elif tipo == "PlanetaRetrogrado":
            planeta_orig = evento.get('planeta')
            if planeta_orig == "True North Node":
                planeta_query = "nodo"
            else:
                planeta_es = self._translate_planet(planeta_orig)
                planeta_query = planeta_es.lower()

            # Agregar "dracónico" para cartas dracónicas
            draconico_suffix = " dracónico" if chart_type.lower() == "draco" else ""
            return f"{planeta_query}{draconico_suffix} retrógrado"

        elif tipo == "CuspideCruzada":
            casa_draconica = evento.get("casa_draconica")
            casa_tropical = evento.get("casa_tropical")
            
            # Generar consulta según el patrón de los títulos
            if casa_draconica == 1:
                # Caso especial para Ascendente dracónico
                return f"la cuspide del ascendente draconico superpuesto a la casa {casa_tropical} tropica"
            else:
                # Casos normales para casas 2-12
                return f"la cuspide de la casa {casa_draconica} draconica superpuesta a la casa {casa_tropical} tropica"

        elif tipo == "AspectoCruzado":
            planeta_drac = self._translate_planet(evento.get("planeta_draconico")).lower()
            planeta_trop = self._translate_planet(evento.get("planeta_tropical")).lower()
            aspecto = evento.get("tipo_aspecto").lower()
            
            # APLICAR GÉNERO CORRECTO usando función auxiliar
            draconico_suffix = self._get_draconico_suffix(evento.get("planeta_draconico"))
            
            # Generar consulta con género correcto
            # Ejemplo: "oposicion de luna draconica con neptuno tropico" (femenino)
            # Ejemplo: "conjuncion de mercurio draconico con neptuno tropico" (masculino)
            return f"{aspecto} de {planeta_drac}{draconico_suffix} con {planeta_trop} tropico"

        elif tipo == "AspectoComplejo":
            return evento.get("titulo_especifico", "").lower()

        return f"Evento {tipo}: {evento}"
    
    def _translate_planet(self, planet: str) -> str:
        """Traducir nombre de planeta al español"""
        translations = {
            "Sun": "Sol", "Moon": "Luna", "Mercury": "Mercurio", "Venus": "Venus", "Mars": "Marte",
            "Jupiter": "Júpiter", "Saturn": "Saturno", "Uranus": "Urano", "Neptune": "Neptuno",
            "Pluto": "Plutón", "Asc": "Ascendente", "MC": "Medio Cielo", "Ic": "Fondo del Cielo",
            "Dsc": "Descendente", "True North Node": "Nodo Norte Verdadero",
            "Lilith": "Lilith", "Chiron": "Quirón",
            "Part of Fortune": "Parte de la Fortuna", "Vertex": "Vertex"
        }
        return translations.get(planet, planet)
    
    def _translate_sign(self, sign: str) -> str:
        """Traducir nombre de signo al español"""
        translations = {
            "Aries": "Aries", "Taurus": "Tauro", "Gemini": "Géminis", "Cancer": "Cáncer",
            "Leo": "Leo", "Virgo": "Virgo", "Libra": "Libra", "Scorpio": "Escorpio",
            "Sagittarius": "Sagitario", "Capricorn": "Capricornio", "Aquarius": "Acuario",
            "Pisces": "Piscis"
        }
        return translations.get(sign, sign)
    
    def _translate_aspect(self, aspect: str) -> str:
        """Traducir nombre de aspecto al español"""
        translations = {
            "Conjunción": "Conjunción", "Oposición": "Oposición", "Cuadratura": "Cuadratura",
            "Trígono": "Trígono", "Sextil": "Sextil"
        }
        return translations.get(aspect, aspect)
    
    def _get_draconico_suffix(self, planet: str) -> str:
        """Obtener sufijo dracónico con género correcto (sin tildes para matching)"""
        return " draconica" if planet == "Moon" else " draconico"
    
    def _format_degrees(self, decimal_degrees: Optional[float]) -> str:
        """Formatear grados decimales a grados y minutos"""
        if decimal_degrees is None:
            return ""
        degrees = int(decimal_degrees)
        minutes = int(round((decimal_degrees - degrees) * 60))
        return f"{degrees}° {minutes:02d}'"
    
    def _create_gender_prompt(self, genero: str) -> PromptTemplate:
        """Crear prompt con instrucciones de género"""
        if genero.lower() == "femenino":
            genero_instruccion = "Instrucción adicional: Redacta usando el género gramatical femenino."
        elif genero.lower() == "masculino":
            genero_instruccion = "Instrucción adicional: Redacta usando el género gramatical masculino."
        else:
            genero_instruccion = ""
        
        persona_instruccion = "Instrucción adicional: Dirígete directamente a la persona usando la segunda persona singular (Tú)."
        instrucciones_adicionales = f"{genero_instruccion}\n{persona_instruccion}".strip()
        
        if instrucciones_adicionales:
            prompt_template_str = (
                f"{instrucciones_adicionales}\n"
                + self.base_custom_prompt_template.template
            )
            return PromptTemplate(prompt_template_str)
        
        return self.base_custom_prompt_template
    
    def _create_interpretation_item(self, evento: Dict[str, Any], interpretacion: str) -> Dict[str, Any]:
        """Crear item de interpretación estructurado"""
        tipo = evento.get("tipo")
        item = {
            "titulo": "",
            "tipo": tipo,
            "interpretacion": interpretacion
        }
        
        if tipo == "PlanetaEnSigno":
            planeta_orig = evento.get('planeta')
            planeta_es = self._translate_planet(planeta_orig)
            signo_es = self._translate_sign(evento.get('signo'))
            grados = evento.get('grados')
            grados_formateados = self._format_degrees(grados)
            
            if grados_formateados:
                item["titulo"] = f"Tu {planeta_es} se encuentra a {grados_formateados} de {signo_es}"
            else:
                item["titulo"] = f"Tu {planeta_es} en {signo_es}"
            
            item["planeta"] = planeta_es
            item["signo"] = signo_es
            if grados_formateados:
                item["grados"] = grados_formateados
                
        elif tipo == "PlanetaEnCasa":
            planeta_es = self._translate_planet(evento.get('planeta'))
            casa = evento.get('casa')
            item["titulo"] = f"Tu {planeta_es} en Casa {casa}"
            item["planeta"] = planeta_es
            item["casa"] = str(casa)
            
        elif tipo == "PlanetaRetrogrado":
            planeta_es = self._translate_planet(evento.get('planeta'))
            signo_es = self._translate_sign(evento.get('signo')) if evento.get('signo') else None
            grados = evento.get('grados')
            grados_formateados = self._format_degrees(grados) if grados else None
            
            # Crear título con información completa
            if signo_es and grados_formateados:
                item["titulo"] = f"Tu {planeta_es} está Retrógrado a {grados_formateados} de {signo_es}"
                item["signo"] = signo_es
                item["grados"] = grados_formateados
            else:
                item["titulo"] = f"Tu {planeta_es} está Retrógrado"
            
            item["planeta"] = planeta_es
            
        elif tipo == "Aspecto":
            p1_es = self._translate_planet(evento.get('planeta1'))
            asp_es = self._translate_aspect(evento.get('aspecto'))
            p2_es = self._translate_planet(evento.get('planeta2'))
            item["titulo"] = f"Aspecto: Tu {p1_es} en {asp_es} con tu {p2_es}"
            item["planeta1"] = p1_es
            item["planeta2"] = p2_es
            item["aspecto"] = asp_es
            
        elif tipo == "CasaEnSigno":
            signo_es = self._translate_sign(evento.get('signo'))
            casa = evento.get('casa')
            item["titulo"] = f"La Cúspide de tu Casa {casa} está en {signo_es}"
            item["casa"] = str(casa)
            item["signo"] = signo_es
            
        elif tipo == "AnguloEnSigno":
            angulo_es = evento.get('angulo_es')  # "Ascendente", "Medio Cielo", etc.
            signo_es = self._translate_sign(evento.get('signo'))
            grados = evento.get('grados')
            grados_formateados = self._format_degrees(grados)
            
            if grados_formateados:
                item["titulo"] = f"Tu {angulo_es} se encuentra a {grados_formateados} de {signo_es}"
            else:
                item["titulo"] = f"Tu {angulo_es} en {signo_es}"
            
            item["angulo"] = angulo_es
            item["signo"] = signo_es
            if grados_formateados:
                item["grados"] = grados_formateados
                
        elif tipo == "CuspideCruzada":
            casa_draconica = evento.get("casa_draconica")
            casa_tropical = evento.get("casa_tropical")
            
            # Crear título descriptivo para cúspides cruzadas
            if casa_draconica == 1:
                item["titulo"] = f"Tu Ascendente Dracónico superpuesto a tu Casa {casa_tropical} Tropical"
            else:
                item["titulo"] = f"Tu Casa {casa_draconica} Dracónica superpuesta a tu Casa {casa_tropical} Tropical"
            
            item["casa_draconica"] = casa_draconica
            item["casa_tropical"] = casa_tropical
            
        elif tipo == "AspectoCruzado":
            planeta_drac_es = self._translate_planet(evento.get("planeta_draconico"))
            planeta_trop_es = self._translate_planet(evento.get("planeta_tropical"))
            aspecto_es = self._translate_aspect(evento.get("tipo_aspecto"))
            orbe = evento.get("orbe", 0)
            
            # Crear título descriptivo para aspectos cruzados
            item["titulo"] = f"Tu {planeta_drac_es} Dracónico en {aspecto_es} con tu {planeta_trop_es} Tropical"
            
            item["planeta_draconico"] = planeta_drac_es
            item["planeta_tropical"] = planeta_trop_es
            item["aspecto"] = aspecto_es
            if orbe:
                item["orbe"] = f"{orbe:.1f}°"
            
        elif tipo == "AspectoComplejo":
            titulo_especifico = evento.get("titulo_especifico", "")
            item["titulo"] = titulo_especifico
        
        return item
    
    async def _generar_interpretaciones_concurrentes(self, eventos_filtrados: List[Dict[str, Any]], query_engine_rag, chart_type: str = "tropical") -> List[Dict[str, Any]]:
        """Generar interpretaciones individuales usando concurrencia real con hilos para mejorar rendimiento"""
        
        def procesar_evento_individual(i: int, evento: Dict[str, Any]) -> Dict[str, Any]:
            """Procesar un evento individual de forma síncrona (se ejecutará en un hilo separado)"""
            consulta = self._generar_consulta_estandarizada(evento, chart_type)
            
            # DEBUG FASE 2: Verificar consultas generadas, especialmente "sol en capricornio"
            # if "capricornio" in consulta.lower():
            #     print(f"✅ DEBUG FASE 2: Consulta con 'capricornio' generada: '{consulta}'")
            #     print(f"🔍 DEBUG FASE 2: Evento que generó la consulta: {evento}")
            
            # print(f"🔍 Consultando RAG ({i+1}/{len(eventos_filtrados)}): {consulta}")
            
            try:
                # Ejecutar consulta RAG de forma síncrona (llama-index es bloqueante)
                respuesta = query_engine_rag.query(consulta)
                interpretacion = respuesta.response.strip() if respuesta.response else "No se encontró interpretación específica."
            except Exception as e:
                print(f"⚠️ Error al consultar RAG para '{consulta}': {e}")
                interpretacion = f"Error al obtener interpretación: {e}"
            
            # Crear item de interpretación
            return self._create_interpretation_item(evento, interpretacion)
        
        # Usar ThreadPoolExecutor para paralelización real de llamadas bloqueantes
        print(f"🚀 Ejecutando {len(eventos_filtrados)} consultas RAG en paralelo usando hilos...")
        
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor(max_workers=min(len(eventos_filtrados), 10)) as executor:
            # Crear tareas para cada evento
            tareas = [
                loop.run_in_executor(executor, procesar_evento_individual, i, evento)
                for i, evento in enumerate(eventos_filtrados)
            ]
            
            # Ejecutar todas las tareas en paralelo y esperar resultados
            interpretaciones_individuales = await asyncio.gather(*tareas)
        
        return interpretaciones_individuales
    
    async def _generar_interpretacion_narrativa(self, interpretaciones_individuales: List[Dict[str, Any]], genero: str, nombre: str, tipo_carta: str = "tropical") -> str:
        """Generar interpretación narrativa usando GPT-4"""
        try:
            # Usar el rewriter configurado en __init__ (GPT-4o, 128k context)
            llm_rewriter = self.llm_rewriter
            
            # Combinar interpretaciones individuales
            interpretaciones_texto = []
            for item in interpretaciones_individuales:
                titulo = item.get("titulo", "")
                interpretacion = item.get("interpretacion", "")
                interpretaciones_texto.append(f"### {titulo}\n{interpretacion}")
            
            interpretaciones_combinadas = "\n\n".join(interpretaciones_texto)
            
            # Configurar instrucciones de género
            if genero.lower() == "femenino":
                genero_instruccion = "Instrucción adicional: Redacta usando el género gramatical femenino."
            elif genero.lower() == "masculino":
                genero_instruccion = "Instrucción adicional: Redacta usando el género gramatical masculino."
            else:
                genero_instruccion = ""
            
            persona_instruccion = "Instrucción adicional: Dirígete directamente a la persona usando la segunda persona singular (Tú)."
            instrucciones_adicionales = f"{genero_instruccion}\n{persona_instruccion}".strip()
            
            # Seleccionar prompt según tipo de carta
            if tipo_carta.lower() == "draco":
                rewrite_prompt_str = self._get_draconian_narrative_prompt(instrucciones_adicionales, interpretaciones_combinadas)
            else:
                rewrite_prompt_str = self._get_tropical_narrative_prompt(instrucciones_adicionales, interpretaciones_combinadas)
            
            # Generar interpretación narrativa
            if LLAMA_INDEX_NEW:
                narrative_response = llm_rewriter.complete(rewrite_prompt_str)
                return narrative_response.text.strip()
            else:
                narrative_response = llm_rewriter.complete(rewrite_prompt_str)
                return narrative_response.text.strip()
            
        except Exception as e:
            print(f"❌ Error durante la re-escritura narrativa: {e}")
            return f"Error al generar el informe narrativo: {e}"

    def buscar_interpretacion_evento(self, evento: dict) -> str:
        """
        Busca la interpretación para un evento de calendario.
        Construye un título candidato basado en los datos del evento.
        """
        tipo_evento = evento.get("tipo_evento")
        descripcion = evento.get("descripcion", "")

        # Lógica para construir el título candidato
        titulo_candidato = descripcion # Usar descripción como base por defecto

        if tipo_evento == "Aspecto":
            planeta1 = evento.get("planeta1", "")
            planeta2 = evento.get("planeta2", "")
            tipo_aspecto = evento.get("tipo_aspecto", "")
            # Ejemplo: "Venus (directo) por tránsito esta en Oposición a tu Mercurio Natal"
            # Queremos extraer "venus en tránsito oposición a mercurio natal"
            if "por tránsito" in descripcion and planeta1 and planeta2 and tipo_aspecto:
                titulo_candidato = f"{planeta1.lower()} en tránsito {tipo_aspecto.lower()} a {planeta2.lower()} natal"
            elif planeta1 and planeta2 and tipo_aspecto:
                 titulo_candidato = f"{planeta1.lower()} {tipo_aspecto.lower()} a {planeta2.lower()}"

        elif tipo_evento in ["Luna Nueva", "Luna Llena"]:
            signo = evento.get("signo", "")
            casa = evento.get("casa_natal")
            if casa:
                # Formato corregido según feedback: "luna nueva en casa 1 natal"
                titulo_candidato = f"{tipo_evento.lower()} en casa {casa} natal"
            elif signo:
                titulo_candidato = f"{tipo_evento.lower()} en {signo.lower()}"

        elif tipo_evento in ["Eclipse Solar", "Eclipse Lunar"]:
             signo = evento.get("signo", "")
             casa = evento.get("casa_natal")
             if signo and casa:
                titulo_candidato = f"{tipo_evento.lower()} en {signo.lower()} en casa natal {casa}"
             elif signo:
                titulo_candidato = f"{tipo_evento.lower()} en {signo.lower()}"
        
        elif tipo_evento == "Luna Progresada":
            if "Conjunción" in descripcion:
                 # Extraer planeta de la descripción, ej: "Luna progresada Conjunción Sol Natal..."
                match = re.search(r'Conjunción (\w+) Natal', descripcion)
                if match:
                    planeta_natal = match.group(1)
                    titulo_candidato = f"luna progresada conjunción a {planeta_natal.lower()} natal"

        # Normalizar el título para la búsqueda
        consulta_normalizada = self._normalize_title(titulo_candidato)

        # Verificar si el título existe en nuestra base de conocimiento
        if self._flexible_title_match(consulta_normalizada):
            try:
                # Crear motor de consulta RAG (es rápido, se basa en el índice en memoria)
                query_engine_rag = self.index.as_query_engine(
                    similarity_top_k=1,
                    text_qa_template=self.base_custom_prompt_template
                )
                # Consultar al motor RAG
                respuesta = query_engine_rag.query(consulta_normalizada)
                interpretacion = respuesta.response.strip() if respuesta.response else "No se encontró una interpretación específica."
                return interpretacion
            except Exception as e:
                print(f"⚠️ Error al consultar RAG para '{consulta_normalizada}': {e}")
                return f"Error al obtener interpretación: {e}"
        else:
            return f"[SIN COINCIDENCIA]: {consulta_normalizada}"

    def _get_tropical_narrative_prompt(self, instrucciones_adicionales: str, interpretaciones_combinadas: str) -> str:
        """Crear prompt específico para cartas natales tropicales"""
        return get_tropical_narrative_prompt_str(instrucciones_adicionales, interpretaciones_combinadas)

    def _get_draconian_narrative_prompt(self, instrucciones_adicionales: str, interpretaciones_combinadas: str) -> str:
        """Crear prompt específico para cartas natales dracónicas - VERSIÓN REFINADA"""
        return get_draconian_narrative_prompt_str(instrucciones_adicionales, interpretaciones_combinadas)
