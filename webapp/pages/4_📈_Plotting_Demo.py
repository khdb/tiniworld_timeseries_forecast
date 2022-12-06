import pandas as pd  #1
import streamlit as st
import numpy as np
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

from tiniworld_core.logic.data import Tiniworld
from webapp.methods import AppFunktion

# instanciating Tiniworld class
tini = Tiniworld()
AF= AppFunktion()

st.set_page_config(page_title="Make Forecast", page_icon="📈", layout="wide")


with st.sidebar:
    AF.sidebar()



plotingDemoLine = st.container()
plotingDemo = st.container()

def plot_it_here(df):
    pass

    return df


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


def plot_forecast(location,forecast=60):
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
        #fig = go.Figure()
        #fig = px.Figure()
        #fig = ff.Figure()

        #fig = px.bar(df_con, x='store_code', y='qty', color='store_code',
        #             animation_frame="date", animation_group="store_code",
        #             range_y=[0,500])
        #fig.update_layout(width=800)


        #fig.add_trace(
        #    #go.Scatter(x=list(future.ds), y=list(future.yhat)))
        #    px.Scatter(x=list(future.ds), y=list(future.yhat)))

        fig = px.scatter(x=list(future.ds), y=list(future.yhat))

        # Set title
        fig.update_layout(
            title_text="Tickets sold in the last 2 years and forecast for 2 month"
        )

        #update layout to show the predction part showing the future footfall
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

        #return the plotly fig object to use in the calling functions to insert in st.write()
        fig.update_layout(width=800)
        return fig




with plotingDemo:
    st.header('Ploting demo with Plotly in Streamlit')
    st.text('Plot forecast and components of Timeseries!')

    all_stores_dict = tini.get_stores_ds_alltime()
    df = all_stores_dict['TW-PS002']

    #result = plot_it_here(df)
    #result = plot_forecast('TW-PS002',forecast=60) #OK
    result = plot_forecast_david('TW-PS002',forecast=60)

    #st.write(result)
    st.plotly_chart(result)

with plotingDemoLine:
    st.header('line graph')

    #store_names = tini.get_store_names()
    #st.text('Here is a list of all Stores: ')
    #st.text(store_names)

    all_locations_dict = tini.get_stores_ds_alltime()
    #stores_selected =  '' #st.multiselect("Select one or multiple locations", store_names)
    stores_selected = ['TW-PS002', 'TW-PS005', 'TW-PS008' ]

    #if st.button("Run!"):
    #st.write(f'{stores_selected} - ready to run...' )
    #loop over the selected locations
    #df_con = pd.DataFrame()
    list_of_df = []

    for tw in stores_selected:
         df = all_locations_dict[tw]
         list_of_df.append(df)

    #df_con = pd.concat([all_locations_dict['TW-PS002'],
    #                   all_locations_dict['TW-PS005'],
    #                   all_locations_dict['TW-PS008']]) #OK

    df_con = pd.concat(list_of_df)
    #st.write(df_con)
    #add a date column formated date for plotting (without hour, minutes, sec)
    df_con['date'] = pd.to_datetime(df_con['ds']).dt.strftime('%y-%m-%d')
    #df_con.set_index('ds', inplace=True)
    #df_con = df_con.resample('M').last()  #.sum() works
    fig_2 = px.bar(df_con, x='store_code', y='qty', color='store_code',
                   animation_frame="date", animation_group="store_code",
                   range_y=[0,500])
    fig_2.update_layout(width=800)

    #st.write(fig_2)

    #st.write(df_con)
    st.text("Showing line plot")
    #df_con_3 = df_con
    df_con_3 = df_con.copy()
    #df_con_3.set_index('ds', inplace=True)
    #df_con_3 = df_con_3.resample('M').sum() #last()  #.sum() works

    # make a crosstab
    #tw_crosstab = pd.crosstab(df_con_3['docDate'], df_con_3['store_code'])
    #fig_3 = px.line(tw_crosstab)

    # Plotly figure 1
    fig_3 = px.line(df_con_3, x='docDate', y='qty',
                  color="store_code",
                  line_group="store_code", hover_name="store_code")
    fig_3.update_layout(title='Footfall, locations' , showlegend=True)

    #fig_3 = go.Figure([go.Scatter(x=df_con_3['ds'], y=df_con_3['qty'])])

    st.write(fig_3)
    st.write(df_con_3)
