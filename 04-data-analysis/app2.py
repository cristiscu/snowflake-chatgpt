import os
import streamlit as st
from openai import OpenAI

st.title("Basic ChatGPT Bot (Chat)")

# initialize status log
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "user", "content": "Hi"}]

# question (from you)
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})

# write all previous message exchanges
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# answer (from ChatGPT)
if st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        r = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=([{"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages]))
        response = r.choices[0].message.content
        st.empty().markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
