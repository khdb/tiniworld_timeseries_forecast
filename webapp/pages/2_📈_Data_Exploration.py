import pandas as pd  #1
import streamlit as st
import numpy as np
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import plotly.express as px
from prophet import Prophet
from prophet.plot import plot_cross_validation_metric, performance_metrics, plot_yearly, plot_weekly
from plotly.subplots import make_subplots

from tiniworld_core.logic.data import Tiniworld
from webapp.methods import AppFunktion

st.set_page_config(page_title="Data Exploration", page_icon="📈", layout="wide", initial_sidebar_state = "expanded")

# instanciating Tiniworld class
tini = Tiniworld()
AF = AppFunktion()

with st.sidebar:
    AF.sidebar()
    AF.sidebare_2()

c = st.session_state.store_c
n = st.session_state.store

dataExploration = st.container()


with dataExploration:
    col1, col2, col3 = st.columns([4,3,1])

    with col1:
        '''### Tiniworld information'''

    with col2:
        f'''
        Store name: {st.session_state.store_name} \n
        Store code: {st.session_state['store']} '''

    with col3:
        st.image(
            "https://theme.hstatic.net/200000113805/1000623432/14/image_partner2.png",
            width=80,
        )


    col1, col2, col3,col4,col5,col6 = st.columns(6)
    col6.metric("Ticket sales today (Trend)", f"{round(st.session_state.sale_today)} ", f"{st.session_state.trend_today}")
    col3.metric("Median percentage of kids", f"{round(st.session_state.ratio*100,2)} %", "")
    col2.metric("Ticket sales overall", f"{st.session_state.sale_overall}")
    col4.metric('Median sale per day open', f"{round(st.session_state.sale_overall/st.session_state.number_of_days)}")
    col1.metric('Company rank', f'{st.session_state.rank}')
    col5.metric(f'Open days since Jan 2020',f'{st.session_state.number_of_days}',f'{round(st.session_state.number_of_days/st.session_state.period*100)}%')


#plot sales
    fig0 = tini.plot_sales(st.session_state.store)
    fig0.update_layout(width=1000)
    st.write(fig0)

#plot trend
    fig1 = tini.plot_trend(st.session_state.store,0)
    if st.session_state.compare:
        fig2 = tini.plot_trend(c)
        fig2.data[0].marker['color'] = 'green'
        fig2.data[0].name = f'compare to {c}'
        fig1.add_trace(fig2.data[0])
        fig1.data[0].name = f'Trend for {n}'
    fig1.update_layout(width=1000)
    st.write(fig1)

# plot monthly chart
    if st.session_state.compare == True:
        fig2_s = make_subplots(specs=[[{"secondary_y": True}]])
        fig2 = tini.plot_monthly(n)
        fig2_c = tini.plot_monthly(c)
        fig2_c.data[0].line['color'] = st.session_state.color
        fig2_c.data[0].name = f'compare to {c}'
        fig2.data[0].name = f'Trend for {n}'
        fig2_s.add_trace(fig2.data[0],secondary_y= False)
        fig2_s.add_trace(fig2_c.data[0],secondary_y=True)
    else:
        fig2_s = tini.plot_monthly(st.session_state.store)
    fig2_s.update_layout(
                        yaxis_title="Trend",
                        xaxis_title="Day of year",
                        title=f"Yearly sales trend",
                        template= "plotly_white",
                        width = 1000
                        )
    st.write(fig2_s)

# plot weekly chart
    fig3 = tini.plot_weekday(n)
    if st.session_state.compare == True:
        fig3_c = tini.plot_weekday(c)
        fig3_c.data[-1].marker['color'] = 'green'
        fig3_c.data[-1].name = f'compare to {c}'
        fig3.data[-1].name = f'Absolute for {n}'
        fig3.add_trace(fig3_c.data[-1])
        y_max = int(np.max([fig3_c.data[-1]['y'].max(),fig3.data[-2]['y'].max()])*1.1)
        fig3.layout['yaxis']['range'] = (0,y_max)


    fig3.update_layout(width=1000)
    st.write(fig3)
