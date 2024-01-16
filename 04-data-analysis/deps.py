import re
import streamlit as st
from openai import OpenAI

@st.cache_data(show_spinner="Loading system prompt...")
def get_system_prompt():
    DATABASE = "FROSTY_SAMPLE"
    SCHEMA = "CYBERSYN_FINANCIAL"
    TABLE = "FINANCIAL_ENTITY_ANNUAL_TIME_SERIES"

    # get columns
    conn = st.connection("snowflake")
    sql = ("SELECT COLUMN_NAME, DATA_TYPE"
        + f" FROM {DATABASE}.INFORMATION_SCHEMA.COLUMNS"
        + f" WHERE TABLE_SCHEMA = '{SCHEMA}' AND TABLE_NAME = '{TABLE}'")
    columns = conn.query(sql, show_spinner=False)
    columns = "\n".join([
        f"- **{columns['COLUMN_NAME'][i]}**: {columns['DATA_TYPE'][i]}"
        for i in range(len(columns["COLUMN_NAME"]))])

    # get metadata
    sql = ("SELECT VARIABLE_NAME, DEFINITION"
        + f" FROM {DATABASE}.{SCHEMA}.FINANCIAL_ENTITY_ATTRIBUTES_LIMITED;")
    metadata = conn.query(sql, show_spinner=False)
    metadata = "\n".join([
        f"- **{metadata['VARIABLE_NAME'][i]}**: {metadata['DEFINITION'][i]}"
        for i in range(len(metadata["VARIABLE_NAME"]))])

    with open("data/system-prompt.txt") as file:
        return file.read().format(**locals())

@st.cache_data(show_spinner="Loading questions...")
def get_prompt_questions():
    with open("data/questions.txt") as file:
        return [line.rstrip() for line in file]

@st.cache_resource(show_spinner="Connecting to ChatGPT...")
def getClient():
    return OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def getDataframe(response):
    message = {"role": "assistant", "content": response}
    sql_match = re.search(r"```sql\n(.*)\n```", response, re.DOTALL)
    if sql_match:
        sql = sql_match.group(1)
        conn = st.connection("snowflake")
        message["results"] = conn.query(sql)
        st.dataframe(message["results"])
    st.session_state.messages.append(message)

def getResults():
    response = ""
    resp_container = st.empty()
    for delta in getClient().chat.completions.create(
        stream=True,
        model="gpt-4-1106-preview",
        messages=([{"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages])):
        response += (delta.choices[0].delta.content or "")
        resp_container.markdown(response)
    getDataframe(response)
