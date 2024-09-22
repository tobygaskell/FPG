import streamlit as st 
import Rules as rules
import pandas as pd
import utils
import streamlit.components.v1 as components
import Dialogs


st.set_page_config(layout="wide")

if 'page_view' not in st.session_state: 
    st.session_state['page_view'] = 'Make Choice'

round = utils.fpg_api_static('current_round')['Round ID']

round_data = utils.fpg_api('get_round_info', {'Round': round})

round_def = 'Normal Round'
submitted = False

if round_data['DMM']: 
    round_def = 'Draw Means More Round!'

if round_data['Double']: 
    round_def = 'Double Points Round!'

if round_data['DMM'] and round_data['Double']:
    round_def = 'Draw Means Mores AND Double Points Round!!'

data = {'Email': st.experimental_user.email}

# player_id = utils.fpg_api('init_player', data)['player_id']

player_id = 2

if st.sidebar.button('Rules', use_container_width=True): 
    rules.view_rules()

st.markdown('<h1 style="text-align: center;"> FPG </h1>', unsafe_allow_html=True)
st.markdown('<h3 style="text-align: center;"> Round {} - {} </h3>'.format(round, round_def), unsafe_allow_html=True)

st.markdown('---')

left, right = st.columns(2)

if left.button('Make Choice', use_container_width=True): 
    st.session_state['page_view'] = 'Make Choice'

if right.button('See FPG Table', use_container_width=True): 
    st.session_state['page_view'] = 'See Standings'

st.markdown(' ')

# st.sidebar.button(round_def, use_container_width=True)

st.sidebar.markdown('---')

st.sidebar.caption('Email: {}'.format(st.experimental_user.email))
st.sidebar.caption('Player ID: {}'.format(player_id))

if st.session_state['page_view'] == 'Make Choice':

    data = {'Round': round}

    fixtures = utils.fpg_api('get_fixtures', data)

    fix=pd.DataFrame(fixtures)
    # st.write(fix)

    fix['vs'] = fix['DERBY'].map(lambda x: '-' if not x else '⚔️')

    fix['Fixtures'] = fix['HOME_TEAM'] + ' ' + fix['vs'] + ' ' + fix['AWAY_TEAM']

    fix.rename(columns = {'HOME_LOGO' : ' ', 
                'AWAY_LOGO': '  '}, inplace = True)
    
    st.caption('⚔️ means this fixture is a derby')
    st.dataframe(fix[[' ', 'Fixtures', '  ']],column_config={
        " ": st.column_config.ImageColumn(), 
        "  ":st.column_config.ImageColumn()}, 
        use_container_width= True, hide_index=True)

    data = {'Player': player_id}

    teams = utils.fpg_api('get_available_choices', data)

    with st.form('Choice', border = False):
        team_choice = st.selectbox('Pick a Team:', [team['TEAM_NAME'] for team in  teams] )

        if st.form_submit_button('Submit', use_container_width=True): 

            data = {'Player' : player_id, 
                    'Choice' : team_choice, 
                    'Round'  : round}
            
            submitted = utils.fpg_api('make_choice', data)
            # submitted = {}r
            # submitted['Submitted'] = 'Too Late'

    if submitted:
        if submitted['Submitted'] == True: 
            st.success('You have submitted {} as you choice for round {} - Thankyou for playing!'.format(team_choice, round))

        elif submitted['Submitted'] == 'Already Chosen':
            Dialogs.update_choice(team_choice, player_id, round)

        elif submitted['Submitted'] == 'Too Late': 
            st.error('Too Late - It\'s past the cut off time for submitting a choice for round {}! Come back after the games have finished.'.format(round))

        else: 
            st.error('There was an issue submitting your choicer')

if st.session_state['page_view'] == 'See Standings':
    
    stand = utils.fpg_api('get_standings')
    
    standings = pd.DataFrame(stand)

    st.dataframe(standings[['USER', 'SCORE']], use_container_width=True, hide_index=True)