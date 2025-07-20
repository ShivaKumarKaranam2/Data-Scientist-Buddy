import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Data Scientist Buddy", page_icon="🤖")
st.title("🤖 Data Scientist Buddy ")

# ✅ Load API key securely
API_KEY = st.secrets.get("GEMINI_API_KEY")
if not API_KEY:
    st.error("❌ GEMINI_API_KEY not found in secrets.")
    st.stop()

# ✅ Configure Gemini
genai.configure(api_key=API_KEY)

# ✅ Custom system instruction (clear prompt)
system_instruction = (
    "You are a helpful, friendly, and knowledgeable AI assistant specialized in data science. "
    "You help students, beginners, and professionals understand concepts in Python, statistics, "
    "machine learning, AI, data analysis, and visualization. Provide clear explanations, code examples, "
    "and suggestions using markdown formatting when necessary. Keep responses concise but informative."
)

# ✅ Initialize chat with system prompt
if "chat" not in st.session_state:
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",  # fallback to "gemini-1.5-flash" if needed
        system_instruction=system_instruction
    )
    st.session_state.chat = model.start_chat(history=[])

# ✅ Display previous chat history
for msg in st.session_state.chat.history:
    with st.chat_message("user" if msg.role == "user" else "assistant"):
        st.markdown(msg.parts[0].text if msg.parts else msg.text)

# ✅ Accept and process user input
if prompt := st.chat_input("Ask anything about data science..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        response = st.session_state.chat.send_message(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
    except Exception as e:
        st.error("⚠️ Could not generate a response. Check your API key or model access.")
