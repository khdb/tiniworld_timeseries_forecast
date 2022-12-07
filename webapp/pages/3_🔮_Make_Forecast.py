
from tiniworld_core.logic.data import Tiniworld
from webapp.methods import AppFunktion
import pandas as pd  #1
import streamlit as st
import numpy as np
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(page_title=f"Forecast", page_icon="🔮", layout="wide",initial_sidebar_state = "expanded")


# instanceating Tiniworld class
tini = Tiniworld()
AF = AppFunktion()


with st.sidebar:
    AF.sidebar()

modelPrediction = st.container()

with modelPrediction:
    col1, col2, col3 = st.columns([4,3,1])

    with col1:
        '''### Forecast on footfall for a location'''

    with col2:
        f'''
        Store name: {st.session_state.store_name} \n
        Store nr: {st.session_state['store']} '''

    with col3:
        st.image(
            "https://theme.hstatic.net/200000113805/1000623432/14/image_partner2.png",
            width=80,
        )

    #st.text('Here you can select the location name and number of days to forecast in the future!')


    # period_to_forecast = st.slider('What should be the number of days in the future to predict?',
    #     min_value=60, max_value=365,
    #     value=60,
    #     step=1)


    # if st.button("Make Forecast"):
    #     #st.write(f'{st.session_state.store} - {period_to_forecast}' )

    #Ploting the graph
    period_to_forecast = 365
    fig_fc = tini.plot_forecast(st.session_state.store, period_to_forecast)

    fig_fc.update_layout(width=1000)
    st.write(fig_fc)
