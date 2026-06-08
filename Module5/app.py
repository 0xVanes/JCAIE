import streamlit as st
import requests

def send_message(user_message, history, ai_role):
    if ai_role:
        # AI Role in n8n
        prompt = f'''System Prompt: {ai_role}
                    History: {history}
                    Question: {user_message}
                    Answer: Answer'''
    else:
        # Default AI ROLE
        prompt = f'Kamu adalah AI assistant yang suka menjawab dan bertanya'
    url = ''
    data = {"prompt": prompt, "ai_role": ai_role}
    response = requests.post(url, data)

    if response.status_code == 200:
        bot_message = response.json().get('answer', '')
        input_tokens = response.json().get('input_tokens', 0)
        output_tokens = response.json().get('output_tokens', 0)
        result = {'content': bot_message,
                  'input_tokens': input_tokens,
                  'output_tokens': output_tokens}
        return result
    else:
        return {"content": "Error", "input_tokens": 0, "output_tokens": 0}
    

st.title('Simple Chat App')
ai_role_prompt = st.text_area("AI Role (optional)", height=100, help="Define the AI's behaviour")
if ai_role_prompt:
    st.session_state.ai_role_prompt = ai_role_prompt
else:
    st.session_state.ai_role_prompt = None

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Give me a question"):
    messages_history = st.session_state.get('messages', [])[-20:]
    history = "\n\n".join([f'{msg['role']}: {msg['content']}' for msg in messages_history]) or " "

    with st.chat_message("Human"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "Human", "content": prompt})

    with st.chat_message("AI"):
        response = send_message(prompt, history, ai_role=st.session_state.get("ai_role_prompt"))
        answer = response["content"]
        st.markdown(answer)
        st.session_state.messages.append({'role': 'AI', 'content': answer})

    with st.expander("History Chat"):
        st.markdown(history)

    with st.expander("Message Details"):
        st.write(f"Input Tokens: {response['input_tokens']}")
        st.write(f"Output Tokens {response['output_tokens']}")
        if st.session_state.get("ai_role_prompt"):
            st.write(f"AI Role Prompt: Custom")
            st.write(st.session_state.get("ai_role_promt"))
        else:
            st.write(f"AI ROLE PROMPT: DEFAULT")