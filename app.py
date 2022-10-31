import streamlit as st
import snowflake.connector
import pandas as pd
import numpy as np

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

st.title('FPG')

def check_if_submitted(player_id, round_num): 
    '''
    '''
    exists = False
    query = '''
            SELECT COUNT(DISTINCT TEAM_CHOICE) AS submitted 
            FROM PLAYER_CHOICES 
            WHERE UPPER(PLAYER_ID) = '{}' 
            AND ROUND = {};
            '''.format(player_id.upper(), round_num)

    if run_query(query)['SUBMITTED'][0] > 0: 
        exists = True 

    return exists

teams = run_static_query('SELECT team_name FROM prem_teams order by team_name asc;')

option = st.selectbox('Pick a Team', teams['TEAM_NAME'])

st.subheader(option)

if st.button('Submit Choice'): 

    exists = check_if_submitted('PL1', 1)

    if not exists:
        query = '''
                INSERT INTO PLAYER_CHOICES
                VALUES
                ('PL1', '{}', 1)
                '''.format(option)
    else: 
        query = '''
                UPDATE PLAYER_CHOICES
                SET TEAM_CHOICE = '{}'
                WHERE UPPER(PLAYER_ID) = 'PL1'
                AND ROUND = 1
                '''.format(option)

    run_query(query)

    st.caption('Choice')
    st.write('Round 1: {}'.format(option))

# query = '''
#         select home_lat as "lon", home_lon as "lat"
#         FROM prem_teams 
#         '''

# left_column, middle_column, right_column,  = st.columns(3)

# with right_column:
#     st.map(run_query(query))












