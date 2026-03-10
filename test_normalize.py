#!/usr/bin/env python3
"""
Test script para verificar que la normalización de keys funciona correctamente.
"""

import unicodedata

def _normalize_key(key: str) -> str:
    """
    Normaliza key: minúsculas, sin acentos, espacios limpios.
    Ej: "Plutón en Casa 12" → "pluton en casa 12"
    """
    # 1. Lowercase
    key = key.lower().strip()
    # 2. Eliminar acentos
    key = ''.join(c for c in unicodedata.normalize('NFD', key) 
                  if unicodedata.category(c) != 'Mn')
    # 3. Normalizar espacios múltiples
    key = ' '.join(key.split())
    return key

# Test cases
test_cases = [
    ("Plutón en Casa 12", "pluton en casa 12"),
    ("Júpiter en Géminis", "jupiter en geminis"),
    ("Sol EN casa 1", "sol en casa 1"),
    ("Saturno  en  Casa  10", "saturno en casa 10"),
    ("Venus Retrógrado", "venus retrogrado"),
    ("Nodo Norte en Cáncer", "nodo norte en cancer"),
    ("Ascendente en Piscis", "ascendente en piscis"),
    ("Conjunción de Marte", "conjuncion de marte"),
    ("Oposición al Sol", "oposicion al sol"),
]

print("🧪 Testing key normalization...")
print("=" * 60)

all_passed = True
for input_key, expected in test_cases:
    result = _normalize_key(input_key)
    status = "✅" if result == expected else "❌"
    if result != expected:
        all_passed = False
    print(f"{status} Input: '{input_key}'")
    print(f"   Expected: '{expected}'")
    print(f"   Got:      '{result}'")
    print()

print("=" * 60)
if all_passed:
    print("✅ All tests passed!")
else:
    print("❌ Some tests failed!")