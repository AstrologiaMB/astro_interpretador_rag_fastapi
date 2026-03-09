
import os
import sys

# Set the environment variable BEFORE importing/initializing
os.environ["USE_SEPARATE_ENGINES"] = "false"

try:
    from interpretador_refactored import InterpretadorRAG
    
    # Initialize gently (if possible, though __init__ does heavy lifting)
    # We really just want to check the flag after init
    print("🚀 Initializing InterpretadorRAG with USE_SEPARATE_ENGINES=false...")
    
    # Mocking external heavy calls might be needed if we want speed, 
    # but for true verification let's let it run (assuming keys are present)
    rag = InterpretadorRAG()
    
    print(f"✅ Flag Value: {rag.USE_SEPARATE_ENGINES}")
    
    if rag.USE_SEPARATE_ENGINES is False:
        print("SUCCESS: Flag correctly respected environment variable.")
    else:
        print("FAILURE: Flag is True despite env var set to 'false'.")

except Exception as e:
    print(f"❌ Error during verification: {e}")
