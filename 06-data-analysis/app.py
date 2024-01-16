import streamlit as st
import deps

st.title("Data Analysis Inspector")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": deps.get_system_prompt()}]

if prompt := st.selectbox("Select a question:", deps.get_prompt_questions(), index=None):
    st.session_state.messages.append({"role": "user", "content": prompt})

if st.session_state.messages[-1]["role"] != "assistant":
    deps.getResults()
