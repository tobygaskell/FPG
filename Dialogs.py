import streamlit as st
import utils

@st.dialog('Update Choice')
def update_choice(team_choice, player_id, round_id):
    '''
    '''
    updated = False
    st.write('You have already submitted a choice for this round.')

    st.write('Would you like to resubmit and update your choice to be {} for round {} ?'.format(team_choice, round_id))

    left, right = st.columns(2)

    if left.button('Yes', use_container_width=True):

        data = {'Player' : player_id, 
                'Choice' : team_choice, 
                'Round'  : round_id}
        
        updated = utils.fpg_api('update_choice', data)['Updated']

        # st.rerun()

        if updated: 
            st.success('You have updated your choices to {} for round {} - Thankyou for playing!'.format(team_choice, round_id))

    if right.button('No', use_container_width= True): 
        st.rerun()

    return updated 