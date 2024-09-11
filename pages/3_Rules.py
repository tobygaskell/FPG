import streamlit as st 
import pandas as pd 
# from streamlit_extras.switch_page_button import switch_page



st.subheader('Overall Rules', divider = True, anchor = False)


# st.markdown(text)


# with tab[0]:
with open('Rules/Rules.md') as file: 
    text = file.read()

# st.markdown(text)

data = {'Result':['🥇 - Win', '❌ - Lose', '🤝 - Draw'], 
        'Points': ['+1', '-1', '0']}

st.write('Each week you will pick a team you hope will earn you the most points - depending on the result \
     from that weekends games you will earn the points below.')

st.dataframe(data, use_container_width = True, hide_index = True)

st.write('However - be careful when you pick a specific team because you can\'t pick the same team more than twice a season.')

st.subheader('Extra Rules', divider = True, anchor = False)

tab = st.tabs(['Double Point Round', 'Head 2 Head Game', 'Draw Means More Round', 'Derby Game'])

cont_height = 310

with tab[0]:
    with st.container(height = cont_height, border = False):

        with open('Rules/Double.md') as file: 
            text = file.read()
        
        st.markdown(text)

with tab[1]:
    with st.container(height = cont_height, border = False):    
        with open('Rules/H2H.md') as file: 
            text = file.read()

        st.markdown(text)

        data = {'Result': ['🥇 - Win', '❌ - Lose', '🤝 - Draw'], 
                'Points': ['+1', '-1', '0']}

        st.dataframe(data, use_container_width = True, hide_index = True)

        st.write('However bare in mind that you wont know what teams everyone else has picked until after the games for that week have finished.')

with tab[2]:
    with st.container(height = cont_height, border = False):   
        with open('Rules/Draw.md') as file: 
            text = file.read()

        st.markdown(text)

        data = {'Result':['🥇 - Win', '❌ - Lose', '🤝 - Draw'], 
                'Points': ['0', '0', '+2']}

        st.dataframe(data, use_container_width = True, hide_index = True)
with tab[3]:
    with st.container(height = cont_height, border = False):   
        with open('Rules/Derby.md') as file: 
            text = file.read()

        st.markdown(text)

        data = {'Result':['🥇 - Win', '❌ - Lose', '🤝 - Draw'], 
                'Points': ['+1', '-1', '-1']}

        st.dataframe(data, use_container_width = True, hide_index = True)


st.subheader('Example', divider = True, anchor = False)
# with tab[4]:
with open('Rules/Example.md') as file: 
    text = file.read()

st.markdown(text)

data = {'Player':['Lucas', 'Will', 'Dustin', 'Mike'], 
        'Choice': ['Manchester United', ' Manchester City', 'Chelsea', 'Tottenham'], 
        'Basic': ['+1', '-1', '0', '0'], 
        'H2H': ['+1', '-1', '0', '0'], 
        'Derby': ['+1', '-1', '0', '-1'], 
        'DMM': ['0', '0', '+2', '+2'], 
        'Sub Total': ['+3', '-3', '+2', '+1'], 
        'Doubled?': [True, True, True, True], 
        'Total': ['+6', '-6', '+4', '+2'], 
        }

st.dataframe(data, use_container_width = True, hide_index = True)