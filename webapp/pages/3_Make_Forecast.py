
from tiniworld_core.logic.data import Tiniworld
from webapp.methods import AppFunktion
import pandas as pd  #1
import streamlit as st
import numpy as np
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

# instanciating Tiniworld class
tini = Tiniworld()
AF = AppFunktion()

st.set_page_config(page_title=f"Make Forecast {st.session_state.store}", page_icon="📈", layout="wide")


st.session_state['df_ratio']

with st.sidebar:
    AF.sidebar()




f'''
    Store number is {st.session_state['store']}'''

modelPrediction = st.container()





def plot_forecast_new(location,forecast=60):
    #KHD for demo
    #all_stores_dict = tini.get_stores_ds_alltime()
    #df = all_stores_dict['TW-PS002']

    #tw_location = 'TW-PS002'
    fig_x = tini.plot_forecast(location, forecast=60)

    return fig_x


def plot_forecast_david(location,forecast=60):
    '''
    forecast = int(number of days to forecast)
    location = str(store code)
    '''
    #get all Data
    #df_all = self.get_stores_ds_alltime()
    #select one location
    #df = df_all[location]

    #KHD for demo
    all_stores_dict = tini.get_stores_ds_alltime()
    df = all_stores_dict['TW-PS002']


    future = tini.predict_model(location,forecast)
    fc_time = (future.ds.max()-df.ds.max()).days
    layout = {
        # to highlight the forecast we use shapes and create a rectangular
        'shapes': [
            {
                'type': 'rect',
                # x-reference is assigned to the x-values
                'xref': 'x',
                # y-reference is assigned to the plot paper [0,1]
                'yref': 'paper',
                'x0': df.ds.max(),
                'y0': 0,
                'x1': future.ds.max(),
                'y1': 1,
                'fillcolor': '#ff9900', # color is orange
                'opacity': 0.5,
                'line': {
                    'width': 0,
                }
            }
        ]
    }
    # Create figure
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=list(future.ds), y=list(future.yhat)))
    # Set title
    #fig.update_layout(
    #    title_text="Tickets sold in the last 2 years and forecast for 2 month"
    #)
    fig.update_layout(layout)
    # Add range slider with 2 options : forecast and all
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=fc_time-1,
                        label="forecast",
                        step="day",
                        stepmode="todate"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    #fig.show()
    fig.update_layout(height=200,
                         margin={'l': 20, 'r': 60, 't': 10, 'b': 10})
    return fig



with modelPrediction:
  st.header('Making Forecast on footfall for a Location')
  st.text('Here you can select the location name and number of days to forecast in the future!')

  store_names = tini.get_store_names()
  #st.text('Here is a list of all Stores: ')
  #st.text(store_names)

  store_name_select = st.selectbox("Select a location", store_names)

  period_to_forecast = st.slider('What should be the number of days in the future to predict?',
      min_value=10, max_value=100,
      value=20,
      step=10)

#  number_of_trees = st.selectbox('How many trees should there be?',
#      options=[100,200,300,'No limit'],
#      index=0)

  if st.button("Make Forecast"):
      st.write(f'{store_name_select} - {period_to_forecast}' )
      # Load prediction model for this store
      #model = tini.load_model(store_name_select)
      # since 01.12.2022 we dont need to load the model anymore, just give the location_name
      # the prediction method will do the model loading behind the scenes

      forecast = tini.predict_model(store_name_select, period_to_forecast) #make prediction for 90 days

      #Ploting the graph
      plot_fig = plot_forecast_david(store_name_select, period_to_forecast)
      st.plotly_chart(plot_fig)

      # for debugging/prototyping, showing the DF
      st.write(forecast)
      #fig2 = model.plot_components(forecast)
      #st.plotly_chart(figure_or_data, use_container_width=False, sharing="streamlit", theme=None, **kwargs)
      #st.plotly_chart(fig2)

      # 05.12.2022
      fig_x = plot_forecast_new(store_name_select, period_to_forecast)
      st.plotly_chart(fig_x)
