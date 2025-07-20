import streamlit as st
import requests
import time

st.set_page_config(page_title="Data Scientist Buddy", page_icon="🤖")
API_KEY = st.secrets.get("OPENROUTER_API_KEY")
MODEL_ID = "deepseek/deepseek-chat-v3-0324:free"

if not API_KEY:
    st.error("❌ OPENROUTER_API_KEY not found in Streamlit secrets.")
    st.stop()

st.title("🤖 Data Scientist Buddy")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant for data science questions."}
    ]

for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        def query_openrouter():
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
                "Referer": "https://share.streamlit.io",  # Standard header name
                "X-Title": "Data Scientist Buddy"
            }
            for attempt in range(3):
                resp = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json={"model": MODEL_ID, "messages": st.session_state.messages, "stream": False},
                    timeout=30
                )
                if resp.status_code == 200:
                    return resp.json()["choices"][0]["message"]["content"]
                if resp.status_code == 401:
                    st.error("❌ Authentication failed (401). Check your API key in Streamlit secrets.")
                    return None
                if resp.status_code in (500, 502, 503):
                    time.sleep(2 ** attempt)
                    continue
                st.error(f"❌ Error {resp.status_code}: {resp.json().get('error', {}).get('message', resp.text)}")
                return None
            return None

        reply = query_openrouter()
        if reply:
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        else:
            st.error("⚠️ Could not generate a response at this time.")
