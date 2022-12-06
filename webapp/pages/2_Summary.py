
import pandas as pd  #1
import streamlit as st
import numpy as np
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import plotly.express as px
from prophet import Prophet
from prophet.plot import plot_cross_validation_metric, performance_metrics, plot_yearly, plot_weekly


from tiniworld_core.logic.data import Tiniworld
from webapp.methods import AppFunktion

# instanciating Tiniworld class
tini = Tiniworld()
AF = AppFunktion()

st.set_page_config(page_title="Data Exploration", page_icon="📈", layout="wide")

with st.sidebar:
    AF.sidebar()


dataExploration = st.container()



with dataExploration:
    st.header(f'Tiniworld Information')
    f'''
    Store Name: {st.session_state.store_name} \n
    Store No: {st.session_state['store']} \n'''

    col1, col2, col3,col4,col5,col6 = st.columns(6)
    col6.metric("Ticket Sales Today (Trend)", f"{round(st.session_state.sale_today)} ", f"{st.session_state.trend_today}")
    col3.metric("Median percentage of Kids", f"{round(st.session_state.ratio*100,2)} %", "")
    col2.metric("Ticket Sales Overall", f"{st.session_state.sale_overall}")
    col4.metric('Median Sale per day open', f"{round(st.session_state.sale_overall/st.session_state.number_of_days)}")
    col1.metric('Company rank', f'{st.session_state.rank}')
    col5.metric(f'Open days since jan 2020',f'{st.session_state.number_of_days}',f'{round(st.session_state.number_of_days/st.session_state.period*100)}%')


    fig = tini.plot_trend(st.session_state.store,0)
    fig.update_layout(width=1000)
    st.write(fig)

    fig1 = tini.plot_sales(st.session_state.store)
    fig1.update_layout(width=1000)
    st.write(fig1)

    fig2 = tini.plot_monthly(st.session_state.store)
    fig2 = tini.plot_monthly('TW-PS004')
    fig2.update_layout(width=1000)
    st.write(fig2)

    fig3 = tini.plot_weekday(st.session_state.store)
    fig3.update_layout(width=1000)
    st.write(fig3)
