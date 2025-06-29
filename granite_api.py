import json
import os
import requests
import pandas as pd

API_KEY = os.getenv("IBM_CLOUD_APIKEY", "eyJraWQiOiIyMDE5MDcyNCIsImFsZyI6IlJTMjU2In0.eyJpYW1faWQiOiJJQk1pZC02OTEwMDBaRVBRIiwiaWQiOiJJQk1pZC02OTEwMDBaRVBRIiwicmVhbG1pZCI6IklCTWlkIiwianRpIjoiMzIyNzgwYjEtYjAxMi00ODJlLWIxY2MtMTNiMGU2M2FjYzM5IiwiaWRlbnRpZmllciI6IjY5MTAwMFpFUFEiLCJnaXZlbl9uYW1lIjoiWXVlcWluIiwiZmFtaWx5X25hbWUiOiJMaSIsIm5hbWUiOiJZdWVxaW4gTGkiLCJlbWFpbCI6ImFteWxlZS5seXFAZ21haWwuY29tIiwic3ViIjoiYW15bGVlLmx5cUBnbWFpbC5jb20iLCJhdXRobiI6eyJzdWIiOiJhbXlsZWUubHlxQGdtYWlsLmNvbSIsImlhbV9pZCI6IklCTWlkLTY5MTAwMFpFUFEiLCJuYW1lIjoiWXVlcWluIExpIiwiZ2l2ZW5fbmFtZSI6Ill1ZXFpbiIsImZhbWlseV9uYW1lIjoiTGkiLCJlbWFpbCI6ImFteWxlZS5seXFAZ21haWwuY29tIn0sImFjY291bnQiOnsidmFsaWQiOnRydWUsImJzcyI6IjViNmYzZDcwMWYwZjRlZGRhODZmOTc2MTg3NzM4NTI3IiwiaW1zX3VzZXJfaWQiOiIxMzk0MzQzMyIsImZyb3plbiI6dHJ1ZSwiaW1zIjoiMjk5OTU5NiJ9LCJtZmEiOnsiaW1zIjp0cnVlfSwiaWF0IjoxNzUxMTk0MzgxLCJleHAiOjE3NTExOTc5ODEsImlzcyI6Imh0dHBzOi8vaWFtLmNsb3VkLmlibS5jb20vaWRlbnRpdHkiLCJncmFudF90eXBlIjoidXJuOmlibTpwYXJhbXM6b2F1dGg6Z3JhbnQtdHlwZTphcGlrZXkiLCJzY29wZSI6ImlibSBvcGVuaWQiLCJjbGllbnRfaWQiOiJkZWZhdWx0IiwiYWNyIjoxLCJhbXIiOlsicHdkIl19.ca4L0KWmi-GWMeeOo-D7ADIJpbOY_ayYf2catIta-BSOIfyVKDG-tOh91gAsfCS4sUnt1UGjyIhluhhqTDXt-plnOjkpEmSB-a-TJIRinK1g0xaDFTuyBm9WtiB2GpGzw-jk6VrteMSPQ8NaHjhcTvtp7Ic2cd8H2Nbol53CDzOE6nyvGTmOdRL7dacZNR3n97VH4nREfkB_hXJGCstf4e0q1ZfiJQIGpK36KOd9S2kQwsfPPnSfnY7CH8_BESWjhgIn8lCHDxi2qgm-Jc7w_mVP_4IGings7u_iJ9V_FM0ALeFyhl9yDyVlePWaMwlldYP2F4ayQkKcRX0P_tjF8A")
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