import streamlit as st 
import requests as r


def fpg_api(endpoint, data = None):
    '''
    '''
    url = st.secrets['fpg']['host']

    if data == None:
        response = r.get(url + endpoint).json()

    else:
        response = r.post(url + endpoint, json = data).json()
        # st.write(response)
    return response

@st.cache_data(ttl = 600)
def fpg_api_static(endpoint, data = None):
    '''
    '''
    url = st.secrets['fpg']['host']

    if data == None:
        response = r.get(url + endpoint).json()

    else:
        response = r.post(url + endpoint, json = data).json()
    return response
