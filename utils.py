import streamlit as st 
import requests as re 
import pandas as pd 
import snowflake.connector


# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )

conn = init_connection()

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_static_query(query):
    '''
    '''
    with conn.cursor() as cur:
        cur.execute(query)
        return pd.DataFrame.from_records(iter(cur), columns = [x[0] for x in cur.description])

def run_query(query):
    '''
    '''
    with conn.cursor() as cur:
        cur.execute(query)
        return pd.DataFrame.from_records(iter(cur), columns = [x[0] for x in cur.description])


@st.experimental_singleton
def get_api(url, querystring = {}): 
    '''
    '''
    headers = {
        "X-RapidAPI-Key": st.secrets["api"]['key'],
        "X-RapidAPI-Host": st.secrets["api"]['host']
    }

    response = re.request("GET", url, headers=headers, params=querystring)

    return response.json()['response']