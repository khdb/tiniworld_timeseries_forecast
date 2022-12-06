#KHD: 25.11.2022

from tiniworld_core.logic.data import Tiniworld
import pandas as pd  #1
import streamlit as st
import numpy as np
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Home", page_icon="📈", layout="wide")

siteHeader = st.container()
projectGoalPlot = st.container()
projectGoal = st.container()


# instanciating Tiniworld class
tini = Tiniworld()

def project_goal_fig():
    #pass
    all_stores_dict = tini.get_stores_ds_alltime()
    the_store_df = all_stores_dict['TW-PS002']

    the_store_df['date'] = pd.to_datetime(the_store_df['ds']) #.dt.strftime('%y-%m-%d')
    the_store_df['docDate'] = pd.to_datetime(the_store_df['ds']) #.dt.strftime('%y-%m-%d')
    the_store_df.set_index('date', inplace=True)
    #the_store_df = the_store_df.resample('Y').last()  #.sum() works

    # Don't care about week days or weekends, use all date from store_code = 'TW-PS002' (tW Aeon Tân Phú)
    #df_tanphu = df[ (df['store_code'] == 'TW-PS002') ]
    known = the_store_df.loc['2021-01-01':'2021-01-08']
    unknown = the_store_df.loc['2021-01-08':'2021-01-15']
    to_predict = the_store_df.loc['2021-01-09':'2021-01-09']

    #Group the date
    known = known.groupby(['docDate']).sum(['qty']) #['qty']
    unknown = unknown.groupby(['docDate']).sum(['qty']) #['qty']
    to_predict = to_predict.groupby(['docDate']).sum(['qty']) #['qty']

    #Plotting
    fig_x, ax_ = plt.subplots()
    known.plot(ax=ax_, c='c', marker='o', zorder=3)
    unknown.plot(ax=ax_, c='grey', alpha=0.5)
    to_predict.plot(ax=ax_, c='red', marker='o', markersize=12,
                    linestyle='-')

    ax_.legend(['known', 'future', 'value to predict'])
    ax_.set_ylabel('# Ticket sales')
    ax_.set_xlabel('Date')
    #st.pyplot(fig_x)

    #px.line(unknown, x=unknown.index, y='qty', title='Forecast')
    # Plotly figure 1
    fig = px.line(known, x=known.index, y='qty', title='Forecast')

    # Plotly figure 2
    fig2 = go.Figure(fig.add_traces(
                     data=px.line(unknown, x=unknown.index, y='qty',
                                  line_dash='qty', hover_name="qty" )._data))
    fig2.update_layout(title='Productivity, Europe and America', showlegend=False)

    trace1 = go.Line(
        x=known.index,
        y=known['qty'],
        name='known',
        marker=dict(
            color='rgb(34,163,192)'
               )
    )
    trace2 = go.Line(
        x=unknown.index,
        y=unknown['qty'],
        name='unknown',
        yaxis='y2',
        opacity=0.3,
        mode="lines+markers",
        marker=dict(
            color='rgb(234,163,192)'
            #,alpha=0.5
               )

    )
    trace3 = go.Line(
        x=to_predict.index,
        y=to_predict['qty'],
        name='value to predict',
        yaxis='y2',
        marker=dict(
            color='rgb(34,163,100)',
            size=15
               )
    )

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(trace1)
    fig.add_trace(trace2)
    fig.add_trace(trace3)

    fig.update_layout(height=300,
                         margin={'l': 20, 'r': 60, 't': 10, 'b': 20})
    return fig




#KHD experimental
# Using "with" notation
with st.sidebar:
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )

    form1 = st.sidebar.form(key="Options")
    form1.header("Params")

    store_names = tini.get_store_names()
    all_locations_dict = tini.get_stores_ds_alltime()
    stores_selected_2 = form1.multiselect("Select one or multiple locations", store_names)

    run_btn = form1.form_submit_button("Run!")

    if run_btn:
        if "stores_selected_2" not in st.session_state:
            st.session_state["prev_word_count"] = stores_selected_2


with siteHeader:
  st.title('Data Science project with Timeseries Data')
  #st.text('In this project We look into Forecast and Prediction with Time-series data. We worked with the dataset from a Kids Entertainment and Attractions center')
  st.text(st.session_state["prev_word_count"])

  st.markdown('''
In this project we look into Forecast and Prediction with Time-series data.
We worked with the dataset from a Kids Entertainment and Attractions center

''')

with projectGoalPlot:
   st.header('Project Goal')
   st.text("What do we want to have as the outcomes?")
   st.write(project_goal_fig())

#with projectGoal:
#  st.header('Project Goal')
#  st.text("What do we want to have as the outcomes?")
#  all_stores_dict = tini.get_stores_ds_alltime()
#  the_store_df = all_stores_dict['TW-PS002']
#
#  the_store_df['date'] = pd.to_datetime(the_store_df['ds']) #.dt.strftime('%y-%m-%d')
#  the_store_df['docDate'] = pd.to_datetime(the_store_df['ds']) #.dt.strftime('%y-%m-%d')
#  the_store_df.set_index('date', inplace=True)
#  #the_store_df = the_store_df.resample('Y').last()  #.sum() works
#
#  # Don't care about week days or weekends, use all date from store_code = 'TW-PS002' (tW Aeon Tân Phú)
#  #df_tanphu = df[ (df['store_code'] == 'TW-PS002') ]
#  known = the_store_df.loc['2021-01-01':'2021-01-08']
#  unknown = the_store_df.loc['2021-01-08':'2021-01-15']
#  to_predict = the_store_df.loc['2021-01-09':'2021-01-09']
#
#  #Group the date
#  known = known.groupby(['docDate']).sum(['qty'])['qty']
#  unknown = unknown.groupby(['docDate']).sum(['qty'])['qty']
#  to_predict = to_predict.groupby(['docDate']).sum(['qty'])['qty']
#
#  #Plotting
#  #known.drop(columns='y', inplace=True)
#  #unknown.drop(columns='y', inplace=True)
#  #to_predict.drop(columns='y', inplace=True)
#
#  fig_x, ax_ = plt.subplots()
#  known.plot(ax=ax_, c='c', marker='o', zorder=3)
#  unknown.plot(ax=ax_, c='grey', alpha=0.5)
#  to_predict.plot(ax=ax_, c='red', marker='o', markersize=12,
#                  linestyle='-')
#
#  ax_.legend(['known', 'future', 'value to predict'])
#  ax_.set_ylabel('# Ticket sales')
#  ax_.set_xlabel('Date')
#  st.pyplot(fig_x)
#
#  #st.write(known)
#  #st.write(to_predict)
#  #st.write(unknown)
#  #st.write(the_store_df)
#
