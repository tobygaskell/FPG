import streamlit as st
import snowflake.connector
import pandas as pd
import numpy as np
import utils as utils

st.sidebar.image('5.png', width = 100)
st.title('Football Prediction Game')



player_id = utils.check_if_player(st.experimental_user['email'])

st.write(player_id)

round = utils.get_api("https://api-football-v1.p.rapidapi.com/v3/fixtures/rounds", {"league":"39","season":"2022","current":"true"})[0][-2:].strip()

teams = utils.run_static_query('SELECT team_name, logo, team_id FROM teams order by team_name asc;')

st.sidebar.markdown('## Pick a Team')   
option = st.sidebar.radio('Pick a team', teams['TEAM_NAME'], label_visibility = 'collapsed')

option_id = teams[teams['TEAM_NAME'] == option].reset_index(drop = True)['TEAM_ID'][0]

left, right = st.columns(2)

with left: 

    query = '''
            SELECT HOME_TEAM, AWAY_TEAM, dayname(kickoff)|| ' ' || TO_VARCHAR(KICKOFF, 'HH12 AM') as game_day
            FROM FIXTURES
            WHERE ROUND = {}
            '''.format(round)

    fixtures = utils.run_static_query(query)

    body = '## Fixtures this round:'
    for index, row in fixtures.iterrows(): 
        body = body + '\n- {} vs {}'.format(row['HOME_TEAM'], row['AWAY_TEAM'])

    st.markdown(body)

with right: 
    st.image(teams[teams['TEAM_ID'] == option_id].reset_index(drop = True)['LOGO'][0])

    if option in fixtures['HOME_TEAM'].unique(): 
        st.markdown('## {} are at home to {} ({})'.format(option, 
                                                         fixtures[fixtures['HOME_TEAM']== option].reset_index(drop = True)['AWAY_TEAM'][0], 
                                                         fixtures[fixtures['HOME_TEAM']== option].reset_index(drop = True)['GAME_DAY'][0]))

    elif option in fixtures['AWAY_TEAM'].unique(): 
        st.markdown('## {} are away to {} ({})'.format(option, 
                                                       fixtures[fixtures['AWAY_TEAM']== option].reset_index(drop = True)['HOME_TEAM'][0], 
                                                       fixtures[fixtures['AWAY_TEAM']== option].reset_index(drop = True)['GAME_DAY'][0]))



    
    # st.markdown('#### From This Season:')
    # form = utils.get_api("https://api-football-v1.p.rapidapi.com/v3/teams/statistics", {"league":"39",
    #                                                                                     "season":"2022", 
    #                                                                                     "team":option_id})['form']
    # st.write(form)

    st.markdown('#### last 5 Results:')
    st.write('WWWWW')








if st.sidebar.button('Submit Choice'): 

    exists = utils.check_if_submitted('PL1', 1)

    if not exists:
        query = '''
                INSERT INTO choices
                VALUES
                ('PL1', '{}', 1)
                '''.format(option)
    else: 
        query = '''
                UPDATE choices
                SET TEAM_CHOICE = '{}'
                WHERE UPPER(PLAYER_ID) = 'PL1'
                AND ROUND = 1
                '''.format(option)

    utils.run_query(query)













