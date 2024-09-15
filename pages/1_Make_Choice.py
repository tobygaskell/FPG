import streamlit as st
# import snowflake.connector
import pandas as pd
# import numpy as np
import utils as utils
# from streamlit_extras.switch_page_button import switch_page

# st.image('5.png', width = 100)

# round = utils.get_api("https://api-football-v1.p.rapidapi.com/v3/fixtures/rounds", {"league":"39","season":"2024","current":"true"})[0][-2:].strip()

# player_id = utils.check_if_player(st.experimental_user['email'])

# st.title('Game Week - {}'.format(round))

# query = '''
#         SELECT double_point_round, draw_round 
#         FROM rounds 
#         where round = {}
#         '''.format(round)

# round_info = utils.run_static_query(query)

# double_round = round_info['DOUBLE_POINT_ROUND'][0]

# draw_round = round_info['DRAW_ROUND'][0]

# st.subheader('Double Points Round {}'.format('✅' if double_round else '❌' ))

# st.subheader('Draw Round {}'.format('✅' if draw_round else '❌' ))

# st.markdown('---')

# teams = utils.run_static_query('SELECT team_name, logo, team_id FROM teams order by team_name asc;')

# query = '''
#         SELECT HOME_TEAM,
#                AWAY_TEAM, 
#                dayname(kickoff)|| ' ' || TO_VARCHAR(KICKOFF, 'HH12 AM') as game_day, 
#                case when derby then '(Derby)' else '' end as derby
#         FROM FIXTURES
#         WHERE ROUND = {}
#         AND SEASON = 2022
#         '''.format(round)

# fixtures = utils.run_static_query(query)

# body = '## Fixtures this round:'
# for index, row in fixtures.iterrows(): 
#     if row['DERBY'] == '(Derby)': 
#         body = body + '\n- {} vs {} {}'.format(row['HOME_TEAM'], row['AWAY_TEAM'], '⚔️')
#     else: 
#         body = body + '\n- {} vs {}'.format(row['HOME_TEAM'], row['AWAY_TEAM'])
        
# st.markdown(body)

# st.markdown('## Pick a Team')   

# option = st.selectbox('Pick a team', teams['TEAM_NAME'], label_visibility = 'collapsed')

# option_id = teams[teams['TEAM_NAME'] == option].reset_index(drop = True)['TEAM_ID'][0]

# st.markdown('---')

# st.image(teams[teams['TEAM_ID'] == option_id].reset_index(drop = True)['LOGO'][0])

# st.markdown('## {}'.format(option))
# if option in fixtures['HOME_TEAM'].unique(): 
#     st.markdown('##### Home to {} ({})'.format(fixtures[fixtures['HOME_TEAM']== option].reset_index(drop = True)['AWAY_TEAM'][0], 
#                                             fixtures[fixtures['HOME_TEAM']== option].reset_index(drop = True)['GAME_DAY'][0]))

# elif option in fixtures['AWAY_TEAM'].unique(): 
#     st.markdown('##### Away to {} ({})'.format(fixtures[fixtures['AWAY_TEAM']== option].reset_index(drop = True)['HOME_TEAM'][0], 
#                                             fixtures[fixtures['AWAY_TEAM']== option].reset_index(drop = True)['GAME_DAY'][0]))

# st.markdown('#### Last 5 Results:')

# query = '''
#         select round,home_team || ' vs ' || away_team as game, 
#                 score, 
#                 case when (home_team = '{option}' and home_goals > away_goals)
#                         or (away_team = '{option}' and away_goals > home_goals) 
#                     then 'Win' 
#                     when home_goals = away_goals 
#                     then 'Draw' 
#                     when (home_team = '{option}' and home_goals < away_goals)
#                         or (away_team = '{option}' and away_goals < home_goals) 
#                     then 'Loss' end as result 
#         from results as a
#         inner join fixtures as b 
#         on a.game_id = b.id
#         where home_team || away_team like '%{option}%'
#         and game_status = 'FT'
#         AND SEASON = 2022
#         order by kickoff desc 
#         limit 5 
#         '''.format(option = option)

# def colouring(val): 

#     if val['RESULT'] == 'Win': 
#         colour = 'background-color: #87c46a' 
#     elif val['RESULT'] == 'Draw': 
#         colour = 'background-color: #e6c050' 
#     elif val['RESULT'] == 'Loss': 
#         colour =  'background-color: #d6796d'

    
#     return [colour] * 4

# st.dataframe(utils.run_static_query(query).style.apply(colouring, axis = 1))

# st.markdown('#### Result for this Fixture Last Season:')

# if option in fixtures['HOME_TEAM'].unique(): 
#     query = '''
#             SELECT SCORE, case when (home_team = '{option}' and home_goals > away_goals)
#                             or (away_team = '{option}' and away_goals > home_goals) 
#                         then 'Win' 
#                         when home_goals = away_goals 
#                         then 'Draw' 
#                         when (home_team = '{option}' and home_goals < away_goals)
#                             or (away_team = '{option}' and away_goals < home_goals) 
#                         then 'Loss' end as result 
#             FROM fixtures 
#             INNER JOIN results 
#             ON id = game_id 
#             WHERE home_team = '{option}' 
#             AND away_team = '{oppo}' 
#             AND season = 2021 
#             '''.format(option = option, oppo = fixtures[fixtures['HOME_TEAM']== option].reset_index(drop = True)['AWAY_TEAM'][0])

# if option in fixtures['AWAY_TEAM'].unique(): 
#     query = '''
#             SELECT SCORE, case when (home_team = '{option}' and home_goals > away_goals)
#                             or (away_team = '{option}' and away_goals > home_goals) 
#                         then 'Win' 
#                         when home_goals = away_goals 
#                         then 'Draw' 
#                         when (home_team = '{option}' and home_goals < away_goals)
#                             or (away_team = '{option}' and away_goals < home_goals) 
#                         then 'Loss' end as result 
#             FROM fixtures 
#             INNER JOIN results 
#             ON id = game_id 
#             WHERE home_team = '{oppo}' 
#             AND away_team = '{option}' 
#             AND season = 2021 
#             '''.format(option = option, oppo = fixtures[fixtures['AWAY_TEAM']== option].reset_index(drop = True)['HOME_TEAM'][0])

# last_year_result  = utils.run_static_query(query)

# if len(last_year_result) > 0: 
#     if last_year_result['RESULT'][0] == 'Win': 
#         st.markdown('##### {} {} ✅'.format(last_year_result['SCORE'][0], last_year_result['RESULT'][0]))
#     elif last_year_result['RESULT'][0] == 'Loss': 
#         st.markdown('##### {} {} ❌'.format(last_year_result['SCORE'][0], last_year_result['RESULT'][0]))
#     elif last_year_result['RESULT'][0] == 'Draw': 
#         st.markdown('##### {} {} 🤝'.format(last_year_result['SCORE'][0], last_year_result['RESULT'][0]))    
# else:
#     st.markdown('This fixture didn\'t happen last year')

# st.markdown('---')

# left, right = st.columns(2)

# with left:

#     if st.button('Submit Choice'): 

#         exists = utils.check_if_submitted(player_id, round)

#         if not exists:
#             query = '''
#                     INSERT INTO choices
#                     VALUES
#                     ('{}', '{}', {})
#                     '''.format(player_id, option, round)
#         else: 
#             query = '''
#                     UPDATE choices
#                     SET TEAM_CHOICE = '{}'
#                     WHERE UPPER(PLAYER_ID) = '{}'
#                     AND ROUND = {}
#                     '''.format(option, player_id, round)

#         utils.run_query(query)
#         st.write('Choice Submitted')

# with right: 
#     if st.button('Home'):

#         switch_page("home")











