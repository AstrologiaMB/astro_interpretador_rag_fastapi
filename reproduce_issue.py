import os
import sys
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

print("🚀 Probando integración de LlamaIndex con Anthropic...")

try:
    from llama_index.llms.anthropic import Anthropic
    print("✅ Importado Anthropic desde llama_index.llms.anthropic")
except ImportError:
    try:
        from llama_index.llms import Anthropic
        print("✅ Importado Anthropic desde llama_index.llms (Legacy)")
    except ImportError as e:
        print(f"❌ Error importando Anthropic: {e}")
        sys.exit(1)

model_id = "claude-sonnet-4-5-20250929" # El ID que validamos

print(f"🛠️ Intentando instanciar Anthropic con model='{model_id}'...")

try:
    llm = Anthropic(api_key=api_key, model=model_id)
    print("✅ Instancia creada exitosamente.")
    
    print("📨 Intentando 'complete' con el modelo...")
    response = llm.complete("Hola, ¿estás funcionando?")
    print(f"✅ Respuesta recibida: {response.text}")

except Exception as e:
    print(f"❌ ERROR CRÍTICO al usar LlamaIndex/Anthropic: {e}")
    import traceback
    traceback.print_exc()
