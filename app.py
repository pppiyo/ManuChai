import streamlit as st
from granite_api import call_granite

st.set_page_config(page_title="ManuChai", page_icon="🤖")
st.title("🤖 ManuChai (IBM Granite)")

# Define FAQ options
faq_options = [
    "What are your opening hours?",
    "Do you offer delivery?",
    "How much does shipping cost?"
]

# Let user pick a FAQ question
selected_faq = st.selectbox("📋 Choose a frequently asked question:", [""] + faq_options)

# Text input box (fallback / custom questions)
user_input = st.text_input("Or ask your own question:")

# Determine the actual question to send
final_input = selected_faq if selected_faq else user_input

# Initialize history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Call Granite if a question is selected or entered
if final_input:
    prompt = f"""
    You are a business assistant. Please answer in this JSON format:
    {{
      "answer": "...",
      "suggestion": "..."
    }}

    Customer question: {final_input}
    """
    bot_response = call_granite(prompt)
    st.session_state.chat_history.append(("User", final_input))
    st.session_state.chat_history.append(("Bot", bot_response))

# Display history
for speaker, msg in st.session_state.chat_history:
    st.markdown(f"**{speaker}**: {msg}")