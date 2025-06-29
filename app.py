import streamlit as st
import pandas as pd
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
    explanation, product_price, shipment_price, total_cost = call_granite(
        product_name, delivery_address, quantity
    )

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

# Display conversation
for speaker, msg in st.session_state.chat_history:
    if speaker == "User":
        st.markdown(f"**🧑 You:** {msg}")
    elif speaker == "Bot":
        st.markdown(f"**🤖 Explanation:** {msg}")
    elif speaker == "Table":
        df = pd.DataFrame([msg])
        st.table(df)