import streamlit as st
import requests

API_URL = 'http://localhost:8000/chat' #sesuai url dari main.py
st.set_page_config(page_title="Simple LLM Chatbot", page_icon="🤖")
st.title("🤖Simple LLM Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = {"input": 0, "output": 0}

def build_history_text() -> str:
    lines = []
    for msg in st.session_state.messages:
        role = "User" if msg["role"] == "user" else "Assistant"
        lines.append(f"{role}: {msg['content']}")
    return "\n".join(lines)

def call_api(question: str, history: str) -> dict:
    response = requests.post(API_URL,
                             json = {"question": question, "history": history},
                             timeout= 60,)
    response.raise_for_status()
    return response.json()

# Render existing chat history
for msg in st.session_state.messages:
    with st.chat_message(msg['role']):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ketik pertanyaan Anda ..."):
    # Tampilkan pesan user
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Bangun history dari semua pesan sebelum pertanyaan saat ini
    history_text = build_history_text()[:-len(f'User: {prompt}') -1].rstrip()

    # Panggil API dan tampilkan respons
    with st.chat_message("assistant"):
        with st.spinner("Sedang berfikir..."):
            try:
                result = call_api(question=prompt, history=history_text)
                answer = result["answer"]
                token_input = result["token_input"]
                token_output = result["token_output"]

                st.markdown(answer)
                st.caption(f'Token - inputL {token_input} | output: {token_output}')
                st.session_state.messages.append({"role": "assistant", "content": answer})
                st.session_state.total_tokens["input"] += token_input
                st.session_state.total_tokens["output"] += token_output
            except requests.exceptions.ConnectionError:
                st.error("Tidak dapat terhubung ke API. Pastikan Docker container sudah berjalan di port 8000")
            except requests.exceptions.HTTPError as e:
                st.error(f"API error: {e.response.status_code} - {e.response.text}")
            except Exception as e:
                st.error(f'Terjadi kesalahan: {e}')

with st.sidebar:
    st.header("Statistik Sesi")
    st.metric("Pesan", len(st.session_state.messages))
    st.metric("Total Token Input", st.session_state.total_tokens["input"])
    st.metric("Total Token Output", st.session_state.total_tokens["output"])
    st.divider()

    if st.button("Hapus Riwayat Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.total_tokens = {"input": 0, "output": 0}
        st.rerun()