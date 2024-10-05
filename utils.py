import streamlit as st
import requests as r


def fpg_api_get(endpoint, **params):
    '''
    '''
    url = st.secrets['fpg']['host']

    url = url + endpoint + '?'

    for key, value in params.items():

        url = url + '&{}={}'.format(key, value)

    # st.write(url)
    response = r.get(url)

    return response.json()


def fpg_api_post(endpoint, data):
    '''
    '''
    url = st.secrets['fpg']['host']

    response = r.post(url + endpoint, json=data).json()

    return response


@st.cache_data(ttl=600)
def fpg_api_static(endpoint, **params):
    '''
    '''
    url = st.secrets['fpg']['host']

    url = url + endpoint

    for key, value in params.items():

        url = url + '?{}={}'.format(key, value)

    # st.write(url)
    response = r.get(url)

    return response.json()
