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

st.title("Usage Monitoring Dashboard")

sels = ["Credit Usage Query", "Storage Usage Query", "Longest Running Queries"]
tabs = st.tabs(sels)

name = "Credit_Usage_Query"
query = open(f"queries/{name}.sql", "r").read()
df = getSession().sql(query).to_pandas()
import charts.Credit_Usage_Query as cuq
fig = cuq.getChart(df)
tabs[0].plotly_chart(fig)

name = "Storage_Usage_Query"
query = open(f"queries/{name}.sql", "r").read()
df = getSession().sql(query).to_pandas()
import charts.Storage_Usage_Query as suq
fig = suq.getChart(df)
tabs[1].plotly_chart(fig)

name = "Longest_Running_Queries"
query = open(f"queries/{name}.sql", "r").read()
df = getSession().sql(query).to_pandas()
import charts.Longest_Running_Queries as lrq
fig = lrq.getChart(df)
tabs[2].plotly_chart(fig)
