import streamlit as st 
# import utils
# from streamlit_extras.switch_page_button import switch_page
import requests as r 
import random 
import Rules as rules
import pandas as pd
# # st.set_page_config(layout="wide")

# st.image('5.png', width = 100)


# round = utils.get_api("https://api-football-v1.p.rapidapi.com/v3/fixtures/rounds", 
#                      {"league":"39","season":"2024","current":"true"})[0][-2:].strip()

# player_id = utils.check_if_player(st.experimental_user['email'])

if 'page_view' not in st.session_state: 
    st.session_state['page_view'] = 'Make Choice'

env = 'Not Local'
player = 100
round = random.choice([i+1 for i in range(3)])






if env == 'Local':
    url = 'http://192.168.0.110:5001'
else: 
    url = 'http://94.2.195.17:5001'


data = {'Email':st.experimental_user.email}

player_id = r.post(url + '/init_player', json = data).json()['player_id']


# st.sidebar.caption()

if st.sidebar.button('Rules', use_container_width=True): 
    rules.view_rules()
# round = 'Testing'



st.markdown('<h1 style="text-align: center;"> FPG </h1>', unsafe_allow_html=True)
st.markdown('<h3 style="text-align: center;"> Round {} </h3>'.format(round), unsafe_allow_html=True)

st.markdown('---')

# round_info = r.post(url + '/get_round_info', json = {'Round' : round}).json()

# st.write(round_info)

left, right = st.columns(2)

if left.button('Make Choice', use_container_width=True): 
    st.session_state['page_view'] = 'Make Choice'

if right.button('See Standings', use_container_width=True): 
    st.session_state['page_view'] = 'See Standings'

st.markdown(' ')
st.markdown(' ')
st.markdown(' ')

# with left: 
st.sidebar.markdown('---')
# st.sidebar.button('Draw Means More Round', disabled = not round_info['DMM'], use_container_width= True)
st.sidebar.button('Draw Means More Round', disabled = False, use_container_width= True)
# st.sidebar.write(round_info['DMM'])

# with right: 
# st.sidebar.button('Double Round', disabled = not round_info['Double'], use_container_width=True )
st.sidebar.button('Double Round', disabled = True, use_container_width = True)
# st.sidebar.write(round_info['Double'])
st.sidebar.caption('Email: {}'.format(st.experimental_user.email))
st.sidebar.caption('Player ID: {}'.format(player_id))


if st.session_state['page_view'] == 'Make Choice':

    fixtures = pd.DataFrame({'Home Team':['Team 1',
                                        'Team 2',
                                        'Team 3',
                                        'Team 4',
                                        'Team 5',
                                        'Team 6',
                                        'Team 7',
                                        'Team 8',
                                        'Team 9', 
                                        'Team 10'], 
                            'Away Team':['Team 11',
                                        'Team 12',
                                        'Team 13',
                                        'Team 14',
                                        'Team 15',
                                        'Team 16',
                                        'Team 17',
                                        'Team 18',
                                        'Team 19', 
                                        'Team 20']})



    # def left_align(s):
    #     return 'text-align: center;'



    # st.dataframe(fixtures.style.applymap(left_align), use_container_width=True, hide_index=True)
    left, center, right = st.columns(3)

    left.caption('Home Team')

    right.caption('<div style="text-align: right"> Away Team </div>', unsafe_allow_html=True)
    with st.container(border=True):


        for index, row in fixtures.iterrows():
            left, center, right  = st.columns(3)

            left.write(row['Home Team'])

            center.caption('<div style="text-align: center"> vs </div>', unsafe_allow_html=True)

            right.write('<div style="text-align: right"> {} </div>'.format(row['Away Team']), unsafe_allow_html=True)

    # st.dataframe(fixtures, use_container_width=True, hide_index=True)


    teams = r.get(url = url + '/get_teams').json()['Teams']


    with st.form('Choice', border = False):
        team_choice = st.selectbox('Pick a Team:', teams )

        # round_choice = st.number_input('Pick a Round:', step = 1, value= 1, max_value= 38 )

        if st.form_submit_button('Submit', use_container_width=True): 

            data = {'Player' : player_id, 
                    'Choice' : team_choice, 
                    'Round'  : round}
            
            r.post(url + '/make_choice', json = data)

            data = {'Player': player_id, 
                    'Choice': team_choice, 
                    'Round': round}
            
            result_data = r.post(url + '/get_result', json = data).json()

            # data = {'Player' : player, 
            #         'Result' : result_data['Result'], 
            #         'H2H' : result_data['H2H'], 
            #         'Derby': result_data['Derby'], 
            #         'DMM': round_info['DMM'], 
            #         'Doubled': round_info['Double']}
            
            data = {'Player' : player_id, 
                    'Result' : result_data['Result'], 
                    'H2H' : result_data['H2H'], 
                    'Derby': result_data['Derby'], 
                    'DMM': True, 
                    'Doubled': False}
            
            score_data = r.post(url + '/get_score', json = data).json()

            left, right = st.columns(2)

            with left: 
                st.write(result_data)

            with right: 
                st.write(score_data)

if st.session_state['page_view'] == 'See Standings':

    standings = pd.DataFrame({'Player':['Player 1', 'Player 2', 'Player 3', 'Player 4', 'Player 5', 'Player 6'], 
                            'Score': [34, 33, 29, 25, 0, -10]})

    st.dataframe(standings, use_container_width=True, hide_index=True)