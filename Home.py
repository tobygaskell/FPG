import streamlit as st 
import utils
from streamlit_extras.switch_page_button import switch_page


# st.set_page_config(layout="wide")

st.image('5.png', width = 100)


round = utils.get_api("https://api-football-v1.p.rapidapi.com/v3/fixtures/rounds", 
                     {"league":"39","season":"2024","current":"true"})[0][-2:].strip()

player_id = utils.check_if_player(st.experimental_user['email'])

st.markdown('# Welcome to FPG - Round {}'.format(round))


query = '''
        SELECT double_point_round, draw_round, 
               dayname(cut_off) || ' ' || day(cut_off) || ' at ' || TO_VARCHAR(cut_off, 'HH12AM') as cut_off 
        FROM rounds 
        where round = {}
        '''.format(round)

round_info = utils.run_static_query(query)

# st.header('hello world')

double_round = round_info['DOUBLE_POINT_ROUND'][0]

draw_round = round_info['DRAW_ROUND'][0]

cutoff = round_info['CUT_OFF'][0]

st.subheader('🔘 DeadLine 💀: {}'.format(cutoff))

st.subheader('🔘 Double Points Round {}'.format('✅' if double_round else '❌' ))

st.subheader('🔘 Draw Round {}'.format('✅' if draw_round else '❌' ))





st.markdown('---')

left, right = st.columns(2)

with left:
    if st.button('Pick Team'):

        switch_page("make choice")

with right: 
    if st.button('Check Standing'):

        switch_page("standings")



