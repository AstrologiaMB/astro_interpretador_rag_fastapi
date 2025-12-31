
import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    print("❌ No API Key found")
    exit(1)

client = Anthropic(api_key=api_key)

try:
    print("🚀 Querying models...")
    # Anthropic API doesn't have a simple "list models" endpoint in the public SDK usually?
    # Wait, let's check if the SDK supports it. If not, we might have to use a known list or just try to complete with different models.
    # Actually, recent API versions DO support listing models.
    # https://docs.anthropic.com/en/api/models-list
    
    # Not all SDK versions might have it, but let's try assuming a recent SDK
    # If this fails, we will try a completion with "claude-3-5-sonnet-latest" and catch the error message which usually lists valid models.
    
    # Try listing (requires newer API features)
    # If the SDK is old or doesn't map it, we might get an error.
    # But we installed anthropic>=0.18.0, so it should be fine.
    
    # Note: As of my last training data, listing models might not be a direct method on `client.models`? 
    # Let's try to inspect client attributes or just run a completion test.
    
    # Listing isn't always available on all tiers/keys.
    # Strategy: Try to list. If fails, try a dummy completion with a bogus model to see available ones in error, or try the known 3.5 Sonnet IDs.
    
    import requests
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01"
    }
    # Direct Requests call is safer if SDK method is unknown
    response = requests.get("https://api.anthropic.com/v1/models", headers=headers)
    
    if response.status_code == 200:
        models = response.json().get("data", [])
        print(f"✅ Found {len(models)} models available to this key:")
        for m in models:
            print(f" - {m['id']} ({m.get('display_name', 'No Name')})")
    else:
        print(f"⚠️ Failed to list models via API: {response.status_code} - {response.text}")

except Exception as e:
    print(f"❌ Error: {e}")
