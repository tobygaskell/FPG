import streamlit as st


st.title('Hi Streamlit this is my first app')

st.text_input("Team Choice", key = "choice")

st.write('you have chosen: ' + st.session_state.choice) 