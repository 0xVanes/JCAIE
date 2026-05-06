import streamlit as st

def render_floating_agent():
    st.markdown('''
    <div class="ai-agent" id="ai-agent-btn">
        <div class="ai-agent-portrait">🤖</div>
                
        🎬 MOVIE ASSISTANT 🎬
            I recommend movies based on
            your age & preferences, to
            help you find where to watch
            them legally in Indonesia.
            Start typing in the chatbox!
    </div>
    ''', unsafe_allow_html=True)