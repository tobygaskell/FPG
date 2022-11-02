import streamlit as st 

with open('Rules.md') as file: 
        
    text = file.read() 

st.image('5.png', width = 100)

st.markdown(text)

