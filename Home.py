import streamlit as st 
import Rules as rules
import pandas as pd
import utils
import streamlit.components.v1 as components


st.set_page_config(layout="wide")

if 'page_view' not in st.session_state: 
    st.session_state['page_view'] = 'Make Choice'

round = utils.fpg_api_static('current_round')['Round ID']

round_data = utils.fpg_api('get_round_info', {'Round': round})

round_def = 'Normal Round'

if round_data['DMM']: 
    round_def = 'Draw Means More Round!'

if round_data['Double']: 
    round_def = 'Double Points Round!'

if round_data['DMM'] and round_data['Double']:
    round_def = 'Draw Means Mores AND Double Points Round!!'

data = {'Email': st.experimental_user.email}

player_id = utils.fpg_api('init_player', data)['player_id']

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

    fix['vs'] = 'vs'

    fix['Fixtures'] = fix['HOME_TEAM'] + ' ' + fix['vs'] + ' ' + fix['AWAY_TEAM']

    fix.rename(columns = {'HOME_LOGO' : ' ', 
                'AWAY_LOGO': '  '}, inplace = True)
    
    st.dataframe(fix[[' ', 'Fixtures', '  ']],column_config={
        " ": st.column_config.ImageColumn(), 
        "  ":st.column_config.ImageColumn()}, 
        use_container_width= True, hide_index=True)

    data = {'Player': player_id}

    teams = utils.fpg_api('get_available_choices', data)

    with st.form('Choice', border = True):
        team_choice = st.selectbox('Pick a Team:', [team['TEAM_NAME'] for team in  teams] )

        if st.form_submit_button('Submit', use_container_width=True): 

            data = {'Player' : player_id, 
                    'Choice' : team_choice, 
                    'Round'  : round}
            
            submitted = utils.fpg_api('make_choice', data)

            if submitted['Submitted']: 
                st.success('You have submitted {} as you choice for round {} - Thankyou for playing!'.format(team_choice, round))
            else: 
                st.error('There was an issue submitting your choicer')

if st.session_state['page_view'] == 'See Standings':

    standings = pd.DataFrame({'Player':['Player 1', 'Player 2', 'Player 3', 'Player 4', 'Player 5', 'Player 6'], 
                            'Score': [34, 33, 29, 25, 0, -10]})

    st.dataframe(standings, use_container_width=True, hide_index=True)