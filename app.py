import streamlit as st
import json
from granite_api import call_granite
import pandas as pd

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

# History orders
orders_options = []

df = pd.read_csv("data.csv", sep="\t")
df.columns = df.columns.str.strip()
matched_rows = df[df["business_name"].str.contains(st.session_state.company, case=False, na=False)]
if matched_rows.empty:
    orders_options = [f"No matching data found for {st.session_state.company}."]
else:
    for index, row in matched_rows.iterrows():
        order_info = f"{row['product_name']} - {row['component_name']} - {row['order_date']} - {row['order_status']}"
        orders_options.append(order_info)
    
# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Clear conversation button
if st.button("🗑️ Clear Conversation"):
    st.session_state.chat_history = []

# Chat input form
with st.form(key="chat_form"):
    selected_faq = st.selectbox("📋 History orders query:", [""] + orders_options, key="faq")
    user_input = st.text_input("💬 Or ask your own question:", key="custom")
    submitted = st.form_submit_button("🚀 Send")

# Determine input source
final_input = None
if submitted:
    if user_input.strip():
        final_input = user_input.strip()
    elif selected_faq:
        final_input = selected_faq + " Please provide more details for this order."

# Process input
if final_input:
    bot_response = call_granite(st.session_state.company, final_input)
    st.session_state.chat_history.append(("User", final_input))

    try:
        response_data = json.loads(bot_response)
        answer = response_data.get("answer", "[No answer]")
        suggestion = response_data.get("suggestion", "[No suggestion]")
        st.session_state.chat_history.append(("Bot", answer))
        st.session_state.chat_history.append(("Bot-suggestion", suggestion))
    except json.JSONDecodeError:
        st.session_state.chat_history.append(("Bot", bot_response))

# Display conversation
for speaker, msg in st.session_state.chat_history:
    if speaker == "User":
        st.markdown(f"**🧑 You:** {msg}")
    elif speaker == "Bot":
        st.markdown(f"**🤖 Answer:** {msg}")
    elif speaker == "Bot-suggestion":
        st.info(f"💡 Suggestion: {msg}")