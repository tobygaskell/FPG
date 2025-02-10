import streamlit as st
import Rules as rules
import utils
import make_choice as chs
import see_table as tbl


st.set_page_config(layout="wide")

if 'page_view' not in st.session_state:
    st.session_state['page_view'] = 'Make Choice'

player = utils.fpg_api_get('init_player', email='toby96@sky.com')

player_id = player['player_id']
# player_id = 6

round = utils.fpg_api_static('current_round', player_id=player_id)['Round ID']

round_data = utils.fpg_api_get('get_round_info',
                               round_id=round,
                               player_id=player_id)

round_def = 'Normal Round'

cut_off = round_data['Cut Off']

if round_data['DMM']:
    round_def = 'Draw Means More Round!'

if round_data['Double']:
    round_def = 'Double Points Round!'

if round_data['DMM'] and round_data['Double']:
    round_def = 'Draw Means Mores AND Double Points Round!!'

if st.sidebar.button('Rules', use_container_width=True):
    rules.view_rules()


st.sidebar.markdown('---')

st.sidebar.caption('Email: {}'.format('toby96@sky.com'))

st.sidebar.caption('Player ID: {}'.format(player_id))

choices = utils.fpg_api_get('get_choices', round_id=round, player_id=player_id)

st.markdown('<h1 style="text-align: center;"> FPG </h1>',
            unsafe_allow_html=True)

text = '<h3 style="text-align: center;"> Round {} - {} </h3>'

st.markdown(text.format(round, round_def),
            unsafe_allow_html=True)

try:
    current_choice = choices[str(player_id)]
    text = '<h5 style="text-align: center;"> Current Choice: {} </h5>'
    st.markdown(text.format(current_choice),
                unsafe_allow_html=True)

    st.sidebar.caption('Cut Off : {}'.format(cut_off))

except BaseException:
    current_choice = None
    text = '<h5 style="text-align:center;"> ‼️ Please make a choice by {} ‼️ </h5>'
    st.markdown(text.format(cut_off),
                unsafe_allow_html=True)

st.markdown('---')

left, right = st.columns(2)

if left.button('Make Choice', use_container_width=True):
    st.session_state['page_view'] = 'Make Choice'

if right.button('See FPG Table', use_container_width=True):
    st.session_state['page_view'] = 'See Standings'

st.markdown(' ')


if st.session_state['page_view'] == 'Make Choice':
    chs.main(player_id, current_choice, round)

if st.session_state['page_view'] == 'See Standings':
    tbl.main(player_id, round)
