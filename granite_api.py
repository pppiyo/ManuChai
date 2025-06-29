import os
import requests

API_KEY = os.getenv("IBM_CLOUD_APIKEY", "eyJraWQiOiIyMDE5MDcyNCIsImFsZyI6IlJTMjU2In0.eyJpYW1faWQiOiJJQk1pZC02OTQwMDBaRFpFIiwiaWQiOiJJQk1pZC02OTQwMDBaRFpFIiwicmVhbG1pZCI6IklCTWlkIiwianRpIjoiOWEzZWFjYzYtMzAwNC00ODY5LWI3OTktNDc4MTg0YTAwYjQwIiwiaWRlbnRpZmllciI6IjY5NDAwMFpEWkUiLCJnaXZlbl9uYW1lIjoiWXV5aW5nIiwiZmFtaWx5X25hbWUiOiJMdSIsIm5hbWUiOiJZdXlpbmcgTHUiLCJlbWFpbCI6Inl1eWluZ2x1QHVzYy5lZHUiLCJzdWIiOiJ5dXlpbmdsdUB1c2MuZWR1IiwiYXV0aG4iOnsic3ViIjoieXV5aW5nbHVAdXNjLmVkdSIsImlhbV9pZCI6IklCTWlkLTY5NDAwMFpEWkUiLCJuYW1lIjoiWXV5aW5nIEx1IiwiZ2l2ZW5fbmFtZSI6Ill1eWluZyIsImZhbWlseV9uYW1lIjoiTHUiLCJlbWFpbCI6Inl1eWluZ2x1QHVzYy5lZHUifSwiYWNjb3VudCI6eyJ2YWxpZCI6dHJ1ZSwiYnNzIjoiY2E1NmQwNWY4NmI5NGY2YzgwNmVjYzY5MmZhODI3N2EiLCJpbXNfdXNlcl9pZCI6IjEzOTQzNDM3IiwiZnJvemVuIjp0cnVlLCJpbXMiOiIyOTk5NzcwIn0sIm1mYSI6eyJpbXMiOnRydWV9LCJpYXQiOjE3NTExNzA4MTksImV4cCI6MTc1MTE3NDQxOSwiaXNzIjoiaHR0cHM6Ly9pYW0uY2xvdWQuaWJtLmNvbS9pZGVudGl0eSIsImdyYW50X3R5cGUiOiJ1cm46aWJtOnBhcmFtczpvYXV0aDpncmFudC10eXBlOmFwaWtleSIsInNjb3BlIjoiaWJtIG9wZW5pZCIsImNsaWVudF9pZCI6ImRlZmF1bHQiLCJhY3IiOjEsImFtciI6WyJwd2QiXX0.jTcsJpiyuNOr4IPOa9wycV637T9t9iOOJUD8lIRKygsAOmSXKuuscAqaOXTglYlVFy25_ONgOlhXzgFSDSbstDxnFZt4QlPFeRPXRvmzg6t7rkSL0YAhqUl97pRQgcLeccoU13p7APEVHqxdxcTAVju9Cz-NfYHBxjkuhlnguroDrtJAsP30ZDNYP08EXDhAaKhUWURck1RmQXMrUBsUacHFDD6S6v3URihtwK-b3HyXD4zkBLvq25naxD8dSUcG_Us-XoRLewHNVpUIVr7MC7YjJS42AlL_0zvV_4enDZznyBXY1cXNacf9n3E02G_U9jB4o0hNBhjc7CSlLf2PaA")
ENDPOINT = os.getenv("GRANITE_CHAT_URL", "https://us-south.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29")
PROJECT_ID = os.getenv("WATSONX_PROJECT_ID", "7d920a6b-64e4-454b-831f-c1d4d07d8f8c")
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
        return data.get("choices", [{}])[0].get("message", {}).get("content", "[No response]")

    except Exception as e:
        print(f"[Exception]: {e}")
        return "[Failed to connect to Granite]"