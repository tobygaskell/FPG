import streamlit as st
import utils


@st.dialog('Update Choice')
def update_choice(team_choice, player_id, round_id, current_choice):
    '''
    '''
    updated = False

    text = 'You have already submitted {} for this round.'

    st.write(text.format(current_choice))

    text = 'Would you like to update your choice to be {} for round {} ?'

    st.write(text.format(team_choice, round_id))

    left, right = st.columns(2)

    if left.button('Yes', use_container_width=True):

        data = {'Player': player_id,
                'Choice': team_choice,
                'Round': round_id}

        updated = utils.fpg_api_post('update_choice', data)['Updated']

        if updated:
            text = 'You have updated your choices to {} for round {}!'

            st.success(text.format(team_choice, round_id))

    if right.button('No', use_container_width=True):
        st.rerun()

    return updated
