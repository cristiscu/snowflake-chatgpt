import os
from snowflake.snowpark import Session
import streamlit as st
import charts.chart1 as c1

st.title("Usage Monitoring")

pars = {
    "account": 'hdb90888',
    "user": 'cristiscu',
    "password": os.environ['SNOWSQL_PWD'],
    "database": 'TESTS',
    "schema": 'PUBLIC'
}
session = Session.builder.configs(pars).create()

tabs = st.tabs(["Chart", "SQL", "Plotly"])

query = open("sql/query1.sql", "r").read()
tabs[1].code(query, language="sql")

code = open("charts/chart1.py", "r").read()
tabs[2].code(code, language="python")

df = session.sql(query).to_pandas()
tabs[0].plotly_chart(c1.getChart(df))
