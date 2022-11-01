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


def check_if_submitted(player_id, round_num): 
     '''
     '''
     exists = False
     query = '''
             SELECT COUNT(DISTINCT TEAM_CHOICE) AS submitted 
             FROM choices   
             WHERE UPPER(PLAYER_ID) = '{}' 
             AND ROUND = {};
             '''.format(player_id, round_num)

     if run_query(query)['SUBMITTED'][0] > 0: 
         exists = True 

     return exists

def get_player_id(email): 
    '''
    '''
    query = '''
            SELECT PLAYER_ID 
            FROM PLAYERS 
            WHERE EMAIL_HASH = '{}'
            '''.format(hash(email))

    return run_static_query(query)['PLAYER_ID'][0]


def check_if_player(email): 
    '''
    '''
    exist = False

    query = '''
            SELECT COUNT(DISTINCT PLAYER_ID) AS PLAYER_EXISTS
            FROM PLAYERS
            WHERE EMAIL_HASH = '{}'
            '''.format(hash(email)) 

    if run_query(query)['PLAYER_EXISTS'][0] == 0: 

        query = '''
                INSERT INTO PLAYERS
                VALUES
                (SEQ_PLAYER_ID.NEXTVAL, '{}', '{}')
                '''.format(hash(email), email)

        run_query(query)

    return get_player_id(email)