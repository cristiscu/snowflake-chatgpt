import requests, os
import streamlit as st

def getChatResponse(prompt):
    prompt = prompt.replace("'", "''")
    key = os.environ["OPENAI_API_KEY"]
    request = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={'Authorization': f'Bearer {key}'},
        json={"model": "gpt-4-1106-preview",
              "messages": [{"role": "user", "content": prompt}]}
    ).json()
    return request["choices"][0]["message"]["content"]


st.header("REST ChatGPT Q&A Interface")

if prompt := st.text_input(
    label="Ask a question and click Enter:",
    value="What is Snowflake Data Cloud"):
    st.write(getChatResponse(prompt))
