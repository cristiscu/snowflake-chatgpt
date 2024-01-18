import re
import streamlit as st
from openai import OpenAI

def getChatResponse(prompt):
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    r = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=([{"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages]))
    return r.choices[0].message.content

def runQuery(sql):
    conn = st.connection("snowflake")
    results = None
    try:
        results = conn.query(sql)
        st.dataframe(results)
    except:
        st.error("Wrong query!")
    return results


st.title("Snowflake Chat Metadata Inspector")

first = "messages" not in st.session_state
if first:
    st.session_state.messages = [{"role": "system", "content": 
        ("Respond with one single Snowflake query that returns"
        + " metadata from the SNOWFLAKE_SAMPLE_DATA database"
        + f" using the INFORMATION_SCHEMA.")}]

if prompt := st.chat_input(placeholder="Ask a question about Snowflake metadata"):
    st.session_state.messages.append({"role": "user", "content": prompt})

if not first and st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        response = getChatResponse(prompt)
        st.write(response)

        message = {"role": "assistant", "content": response}
        if sql_match := re.search(r"```sql\n(.*)\n```", response, re.DOTALL):
            message["results"] = runQuery(sql_match.group(1))
        else:
            st.error("No query!")
        st.session_state.messages.append(message)
