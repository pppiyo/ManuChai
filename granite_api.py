import os
import requests

API_KEY = os.getenv("IBM_CLOUD_APIKEY", "eyJraWQiOiIyMDE5MDcyNCIsImFsZyI6IlJTMjU2In0.eyJpYW1faWQiOiJJQk1pZC02OTMwMDBaSTM4IiwiaWQiOiJJQk1pZC02OTMwMDBaSTM4IiwicmVhbG1pZCI6IklCTWlkIiwianRpIjoiODBhM2NjNTgtZTc4YS00ZjM4LThkMzYtNjY4NDI4ZjA2MGIzIiwiaWRlbnRpZmllciI6IjY5MzAwMFpJMzgiLCJnaXZlbl9uYW1lIjoiSmVzc2llIiwiZmFtaWx5X25hbWUiOiJXYW5nIiwibmFtZSI6Ikplc3NpZSBXYW5nIiwiZW1haWwiOiJqZXNzaWV3YW5nMDUxM0BnbWFpbC5jb20iLCJzdWIiOiJqZXNzaWV3YW5nMDUxM0BnbWFpbC5jb20iLCJhdXRobiI6eyJzdWIiOiJqZXNzaWV3YW5nMDUxM0BnbWFpbC5jb20iLCJpYW1faWQiOiJJQk1pZC02OTMwMDBaSTM4IiwibmFtZSI6Ikplc3NpZSBXYW5nIiwiZ2l2ZW5fbmFtZSI6Ikplc3NpZSIsImZhbWlseV9uYW1lIjoiV2FuZyIsImVtYWlsIjoiamVzc2lld2FuZzA1MTNAZ21haWwuY29tIn0sImFjY291bnQiOnsidmFsaWQiOnRydWUsImJzcyI6IjJlMjI1YTZmZmJjMTQ5MGI5NzhjOGJiNGRkMjY3OGI0IiwiaW1zX3VzZXJfaWQiOiIxMzk0NTE3NSIsImZyb3plbiI6dHJ1ZSwiaW1zIjoiMzAwMDIxOCJ9LCJtZmEiOnsiaW1zIjp0cnVlfSwiaWF0IjoxNzUxMTY2Mjc3LCJleHAiOjE3NTExNjk4NzcsImlzcyI6Imh0dHBzOi8vaWFtLmNsb3VkLmlibS5jb20vaWRlbnRpdHkiLCJncmFudF90eXBlIjoidXJuOmlibTpwYXJhbXM6b2F1dGg6Z3JhbnQtdHlwZTphcGlrZXkiLCJzY29wZSI6ImlibSBvcGVuaWQiLCJjbGllbnRfaWQiOiJkZWZhdWx0IiwiYWNyIjoxLCJhbXIiOlsicHdkIl19.BJMoveMM4vo4Bvt2iwjiErQnmQ6IbyBgJwRlKsVupWVSm1F2hG0WcwosLULvmEmcXvrdp5JwY8FsPrGMDGiWfxqptsi3hpclNgTWcFSW_MVfiXzHk_EWBSyojAqp_wSu0EGZbIpbVJWLQjAmwY1T2QLo3rlp-He_nI0O0gmgJJWdtxL4kX4flR8TNixAWolo5KqicM2dZ1oE9Df-clNTT8eIVfRRYfye4DDjDsCjU5ldBc_RZEtEhfU9TjZXZcnsr8VM8Z7CganuygUBJeJpdplSSw4i2Vkw1Ra2o9LhWgsUgauqK5HJK_nZy5vkqhjB3HBBwth-YploRHWstp1d3w")
ENDPOINT = os.getenv("GRANITE_CHAT_URL", "https://us-south.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29")
PROJECT_ID = os.getenv("WATSONX_PROJECT_ID", "419929ef-9d76-4999-81f6-0ed54c923e77")
MODEL_ID = "ibm/granite-3-3-8b-instruct"

def call_granite(prompt: str) -> str:
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    body = {
        "project_id": PROJECT_ID,
        "model_id": MODEL_ID,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}]
            }
        ],
        "temperature": 0.7,
        "max_tokens": 1000,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0
    }

    try:
        response = requests.post(ENDPOINT, headers=headers, json=body, timeout=10)

        if response.status_code != 200:
            print(f"[Granite API error {response.status_code}]: {response.text}")
            return "[Error from Granite API]"

        data = response.json()
        print(f"[Granite API response]: {data}")
        return data.get("generated_text", "[No response]")

    except Exception as e:
        print(f"[Exception]: {e}")
        return "[Failed to connect to Granite]"