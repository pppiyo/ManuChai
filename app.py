import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
from granite_api import call_granite, call_granite_chat

def save_to_order_history(data):
    """
    Save JSON data to order_history.json file by appending to existing array.
    
    Args:
        data: The data to save (dict, list, or any JSON-serializable object)
    
    Returns:
        bool: True if successful, False otherwise
    """
    filename = "order_history.json"
    existing_data = []
    
    try:
        # Read existing data if file exists
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    file_content = f.read().strip()
                    if file_content:  # Check if file is not empty
                        existing_data = json.loads(file_content)
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

# Initialize chatbot history
if "chatbot_history" not in st.session_state:
    st.session_state.chatbot_history = []

# Create tabs
tab1, tab2 = st.tabs(["📦 Product Quote", "💬 Chat with Bot"])

with tab1:
    st.subheader("📦 Request a Product Quote")
    
    # Clear conversation
    if st.button("🗑️ Clear Chat History", key="clear_quote_history"):
        st.session_state.chat_history = []

    # Input fields (outside form to remove "press enter to submit" prompt)
    product_name = st.text_input("Product Name *", key="product_name_input", placeholder="Enter product name")
    delivery_address = st.text_input("Delivery Address *", key="delivery_address_input", placeholder="Enter delivery address")
    quantity = st.number_input("Quantity", min_value=1, step=1, key="quantity_input")
    
    # Submit button
    submitted = st.button("🚀 Send Quote", key="submit_quote", use_container_width=True)

    # On submit
    if submitted:
        # Validate required fields
        if not product_name.strip():
            st.error("❌ Product Name is required!")
        elif not delivery_address.strip():
            st.error("❌ Delivery Address is required!")
        else:
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

with tab2:
    st.subheader("💬 Chat with ManuChai")
    
    # Clear chatbot conversation
    if st.button("🗑️ Clear Chat History", key="clear_chatbot_history"):
        st.session_state.chatbot_history = []
    
    # Chat input
    user_message = st.text_input("Type your message here:", key="chat_input")
    
    if st.button("🚀 Send", key="send_chat"):
        if user_message.strip():
            # Add user message to history
            st.session_state.chatbot_history.append({"role": "user", "content": user_message})
            
            # Get bot response from Granite API
            bot_response = call_granite_chat(user_message, st.session_state.company)
            
            # Add bot response to history
            st.session_state.chatbot_history.append({"role": "assistant", "content": bot_response})
            
            # Clear the input
            st.rerun()
    
    # Display chat history
    for message in st.session_state.chatbot_history:
        if message["role"] == "user":
            st.markdown(f"**🧑 You:** {message['content']}")
        else:
            st.markdown(f"**🤖 ManuChai:** {message['content']}")
    
    # Show placeholder if no messages
    if not st.session_state.chatbot_history:
        st.info("💡 Start a conversation by typing a message above!")
               