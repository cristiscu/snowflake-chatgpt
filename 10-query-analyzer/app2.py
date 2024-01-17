import re
import streamlit as st
from snowflake.snowpark.context import get_active_session

st.title("Query Analyzer and Optimizer")
st.write("Analyze and optimize Snowflake SQL queries for corectness and performance.")

session = get_active_session()
tabs = st.tabs(["Query", "Plan", "Description", "Comments", "Optimization", "Encapsulation"])

# Snowflake-based menus
with tabs[0]:
    query = "select count(*) from snowflake_sample_data.tpch_sf1.lineitem"
    query = st.text_area("Query:", query, label_visibility="hidden")
    st.dataframe(session.sql(query).collect())

with tabs[1]:
    explain = f"EXPLAIN USING TABULAR\n{query}"
    st.code(explain, language="sql")
    st.dataframe(session.sql(explain).collect())

# ChatGPT-based menus
q = f"the Snowflake SQL query \n\n```\n{query}\n```"
q = q.replace("'", "''")

with tabs[2]:
    prompt = f"explain {q}"
    query = f"select openai_db.public.openai('{prompt}')"
    response = session.sql(query).collect()[0][0]
    st.write(response)

with tabs[3]:
    prompt = f"comment {q}"
    query = f"select openai_db.public.openai('{prompt}')"
    response = session.sql(query).collect()[0][0]
    if sql_match := re.search(r"```sql\n(.*)\n```", response, re.DOTALL):
        st.code(sql_match.group(1), language="sql")
    else: st.write(response)

with tabs[4]:
    prompt = f"optimize {q}"
    query = f"select openai_db.public.openai('{prompt}')"
    response = session.sql(query).collect()[0][0]
    st.write(response)

with tabs[5]:
    prompt = f"create a stored procedure with {q}"
    query = f"select openai_db.public.openai('{prompt}')"
    response = session.sql(query).collect()[0][0]
    if sql_match := re.search(r"```sql\n(.*)\n```", response, re.DOTALL):
        st.code(sql_match.group(1), language="sql")
    else: st.write(response)
