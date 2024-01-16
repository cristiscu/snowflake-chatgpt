import streamlit as st
from snowflake.snowpark import Session
from langchain_community.utilities import SQLDatabase
from langchain_openai import OpenAI
from langchain.chains import create_sql_query_chain

@st.cache_resource(show_spinner="Connecting...")
def getSession():
    section = st.secrets[f"connections_snowflake"]
    pars = {
        "account": section["account"],
        "user": section["user"],
        "password": section["password"],
        "database": section["database"],
        "schema": section["schema"],
        "warehouse": section["warehouse"],
        "role": section["role"]
    }
    session = Session.builder.configs(pars).create()

    url = (f"snowflake://{pars['user']}:{pars['password']}@{pars['account']}"
        + f"/{pars['database']}/{pars['schema']}"
        + f"?warehouse={pars['warehouse']}&role={pars['role']}")
    db = SQLDatabase.from_uri(url)

    openai_key = st.secrets["OPENAI_API_KEY"]
    llm = OpenAI(openai_api_key=openai_key)
    chain = create_sql_query_chain(llm, db)
    return session, db, chain


st.title("LangChain Demo App")
st.write("Returns and runs queries from questions in natural language.")

session, db, chain = getSession()

question = st.sidebar.text_area("Ask a question:",
    value="show me the total number of entries in the first table")
sql = chain.invoke({"question": question})

tabQuery, tabData, tabLog = st.tabs(["Query", "Data", "Log"])
tabQuery.code(sql, language="sql")
tabData.dataframe(session.sql(sql))
tabLog.code(db.table_info, language="sql")
