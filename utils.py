import streamlit as st
import requests as r
import os


def fpg_api_get(endpoint, **params):
    '''
    '''
    url = st.secrets['fpg']['host']

    url = url + endpoint + '?'

    for key, value in params.items():

        url = url + '&{}={}'.format(key, value)

    auth = (st.secrets['fpg']['api_user'],
            st.secrets['fpg']['api_pass'])

    response = r.get(url, auth=auth)

    return response.json()


def fpg_api_post(endpoint, data):
    '''
    '''
    url = st.secrets['fpg']['host']

    response = r.post(url + endpoint,
                      json=data,
                      auth=(st.secrets['fpg']['api_user'],
                            st.secrets['fpg']['api_pass'])).json()

    return response


@st.cache_data(ttl=600)
def fpg_api_static(endpoint, **params):
    '''
    '''
    url = st.secrets['fpg']['host']

    url = url + endpoint

    for key, value in params.items():

        url = url + '?{}={}'.format(key, value)

    auth = (st.secrets['fpg']['api_user'],
            st.secrets['fpg']['api_pass'])
    response = r.get(url, auth=auth)

    return response.json()
