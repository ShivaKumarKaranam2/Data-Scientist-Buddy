
import streamlit as st
import requests
import os


API_KEY = st.secrets["OPENROUTER_API_KEY"]


# 🔐 Your OpenRouter API key (keep this secret!)
API_KEY = "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"  # Replace with your actual API key

# Model ID for DeepSeek Chat via OpenRouter
MODEL_ID = "deepseek/deepseek-r1:free"

# Streamlit page config
st.set_page_config(page_title="Data Scientist Buddy", page_icon="🤖", layout="centered")

# App Title
st.title("🤖 Data Scientist Buddy")
st.markdown("Ask me anything about data science, machine learning, Python, or AI!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful and friendly AI assistant for data science learners. "
                "Answer questions clearly and concisely."
            ),
        }
    ]

# Display chat history
for msg in st.session_state.messages[1:]:  # skip system message
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Ask me a data science question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # API request to OpenRouter
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": MODEL_ID,
                    "messages": st.session_state.messages,
                    "stream": False
                }
            )

            # Handle response
            if response.status_code == 200:
                reply = response.json()["choices"][0]["message"]["content"]
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            else:
                st.error(f"❌ Failed to get response: {response.status_code} - {response.text}")

        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")
