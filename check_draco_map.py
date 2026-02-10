from interpretador_refactored import InterpretadorRAG

print("--- Minimal Draco Map Check ---")
wrapper = InterpretadorRAG()

if hasattr(wrapper, 'interpretador_astrologico') and wrapper.interpretador_astrologico:
    print(f"✅ interpretador_astrologico exists.")
    if hasattr(wrapper.interpretador_astrologico, 'draco_map'):
        print(f"✅ draco_map exists. Len: {len(wrapper.interpretador_astrologico.draco_map)}")
    else:
        print(f"❌ draco_map attribute missing!")
else:
    print(f"❌ interpretador_astrologico is None or missing!")
