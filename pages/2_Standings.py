# import streamlit as st 
# import utils
# from streamlit_extras.switch_page_button import switch_page

# player_id = utils.check_if_player(st.experimental_user['email'])

# st.image('5.png', width = 100)

# round = utils.get_api("https://api-football-v1.p.rapidapi.com/v3/fixtures/rounds", {"league":"39","season":"2024","current":"true"})[0][-2:].strip()

# def colouring(val): 

#     if val['PLAYER'] == st.experimental_user['email'][:st.experimental_user['email'].find('@')]: 
#         colour = 'background-color: #93baa4' 
#     else: 
#         colour = 'background-color: #7b8494' 
#     return [colour] * len(val)

# query = '''
#         SELECT row_number() over(order by pts desc) as pos, substr(Email, 0, position('@', email) -1) as player, PTS 
#         FROM((
#             SELECT player_id, SUM(total) AS pts
#             FROM scores 
#             GROUP BY player_id
#         ORDER BY pts DESC) AS A 
#         INNER JOIN (SELECT EMAIL, PLAYER_ID 
#                     FROM PLAYERS) AS B 
#         ON A.PLAYER_ID = B.PLAYER_ID) 
#         ORDER BY PTS DESC 
#         '''

# standings = utils.run_static_query(query)

# st.header('Standings 🔝')

# st.table(standings.style.apply(colouring, axis = 1))

# st.markdown('---')

# st.header('Scores〽️')

# rounds = utils.run_static_query('SELECT distinct round from scores')

# st.write('Pick a Game Week')

# score_round = st.selectbox('Pick a Game Week', rounds['ROUND'], label_visibility = 'collapsed')

# query = '''
#         select b.team_choice, COALESCE(NULLIF(HOME_TEAM, TEAM_CHOICE), NULLIF(AWAY_TEAM, TEAM_CHOICE)) AS OPPO, D.DERBY, C.SCORE,
                    
#         CASE WHEN (home_team = TEAM_CHOICE AND home_goals > away_goals) 
#             OR (away_team = TEAM_CHOICE AND away_goals > home_goals) 
#         THEN 'Won' 

#         WHEN home_goals = away_goals 
#         THEN 'Drew' 

#         WHEN (home_team = TEAM_CHOICE AND home_goals < away_goals)
#             OR (away_team = TEAM_CHOICE AND away_goals < home_goals) 
#         THEN 'Lost' 

#         END AS result,
#         CASE WHEN OPPO IN (SELECT DISTINCT TEAM_CHOICE FROM CHOICES WHERE ROUND = {}) THEN TRUE ELSE FALSE END AS HEAD_2_HEAD, draw_round, double_point_round

#         from choices as b 
#         inner join fixtures as d
#         on fixture_id = id 
#         inner join results as c
#         on game_id = id
#         inner join rounds as a
#         on b.round = a.round
#         where player_id = {}
#         and b.round = {}
#         '''.format(score_round, player_id, score_round)

# lookback_info = utils.run_static_query(query).reset_index(drop = True)

# choice_lb = lookback_info['TEAM_CHOICE'][0]
# oppo_lb = lookback_info['OPPO'][0]
# derby_lb = lookback_info['DERBY'][0]
# score_lb = lookback_info['SCORE'][0]
# result_lb = lookback_info['RESULT'][0]
# h2h_lb = lookback_info['HEAD_2_HEAD'][0]
# draw_lb = lookback_info['DRAW_ROUND'][0]
# double_lb = lookback_info['DOUBLE_POINT_ROUND'][0]

# st.header('Game Week - {}'.format(score_round))

# st.markdown('## Game Week Info')

# st.write('Draw Round {}'.format('✅' if draw_lb else '❌' ))

# st.write('Double Points Round {}'.format('✅' if double_lb else '❌' ))

# st.markdown('## Choice Info')

# st.markdown('#### You picked - {}'.format(choice_lb))

# st.write('Who {} {} to {}'.format(result_lb, score_lb, oppo_lb))

# st.write('Head 2 Head Game {}'.format('✅' if h2h_lb else '❌' ))

# st.write('Derby Game {}'.format('✅' if derby_lb else '❌' ))

# st.markdown('&nbsp;')

# query = '''
#         select row_number() over(order by total desc) as pos,
#             substr(Email, 0, position('@', email) -1) as player, 
#             basic_points as basic, 
#             head_to_head_points as h2h, 
#             derby_points as derby, 
#             draw_round_points as draw, 
#             basic_points + head_to_head_points+derby_points+draw_round_points as sub, 
#             case when double then 'x2' else 'x1' end as double, 
#             total
#         from players as a 
#         left join scores as b
#         on a.player_id = b.player_id
#         where round = {} 
#         order by total desc 
#         '''.format(score_round)



# st.table(utils.run_static_query(query).style.apply(colouring, axis = 1))

# st.markdown('---')

# left, right = st.columns(2)

# with left:
#     if st.button('Pick Team'):

#         switch_page("make choice")

# with right: 
#     if st.button('Home'):

#         switch_page("home")