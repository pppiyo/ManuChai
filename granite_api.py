import os
import requests
import pandas as pd

API_KEY = os.getenv("IBM_CLOUD_APIKEY", "eyJraWQiOiIyMDE5MDcyNCIsImFsZyI6IlJTMjU2In0.eyJpYW1faWQiOiJJQk1pZC02OTQwMDBaRFpFIiwiaWQiOiJJQk1pZC02OTQwMDBaRFpFIiwicmVhbG1pZCI6IklCTWlkIiwianRpIjoiODQwY2U4ODktMmM0MS00ZTFlLThmZjAtMDE5MTA1NDQxMmQwIiwiaWRlbnRpZmllciI6IjY5NDAwMFpEWkUiLCJnaXZlbl9uYW1lIjoiWXV5aW5nIiwiZmFtaWx5X25hbWUiOiJMdSIsIm5hbWUiOiJZdXlpbmcgTHUiLCJlbWFpbCI6Inl1eWluZ2x1QHVzYy5lZHUiLCJzdWIiOiJ5dXlpbmdsdUB1c2MuZWR1IiwiYXV0aG4iOnsic3ViIjoieXV5aW5nbHVAdXNjLmVkdSIsImlhbV9pZCI6IklCTWlkLTY5NDAwMFpEWkUiLCJuYW1lIjoiWXV5aW5nIEx1IiwiZ2l2ZW5fbmFtZSI6Ill1eWluZyIsImZhbWlseV9uYW1lIjoiTHUiLCJlbWFpbCI6Inl1eWluZ2x1QHVzYy5lZHUifSwiYWNjb3VudCI6eyJ2YWxpZCI6dHJ1ZSwiYnNzIjoiY2E1NmQwNWY4NmI5NGY2YzgwNmVjYzY5MmZhODI3N2EiLCJpbXNfdXNlcl9pZCI6IjEzOTQzNDM3IiwiZnJvemVuIjp0cnVlLCJpbXMiOiIyOTk5NzcwIn0sIm1mYSI6eyJpbXMiOnRydWV9LCJpYXQiOjE3NTExNzQ1OTksImV4cCI6MTc1MTE3ODE5OSwiaXNzIjoiaHR0cHM6Ly9pYW0uY2xvdWQuaWJtLmNvbS9pZGVudGl0eSIsImdyYW50X3R5cGUiOiJ1cm46aWJtOnBhcmFtczpvYXV0aDpncmFudC10eXBlOmFwaWtleSIsInNjb3BlIjoiaWJtIG9wZW5pZCIsImNsaWVudF9pZCI6ImRlZmF1bHQiLCJhY3IiOjEsImFtciI6WyJwd2QiXX0.CzQIRd22vJ3moPTT4W4g5jZ58yRWQn0dg4-NvntX0KZXmfYaRu-4wLB46vk69emF49qTZc9AqBuGVvP7ejeVk6hCUqwnYKmC7_nhATcxT23bfuZ0_al7Mlfai49AktG9ofZ8iCtvbjvZ8P9tyRXQCIzj6ZXNSK9bdjDK3XUR57T_-btejPJCBR2oiAevErEfSJHcltnOrOrawFECoWsplrBhJvdq717naV7rA_0nAlJYq07jvjOLl2oxVCttpPc3tzmC9QVKohowaT_pUU1bG8YBkDQ12CynjBJacUEHsP8QCyF5Lyi9RlR-0sqKL3txwr9mWx6WjTSFL4M7Cqp-pw")
ENDPOINT = os.getenv("GRANITE_CHAT_URL", "https://us-south.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29")
PROJECT_ID = os.getenv("WATSONX_PROJECT_ID", "7d920a6b-64e4-454b-831f-c1d4d07d8f8c")
MODEL_ID = "ibm/granite-3-3-8b-instruct"

def call_granite(product_name, delivery_address, quantity):
    explanation = "lalala"
    product_price = 100.0  # Example price for the product
    shipment_price = 20.0  # Example shipment price
    total_cost = product_price + shipment_price
    return explanation, product_price, shipment_price, total_cost

# def call_granite(business_name: str, user_question: str) -> str:
    # try:
    #     df = pd.read_csv("data.csv", sep="\t")
    #     df.columns = df.columns.str.strip()
    #     context = df.to_string(index=False)
    #     # matched_rows = df[df["business_name"].str.contains(business_name, case=False, na=False)]
    #     # if matched_rows.empty:
    #     #     context = "No matching data found for this company."
    #     # else:
    #     #     context = matched_rows.head(5).to_string(index=False)
    # except Exception as e:
    #     context = f"[Failed to load CSV: {str(e)}]"

    # prompt = f"""
    #         You are a business assistant. Use the following company and data to help answer the question.

    #         Company Name: {business_name}
    #         data: {context}

    #         Please answer in this JSON format:
    #         {{
    #         "answer": "...",
    #         "suggestion": "..."
    #         }}

    #         Customer question: {user_question}
    #         """
    # print(f"[Granite API request]: {prompt}")

    # headers = {
    #     "Accept": "application/json",
    #     "Content-Type": "application/json",
    #     "Authorization": f"Bearer {API_KEY}"
    # }

    # body = {
    #     "project_id": PROJECT_ID,
    #     "model_id": MODEL_ID,
    #     "messages": [
    #         {
    #             "role": "user",
    #             "content": [{"type": "text", "text": prompt}]
    #         }
    #     ],
    #     "temperature": 0.7,
    #     "max_tokens": 1000,
    #     "top_p": 1,
    #     "frequency_penalty": 0,
    #     "presence_penalty": 0
    # }

    # try:
    #     response = requests.post(ENDPOINT, headers=headers, json=body, timeout=10)

    #     if response.status_code != 200:
    #         print(f"[Granite API error {response.status_code}]: {response.text}")
    #         return "[Error from Granite API]"

    #     data = response.json()
    #     print(f"[Granite API response]: {data}")
    #     return data.get("choices", [{}])[0].get("message", {}).get("content", "[No response]")

    # except Exception as e:
    #     print(f"[Exception]: {e}")
    #     return "[Failed to connect to Granite]"