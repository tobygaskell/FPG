import streamlit as st
import utils
import pandas as pd
import Dialogs
import vis


def main(player_id, current_choice, round):
    '''
    '''
    submitted = False

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

            text = 'You have submitted {} as your choice for round {}!'

            st.success(text.format(team_choice, round))

        elif submitted['Submitted'] == 'Already Chosen':
            Dialogs.update_choice(team_choice, player_id,
                                  round,
                                  current_choice)

        elif submitted['Submitted'] == 'Too Late':

            st.error('Too Late - It\'s past the cut off time for submitting a \
choice for round {}! Come back after the games have finished.'.format(round))

        else:
            st.error('There was an issue submitting your choice')

    st.markdown('---')

    with st.expander('See Previous Picks'):

        see_points = st.toggle('Points Earned', value=False)

        if not see_points:
            previous_choices = utils.fpg_api_get('get_previous_choices',
                                                 player_id=player_id)

            prev = pd.DataFrame(previous_choices)

            prev['1st Pick'] = prev['1st Pick'].map(lambda x: bool(x))
            prev['2nd Pick'] = prev['2nd Pick'].map(lambda x: bool(x))

            prev = prev.style.apply(lambda x: vis.highlight_choices(x), axis=1)

            st.dataframe(prev, use_container_width=True, hide_index=True)
        else:
            previous_points = utils.fpg_api_get('get_previous_points',
                                                player_id=player_id)

            prev = pd.DataFrame(previous_points)

            prev = (prev.style
                    .map(vis.color_totals, subset=['1st Pick'], inc_zero=True)
                    .map(vis.color_totals, subset=['2nd Pick'], inc_zero=True)
                    .format({'1st Pick': '{:.0f}',
                            '2nd Pick': '{:.0f}'}))
            try:
                st.dataframe(prev,
                             use_container_width=True,
                             hide_index=True)

            except TypeError:
                st.error('No Points Earned')
