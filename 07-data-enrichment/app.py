import streamlit as st
from snowflake.snowpark.context import get_active_session

st.header("Basic ChatGPT Q&A Interface")

if prompt := st.text_input(
    label="Ask a question and click Enter:",
    value="What is Snowflake"):
    prompt = prompt.replace("'", "''")
    query = f"select openai_db.public.openai('{prompt}')"
    response = get_active_session().sql(query).collect()[0][0]
    st.write(response)
