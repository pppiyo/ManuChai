import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
from granite_api import call_granite

# Set page config
st.set_page_config(page_title="ManuChai", page_icon="🤖")
st.title("🤖 ManuChai (IBM Granite Chatbot)")

# Ask for company name at the beginning
if "company" not in st.session_state:
    st.session_state.company = None

if st.session_state.company is None:
    st.title("🏢 Welcome to ManuChai")
    company = st.text_input("Please enter your company name:")
    if company:
        st.session_state.company = company
        st.rerun()
    st.stop()

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Clear conversation
if st.button("🗑️ Clear Conversation"):
    st.session_state.chat_history = []

# Input form
with st.form(key="quote_form"):
    st.subheader("📦 Request a Product Quote")
    product_name = st.text_input("Product Name")
    delivery_address = st.text_input("Delivery Address")
    quantity = st.number_input("Quantity", min_value=1, step=1)
    submitted = st.form_submit_button("🚀 Send")

# On submit
if submitted:
    # Store input
    user_msg = f"Product: {product_name}, Address: {delivery_address}, Quantity: {quantity}"
    st.session_state.chat_history.append(("User", user_msg))

    # Get response
    res = call_granite(
        product_name, delivery_address, quantity
    )
    if len(res) == 4:
        explanation, product_price, shipment_price, total_cost = res
    else:
        explanation = res[0]
        product_price = shipment_price = total_cost = 0.0

    # Create table as dict (for consistent rendering later)
    table_data = {
        "Company": st.session_state.company,
        "Product": product_name,
        "Delivery Address": delivery_address,
        "Quantity": quantity,
        "Product Price": f"${product_price:.2f}",
        "Shipment Price": f"${shipment_price:.2f}",
        "Total Cost": f"${total_cost:.2f}"
        # "Product Price": -1,
        # "Shipment Price": -1,
        # "Total Cost": -1
    }

    # Save to chat history
    st.session_state.chat_history.append(("Bot", explanation))
    st.session_state.chat_history.append(("Table", table_data))

    # Save to order history JSON file
    if save_to_order_history(table_data):
        st.success("✅ Quote data saved to order history!")

# Display conversation
for speaker, msg in st.session_state.chat_history:
    if speaker == "User":
        st.markdown(f"**🧑 You:** {msg}")
    elif speaker == "Bot":
        st.markdown(f"**🤖 Explanation:** {msg}")
    elif speaker == "Table":
        df = pd.DataFrame([msg])
        st.table(df)

def save_to_order_history(data):
    """
    Save JSON data to order_history.json file by appending to existing array.
    
    Args:
        data: The data to save (dict, list, or any JSON-serializable object)
    
    Returns:
        bool: True if successful, False otherwise
    """
    filename = "order_history.json"
    
    try:
        # Read existing data if file exists
        existing_data = []
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    file_content = f.read().strip()
                    if file_content:  # Check if file is not empty
                        existing_data = json.load(f)
                    else:
                        existing_data = []
            except json.JSONDecodeError:
                # If file is corrupted, start fresh
                existing_data = []
        
        # Add timestamp to the data
        data_with_timestamp = {
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        
        # Append new data to existing array
        existing_data.append(data_with_timestamp)
        
        # Write back to file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=2, ensure_ascii=False)
        
        return True
        
    except Exception as e:
        st.error(f"Error saving to order history: {str(e)}")
        return False


                