import streamlit as st
import Rules as rules
import pandas as pd
import utils
import Dialogs
import vis

st.set_page_config(layout="wide")

if 'page_view' not in st.session_state:
    st.session_state['page_view'] = 'Make Choice'

player = utils.fpg_api_get('init_player', email=st.experimental_user.email)

# palyer_id = player['player_id']
player_id = 6

round = utils.fpg_api_static('current_round', player_id=player_id)['Round ID']

round_data = utils.fpg_api_get('get_round_info',
                               round_id=round,
                               player_id=player_id)

round_def = 'Normal Round'
submitted = False

if round_data['DMM']:
    round_def = 'Draw Means More Round!'

if round_data['Double']:
    round_def = 'Double Points Round!'

if round_data['DMM'] and round_data['Double']:
    round_def = 'Draw Means Mores AND Double Points Round!!'

if st.sidebar.button('Rules', use_container_width=True):
    rules.view_rules()

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

except BaseException:
    current_choice = None
    text = '<h3 style="text-align:center;"> 💥 Please make a choice 💥 </h3>'
    st.markdown(text,
                unsafe_allow_html=True)

st.markdown('---')

left, right = st.columns(2)

if left.button('Make Choice', use_container_width=True):
    st.session_state['page_view'] = 'Make Choice'

if right.button('See FPG Table', use_container_width=True):
    st.session_state['page_view'] = 'See Standings'

st.markdown(' ')

st.sidebar.markdown('---')

st.sidebar.caption('Email: {}'.format(st.experimental_user.email))

st.sidebar.caption('Player ID: {}'.format(player_id))

if st.session_state['page_view'] == 'Make Choice':

    fixtures = utils.fpg_api_get('get_fixtures',
                                 round_id=round,
                                 player_id=player_id)

    fix = pd.DataFrame(fixtures)

    fix['vs'] = fix['DERBY'].map(lambda x: '-' if not x else '⚔️')

    fix['Fixtures'] = (fix['HOME_TEAM'] +
                       ' ' +
                       fix['vs'] +
                       ' ' +
                       fix['AWAY_TEAM'])

    fix.rename(columns={'HOME_LOGO': ' ',
                        'AWAY_LOGO': '  '},
               inplace=True)

    st.caption('⚔️ means this fixture is a derby')

    st.dataframe(fix[[' ', 'Fixtures', '  ']], column_config={
        " ": st.column_config.ImageColumn(),
        "  ": st.column_config.ImageColumn()},
        use_container_width=True, hide_index=True)

    teams = utils.fpg_api_get('get_available_choices', player_id=player_id)

    with st.expander('See Previous Picks'):

        previous_choices = utils.fpg_api_get('get_previous_choices',
                                             player_id=player_id)

        prev = pd.DataFrame(previous_choices)

        prev['1st Pick'] = prev['1st Pick'].map(lambda x: bool(x))
        prev['2nd Pick'] = prev['2nd Pick'].map(lambda x: bool(x))

        st.dataframe(prev, use_container_width=True, hide_index=True)

    with st.form('Choice', border=False):
        team_choice = st.selectbox('Pick a Team:',
                                   [team['TEAM_NAME'] for team in teams])

        if st.form_submit_button('Submit', use_container_width=True):

            data = {'Player': player_id,
                    'Choice': team_choice,
                    'Round': round}

            submitted = utils.fpg_api_post('make_choice', data)

    if submitted:
        if submitted['Submitted'] is True:

            text = 'You have submitted {} as you choice for round {}!'

            st.success(text.format(team_choice, round))

        elif submitted['Submitted'] == 'Already Chosen':
            Dialogs.update_choice(team_choice, player_id,
                                  round,
                                  current_choice)

        elif submitted['Submitted'] == 'Too Late':

            st.error('Too Late - It\'s past the cut off time for submitting a \
choice for round {}! Come back after the games have finished.'.format(round))

        else:
            st.error('There was an issue submitting your choicer')

if st.session_state['page_view'] == 'See Standings':

    stand = utils.fpg_api_get('get_standings', player_id=player_id)

    standings = pd.DataFrame(stand)

    standings['Position'] = (standings['Position']
                             .map(lambda n: "%d%s" %
                             (n, "tsnrhtdd"[(n//10 % 10 != 1) *
                                            (n % 10 < 4) * n % 10::4])))

    standings = standings.set_index('player_id', drop=True)

    st.subheader('Overall Table', divider='grey')

    if st.toggle('See Goal Difference'):
        standings = standings[['Position', 'User', 'Goal Diff', 'Score']]

    else:
        standings = standings[['Position', 'User', 'Score']]

    styled_standings = (standings.style
                        .apply(lambda x: vis.highlight_row(x, player_id),
                               axis=1))

    st.dataframe(styled_standings,
                 use_container_width=True,
                 hide_index=True)

    st.subheader('Points Details', divider='grey')

    round_ops = [i+1 for i in range(round-1)]

    round_ops.sort(reverse=True)

    round_choice = st.selectbox('Pick a Round: ', round_ops)

    points = utils.fpg_api_get('get_points',
                               round_id=round_choice,
                               player_id=player_id)

    points = pd.DataFrame(points)

    if len(points) != 0:

        round_info = utils.fpg_api_get('get_round_info',
                                       round_id=round_choice,
                                       player_id=player_id)

        left, right = st.columns(2)
        left.button('Draw Means More Round',
                    disabled=not round_info['DMM'],
                    use_container_width=True,
                    type='primary')

        right.button('Double Points Round',
                     disabled=not round_info['Double'],
                     use_container_width=True,
                     type='primary')

        points = points.set_index('player_id', drop=True)

        styled_points = (points.style
                         .apply(lambda x: vis.highlight_row(x, player_id),
                                axis=1)
                         .applymap(vis.color_results,
                                   subset=['Result'])

                         .applymap(vis.color_totals,
                                   subset=['Total'],
                                   inc_zero=True)

                         .applymap(vis.color_totals,
                                   subset=['Subtotal'],
                                   inc_zero=True)

                         .applymap(vis.color_totals,
                                   subset=['Basic'],
                                   inc_zero=True)

                         .applymap(vis.color_totals,
                                   subset=['Head 2 Head'],
                                   inc_zero=True)

                         .applymap(vis.color_totals,
                                   subset=['Derby'],
                                   inc_zero=True)

                         .applymap(vis.color_totals,
                                   subset=['Draw Means More'],
                                   inc_zero=True))

        st.dataframe(styled_points,
                     use_container_width=True,
                     hide_index=True)

    else:
        st.warning('Score not yet calculated for this round - come back soon!')

    st.subheader('Charts', divider='grey')

    chart_choice = st.radio('Pick Chart Type',
                            ['Score', 'Position'],
                            horizontal=True,
                            label_visibility='collapsed')

    stand = utils.fpg_api_get('get_rolling_standings', player_id=player_id)

    df = pd.DataFrame(stand)

    fig = vis.linechart(df, chart_choice,
                        False if chart_choice == 'Score' else True)

    st.plotly_chart(fig, config={'displayModeBar': False})
