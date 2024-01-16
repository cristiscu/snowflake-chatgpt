import streamlit as st
import deps

st.title("Data Analysis Inspector")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": deps.get_system_prompt()}]

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})

# write all previous message exchanges
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if "results" in message:
                st.dataframe(message["results"])

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        deps.getResults()
