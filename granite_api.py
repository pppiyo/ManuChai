import json
import os
import requests
import pandas as pd

API_KEY = os.getenv("IBM_CLOUD_APIKEY", "eyJraWQiOiIyMDE5MDcyNCIsImFsZyI6IlJTMjU2In0.eyJpYW1faWQiOiJJQk1pZC02OTQwMDBaRFpFIiwiaWQiOiJJQk1pZC02OTQwMDBaRFpFIiwicmVhbG1pZCI6IklCTWlkIiwianRpIjoiYTY4NDk5ZTEtYzA0NC00YWNkLWE2N2EtNjUxOGVmODUxN2EzIiwiaWRlbnRpZmllciI6IjY5NDAwMFpEWkUiLCJnaXZlbl9uYW1lIjoiWXV5aW5nIiwiZmFtaWx5X25hbWUiOiJMdSIsIm5hbWUiOiJZdXlpbmcgTHUiLCJlbWFpbCI6Inl1eWluZ2x1QHVzYy5lZHUiLCJzdWIiOiJ5dXlpbmdsdUB1c2MuZWR1IiwiYXV0aG4iOnsic3ViIjoieXV5aW5nbHVAdXNjLmVkdSIsImlhbV9pZCI6IklCTWlkLTY5NDAwMFpEWkUiLCJuYW1lIjoiWXV5aW5nIEx1IiwiZ2l2ZW5fbmFtZSI6Ill1eWluZyIsImZhbWlseV9uYW1lIjoiTHUiLCJlbWFpbCI6Inl1eWluZ2x1QHVzYy5lZHUifSwiYWNjb3VudCI6eyJ2YWxpZCI6dHJ1ZSwiYnNzIjoiY2E1NmQwNWY4NmI5NGY2YzgwNmVjYzY5MmZhODI3N2EiLCJpbXNfdXNlcl9pZCI6IjEzOTQzNDM3IiwiZnJvemVuIjp0cnVlLCJpbXMiOiIyOTk5NzcwIn0sIm1mYSI6eyJpbXMiOnRydWV9LCJpYXQiOjE3NTExODc2MTYsImV4cCI6MTc1MTE5MTIxNiwiaXNzIjoiaHR0cHM6Ly9pYW0uY2xvdWQuaWJtLmNvbS9pZGVudGl0eSIsImdyYW50X3R5cGUiOiJ1cm46aWJtOnBhcmFtczpvYXV0aDpncmFudC10eXBlOmFwaWtleSIsInNjb3BlIjoiaWJtIG9wZW5pZCIsImNsaWVudF9pZCI6ImRlZmF1bHQiLCJhY3IiOjEsImFtciI6WyJwd2QiXX0.LEUcm5dZRT6wFx4BgGlWKKUwSrA96n2HdWKgeEPyyeGuIF2LETauDsESenOoXrkzzl_5vx1JBmkoiFSDseJlZaiZjzkCgoPepbHxN1hYLXpDcWSciWaDzLXRwPRABuztRjwFEGtZiTlkGnSXbmuWDiUSfKuHUaI61CGUvVpcuU93BKBTqcGvoScl9h01oeIj47bc13JhmbE4kD4qDguNaQ8StS4oSIhtK-f-Kt2MPkpzs21icaabZofNWzaF62DgFBbfwPZL3qJPp_hKhH5o-bKX5DRCb6z7YrZ1Y4dkwuLh6PepN0Xno9uXEDLtDIp_xGAobQJ0HkF-iPbxcVKuGQ")
ENDPOINT = os.getenv("GRANITE_CHAT_URL", "https://us-south.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29")
PROJECT_ID = os.getenv("WATSONX_PROJECT_ID", "7d920a6b-64e4-454b-831f-c1d4d07d8f8c")
MODEL_ID = "ibm/granite-3-3-8b-instruct"

# def call_granite(product_name, delivery_address, quantity):
#     explanation = "lalala"
#     product_price = 100.0  # Example price for the product
#     shipment_price = 20.0  # Example shipment price
#     total_cost = product_price + shipment_price
#     return explanation, product_price, shipment_price, total_cost

def call_granite(product_name, delivery_address, quantity):
    try:
        df = pd.read_csv("data.csv", sep="\t")
        df.columns = df.columns.str.strip()
        context = df.to_string(index=False)
        # matched_rows = df[df["business_name"].str.contains(business_name, case=False, na=False)]
        # if matched_rows.empty:
        #     context = "No matching data found for this company."
        # else:
        #     context = matched_rows.head(5).to_string(index=False)
    except Exception as e:
        context = f"[Failed to load CSV: {str(e)}]"


    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

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