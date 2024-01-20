import os
from snowflake.snowpark import Session
import streamlit as st

def getSession():
    return Session.builder.configs({
        "account": 'hdb90888',
        "user": 'cristiscu',
        "password": os.environ['SNOWSQL_PWD'],
        "database": 'SNOWFLAKE',
        "schema": 'ACCOUNT_USAGE'
    }).create()

def showChart(name):
    st.title("Usage Monitoring Dashboard")
    tabChart, tabQuery, tabCode = st.tabs(["Chart", "Query", "Code"])

    query = open(f"queries/{name}.sql", "r").read()
    tabQuery.code(query, language="sql")

    code = open(f"charts/{name}.py", "r").read()
    tabCode.code(code, language="python")

    df = getSession().sql(query).to_pandas()
    if name == 'Credit_Usage_Query':
        import charts.Credit_Usage_Query as cuq
        fig = cuq.getChart(df)
    elif name == 'Storage_Usage_Query':
        import charts.Storage_Usage_Query as suq
        fig = suq.getChart(df)
    elif name == 'Longest_Running_Queries':
        import charts.Longest_Running_Queries as lrq
        fig = lrq.getChart(df)
    
    tabChart.plotly_chart(fig)
