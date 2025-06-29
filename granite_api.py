import json
import os
import requests
import pandas as pd

API_KEY = os.getenv("IBM_CLOUD_APIKEY", "eyJraWQiOiIyMDE5MDcyNCIsImFsZyI6IlJTMjU2In0.eyJpYW1faWQiOiJJQk1pZC02OTEwMDBaRVBRIiwiaWQiOiJJQk1pZC02OTEwMDBaRVBRIiwicmVhbG1pZCI6IklCTWlkIiwianRpIjoiOTRhNTI0ODUtNDljZS00NGExLWIzNTEtNDIwMjI0MTI2ZDczIiwiaWRlbnRpZmllciI6IjY5MTAwMFpFUFEiLCJnaXZlbl9uYW1lIjoiWXVlcWluIiwiZmFtaWx5X25hbWUiOiJMaSIsIm5hbWUiOiJZdWVxaW4gTGkiLCJlbWFpbCI6ImFteWxlZS5seXFAZ21haWwuY29tIiwic3ViIjoiYW15bGVlLmx5cUBnbWFpbC5jb20iLCJhdXRobiI6eyJzdWIiOiJhbXlsZWUubHlxQGdtYWlsLmNvbSIsImlhbV9pZCI6IklCTWlkLTY5MTAwMFpFUFEiLCJuYW1lIjoiWXVlcWluIExpIiwiZ2l2ZW5fbmFtZSI6Ill1ZXFpbiIsImZhbWlseV9uYW1lIjoiTGkiLCJlbWFpbCI6ImFteWxlZS5seXFAZ21haWwuY29tIn0sImFjY291bnQiOnsidmFsaWQiOnRydWUsImJzcyI6IjViNmYzZDcwMWYwZjRlZGRhODZmOTc2MTg3NzM4NTI3IiwiaW1zX3VzZXJfaWQiOiIxMzk0MzQzMyIsImZyb3plbiI6dHJ1ZSwiaW1zIjoiMjk5OTU5NiJ9LCJtZmEiOnsiaW1zIjp0cnVlfSwiaWF0IjoxNzUxMTk4MjIzLCJleHAiOjE3NTEyMDE4MjMsImlzcyI6Imh0dHBzOi8vaWFtLmNsb3VkLmlibS5jb20vaWRlbnRpdHkiLCJncmFudF90eXBlIjoidXJuOmlibTpwYXJhbXM6b2F1dGg6Z3JhbnQtdHlwZTphcGlrZXkiLCJzY29wZSI6ImlibSBvcGVuaWQiLCJjbGllbnRfaWQiOiJkZWZhdWx0IiwiYWNyIjoxLCJhbXIiOlsicHdkIl19.eSXfhKcu-UEV5RAu-QbjFbRhpmtBHz5PSALCCatoO57sVdQ0LntARFVVXzVlgrvu3b7rJZBXx3094W8_Iz4toDDVcBXKEdcV50lfKQfYZIxOAuDEmHEn2czUKaF_6wSQjcO1HKv9c4chAvVm46xWQZO2WUnrk3qU9iu7m91nj1uMJWKKzRvmghX-cWAQPlr363iWII9m_gNvrl7aqrkp_PhKttf1VHTWqaDsWucoosJ_IxmGoE1wyQemw3ZU_KWYPvYT1JGdHnIYWWpiP8Ki0cb8k3nrVsCbNnNc0XSEmAEEFdRlQV5-qIEknYVpnP5uCyailu8JHGS0gZpq7JfsnA")
ENDPOINT = os.getenv("GRANITE_CHAT_URL", "https://us-south.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29")
PROJECT_ID = os.getenv("WATSONX_PROJECT_ID", "0d2579c2-c1e9-4cdf-8a4d-b1b85f3fafff")
MODEL_ID = "ibm/granite-3-3-8b-instruct"

def call_granite(product_name, delivery_address, quantity):
    try:
        df = pd.read_csv("data.csv", sep="\t")
        df.columns = df.columns.str.strip()
        context = df.to_string(index=False)
    except Exception as e:
        context = f"[Failed to load CSV: {str(e)}]"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    body = {
            "project_id": f"{PROJECT_ID}",
            "model_id": "ibm/granite-3-3-8b-instruct",
            "messages": [{
            "role": "user",
            "content": [{
                "type": "text",
                "text": f"""
                
                <|system|>
                You are a logistics and cost estimation expert. Based on customer input and reference data, calculate the most cost-efficient shipping method, shipping price, product price, and total cost.

                <|user|>
                **Customer Order:**
                - Product: {product_name}
                - Quantity: {quantity}
                - Destination: {delivery_address}
                - Origin: Dallas, Texas

                **Reference Data:**
                - **Unit Prices:** {{
                "Tank": 800000,
                "Heat Exchanger": 6000000,
                "Pump": 700000,
                "Air Cooler": 50000,
                "Compressor": 700000
                }}

                - **Shipping Info:**
                * Distance: 1550 miles
                * Diesel: $3.80/gal, 5 mpg
                * Driver Wage: $0.60/mile
                * Operating Cost: $350/day
                * Profit Margin: 18%
                * FCA: Buyer arranges main carriage
                * FOB: Add 2% admin fee on shipping

                **Task:**

                1.  **Calculate Shipping Price for FCA:** Determine the estimated shipping cost under FCA Incoterms, detailing the components like fuel, driver wages, truck operating costs, tolls, and profit margin.
                2.  **Calculate Shipping Price for FOB:** Determine the estimated shipping cost under FOB Incoterms, applying the specific cost implication mentioned above, and detailing components.
                3.  **Determine Optimized Shipping Method:** Compare the calculated FCA and FOB shipping prices and select the method with the lower cost. This will be the "optimized shipping method."
                4.  **Calculate Product Price:** Use the 'Quantity' from the customer order and the 'Product Unit Price Table' to find the total product cost.
                5.  **Calculate Total Cost:** Sum the "Optimized Shipping Price" and the "Product Price."

                ---

                **Strict Output Format (JSON):**

                ```json
                {{
                "optimized_shipping_method": "text",
                "shipping_price": int,
                "product_price": int,
                "total_cost": int,
                "shipping_price_explanation": "text"
                }}

                """
                    }]
                }],
            "frequency_penalty": 0,
            "max_tokens": 5000,
            "presence_penalty": 0,
            "temperature": 0,
            "top_p": 1
        }

    try:
        response = requests.post(ENDPOINT, headers=headers, json=body, timeout=100)

        if response.status_code != 200:
            print(f"[Granite API error {response.status_code}]: {response.text}")
            return "[Error from Granite API]"

        data = response.json()
        print(f"[Granite API response]: {data}")
        # print(f"[Granite API response]: {data}")
        # Extract the assistant's reply content from the response
        content_str = data["choices"][0]["message"]["content"]

        # Locate the JSON block inside the content string
        json_start = content_str.index("```json") + len("```json")
        json_end = content_str.index("```", json_start)
        json_block = content_str[json_start:json_end].strip()

        # Parse the JSON block into a dictionary
        parsed = json.loads(json_block)

        # Extract the required fields
        shipping_price_explanation = parsed["shipping_price_explanation"]
        product_price = parsed["product_price"]
        shipping_price = parsed["shipping_price"]
        total_cost = parsed["total_cost"]

        total_cost = product_price + shipping_price

        return shipping_price_explanation, product_price, shipping_price, total_cost

    except Exception as e:
        print(f"[Exception]: {e}")
        return "[Failed to connect to Granite]"

def call_granite_chat(user_message, company_name=None):
    """
    Call Granite LLM for general chat interactions.
    
    Args:
        user_message: The user's message
        company_name: Optional company name for context
    
    Returns:
        str: The bot's response
    """
    try:
        # Load context data if available
        try:
            df = pd.read_csv("data.csv", sep="\t")
            df.columns = df.columns.str.strip()
            context = df.to_string(index=False)
        except Exception as e:
            context = f"[No reference data available: {str(e)}]"

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }

        # Create a more general prompt for chat
        prompt = f"""
        <|system|>
        You are ManuChai, a helpful AI assistant for manufacturing and logistics companies. 
        You provide expert advice on manufacturing processes, logistics, cost estimation, 
        and general business questions. Be professional, helpful, and concise in your responses.
        
        {f"Company Context: {company_name}" if company_name else ""}
        
        <|user|>
        {user_message}
        """

        body = {
            "project_id": f"{PROJECT_ID}",
            "model_id": "ibm/granite-3-3-8b-instruct",
            "messages": [{
                "role": "user",
                "content": [{
                    "type": "text",
                    "text": prompt
                }]
            }],
            "frequency_penalty": 0,
            "max_tokens": 2000,
            "presence_penalty": 0,
            "temperature": 0.7,
            "top_p": 1
        }

        response = requests.post(ENDPOINT, headers=headers, json=body, timeout=30)

        if response.status_code != 200:
            print(f"[Granite API error {response.status_code}]: {response.text}")
            return "I apologize, but I'm having trouble connecting to my knowledge base right now. Please try again later."

        data = response.json()
        print(f"[Granite Chat API response]: {data}")
        
        # Extract the assistant's reply content from the response
        content = data["choices"][0]["message"]["content"]
        return content

    except Exception as e:
        print(f"[Chat Exception]: {e}")
        return "I apologize, but I encountered an error while processing your request. Please try again."