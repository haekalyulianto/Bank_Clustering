import streamlit as st
import pyodbc
import pandas as pd

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server}"
        + ";SERVER=" + st.secrets["db_server"]
        + ";DATABASE=" + st.secrets["db_database"]
        + ";UID=" + st.secrets["db_username"]
        + ";PWD=" + st.secrets["db_password"]
    )

def get_data():    
    conn = init_connection()
    query = "SELECT * from [dbo].[vSAPIT_Clustering_6Month]"
    df = pd.read_sql(query, conn)
    return df

