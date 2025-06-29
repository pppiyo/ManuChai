import streamlit as st
import json
from granite_api import call_granite

# Set page title and icon
st.set_page_config(page_title="ManuChai", page_icon="🤖")
st.title("🤖 ManuChai (IBM Granite Chatbot)")

# Define FAQ options
faq_options = [
    "What are your opening hours?",
    "Do you offer delivery?",
    "How much does shipping cost?"
]

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# FAQ selection dropdown
selected_faq = st.selectbox("📋 Choose a frequently asked question:", [""] + faq_options)

# Manual input fallback
user_input = st.text_input("Or ask your own question:")

# Determine actual user question
final_input = selected_faq if selected_faq else user_input

# Send prompt and process response
if final_input and (not st.session_state.chat_history or final_input != st.session_state.chat_history[-1][1]):
    # Construct prompt for structured response
    prompt = f"""
    You are a business assistant. Please answer in this JSON format:
    {{
      "answer": "...",
      "suggestion": "..."
    }}

    Customer question: {final_input}
    """
    
    # Call Granite model
    bot_response = call_granite(prompt)

    # Append user input
    st.session_state.chat_history.append(("User", final_input))

    # Try to parse structured response
    try:
        response_data = json.loads(bot_response)
        answer = response_data.get("answer", "[No answer]")
        suggestion = response_data.get("suggestion", "[No suggestion]")

        st.session_state.chat_history.append(("Bot", answer))
        st.session_state.chat_history.append(("Bot-suggestion", suggestion))
    except json.JSONDecodeError:
        st.session_state.chat_history.append(("Bot", bot_response))

    # Reset FAQ dropdown after asking
    if selected_faq:
        st.experimental_rerun()

# Display full chat history
for speaker, msg in st.session_state.chat_history:
    if speaker == "User":
        st.markdown(f"**🧑 You:** {msg}")
    elif speaker == "Bot":
        st.markdown(f"**🤖 Answer:** {msg}")
    elif speaker == "Bot-suggestion":
        st.info(f"💡 Suggestion: {msg}")