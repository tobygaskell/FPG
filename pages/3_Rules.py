import streamlit as st 
from streamlit_extras.switch_page_button import switch_page

with open('Rules.md') as file: 
        
    text = file.read() 

st.image('5.png', width = 100)

st.markdown(text)

st.markdown('---')

left, right = st.columns(2)

with left:
    if st.button('Pick Team'):

        switch_page("make choice")

with right: 
    if st.button('Home'):

        switch_page("home")