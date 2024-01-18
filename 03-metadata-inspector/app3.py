import re
import streamlit as st
from openai import OpenAI

def getChatResponse(prompt):
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    r = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{"role": "user", "content": prompt}])
    return r.choices[0].message.content

def runQuery(sql):
    conn = st.connection("snowflake")
    st.dataframe(conn.query(sql))


st.header("Snowflake Q&A Metadata Inspector")
st.write("Ask questions about the SNOWFLAKE_SAMPLE_DATA database...")

if prompt := st.sidebar.text_area(label="Ask question here:"):
    prompt = ("Respond with one single Snowflake query that returns"
        + " metadata from the SNOWFLAKE_SAMPLE_DATA database"
        + f" using the INFORMATION_SCHEMA: {prompt}")
    response = getChatResponse(prompt)

    tabTable, tabText = st.tabs(["Table", "Text"])
    tabText.write(response)

    with tabTable:
        if sql_match := re.search(r"```sql\n(.*)\n```", response, re.DOTALL):
            runQuery(sql_match.group(1))
        else:
            st.warning("Nothing returned!")
