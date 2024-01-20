import os.path
import streamlit as st
from snowflake.snowpark import Session
from langchain_community.utilities import SQLDatabase
from langchain_openai import OpenAI
from langchain.chains import create_sql_query_chain

def getParams():
    openai_key = ""
    pars = {
        "account": "",
        "user": "",
        "password": "",
        "database": "SNOWFLAKE_SAMPLE_DATA",
        "schema": "TPCH_SF1",
        "warehouse": "COMPUTE_WH",
        "role": "ACCOUNTADMIN"
    }
    #if os.path.isfile("./.streamlit/secrets.toml"):
    #    openai_key = st.secrets["OPENAI_API_KEY"]
    #    section = st.secrets[f"connections_snowflake"]
    #    pars["account"] = section["account"]
    #    pars["user"] = section["user"]
    #    pars["password"] = section["password"]
    #    pars["database"] = section["database"]
    #    pars["schema"] = section["schema"]
    #    pars["warehouse"] = section["warehouse"]
    #    pars["role"] = section["role"]

    must_connect = (len(openai_key) == 0)
    if must_connect: st.warning("Please connect first.")
    with st.sidebar.expander("Connection Form", expanded=must_connect):
        with st.form("my_form"):
            openai_key = st.text_input("OpenAI API Key:", type="password", value=openai_key)
            pars['account'] = st.text_input("Snowflake Account:", value=pars['account'])
            pars['user'] = st.text_input("User Name:", value=pars['user'])
            pars['password'] = st.text_input("Password:", type="password", value=pars['password'])
            pars['database'] = st.text_input("Database:", value=pars['database'])
            pars['schema'] = st.text_input("Schema:", value=pars['schema'])
            pars['warehouse'] = st.text_input("Warehouse:", value=pars['warehouse'])
            pars['role'] = st.text_input("Role:", value=pars['role'])

            submit = st.form_submit_button("Connect")
            if len(openai_key) == 0 and not submit: st.stop()
    return openai_key, pars

@st.cache_resource(show_spinner="Connecting...")
def getSession(openai_key, pars):
    session = Session.builder.configs(pars).create()

    url = (f"snowflake://{pars['user']}:{pars['password']}@{pars['account']}"
        + f"/{pars['database']}/{pars['schema']}"
        + f"?warehouse={pars['warehouse']}&role={pars['role']}")
    db = SQLDatabase.from_uri(url)
    llm = OpenAI(openai_api_key=openai_key)
    chain = create_sql_query_chain(llm, db)
    return session, db, chain


st.title("LangChain SQL Generator")
st.write("Returns and runs queries from questions in natural language.")

openai_key, pars = getParams()
session, db, chain = getSession(openai_key, pars)

question = st.sidebar.text_area("Ask a question:",
    value="show me the total number of entries in the first table")
sql = chain.invoke({"question": question})

tabQuery, tabData, tabLog = st.tabs(["Query", "Data", "Log"])
tabQuery.code(sql, language="sql")
tabData.dataframe(session.sql(sql))
tabLog.code(db.table_info, language="sql")
