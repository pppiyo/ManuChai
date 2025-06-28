import os
import requests

API_KEY = os.getenv("IBM_CLOUD_APIKEY")
ENDPOINT = os.getenv("GRANITE_URL")
MODEL_ID = "granite-13b-chat"

def call_granite(prompt: str) -> str:
    payload = {
        "model_id": MODEL_ID, 
        "input": prompt
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(ENDPOINT, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        result = response.json()
        return result.get("generated_text", "[No response from model]")
    
    except requests.exceptions.RequestException as e:
        print(f"[Granite API error] {e}")
        return "[Unable to connect to Granite API]"
    
    except Exception as e:
        print(f"[Unexpected error] {e}")
        return "[Unexpected error occurred]"