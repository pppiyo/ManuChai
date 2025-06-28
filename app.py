import streamlit as st
from granite_api import call_granite

st.set_page_config(page_title="Business Chatbot", page_icon="🤖")
st.title("🤖 ManuChai (IBM Granite)")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Ask a question:")

if user_input:
    prompt = f"""
    You are a business assistant. Please answer in this JSON format:
    {{
      "answer": "...",
      "suggestion": "..."
    }}

    Customer question: {user_input}
    """
    bot_response = call_granite(prompt)
    st.session_state.chat_history.append(("User", user_input))
    st.session_state.chat_history.append(("Bot", bot_response))

# Display history
for speaker, msg in st.session_state.chat_history:
    st.markdown(f"**{speaker}**: {msg}")