#KHD: 25.11.2022

from tiniworld_core.logic.data import Tiniworld
import pandas as pd  #1
import streamlit as st
import numpy as np
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import plotly.express as px

# instanciating Tiniworld class
tini = Tiniworld()

# todo: making the dot bigger based on the qty of that location if possible

#st.set_page_config(page_title="Plotting Demo", page_icon="📈", layout="wide")

tiniworldLocations = st.container()
allLocations = st.container()

def show_line_plot(df):
    # Plotly figure 1
    df_con_3 = df
    fig_3 = px.line(df_con_3, x='docDate', y='qty',
                  color="store_code",
                  line_group="store_code", hover_name="store_code")
    fig_3.update_layout(title='Footfall, locations' , showlegend=True)
    return fig_3


with tiniworldLocations:
    st.header('Tiniworld location')
    location_file = "/Users/khoado/code/khdb/tiniworld_timeseries_forecast/raw_data/tw_location_info.csv" #Load OK

    #dtypes = {'store_code': object, 'shortName': object, 'city': object, 'country': object, 'latitude': float, 'longitude': float,}
    df_locations = pd.read_csv(location_file)
    df_locations = df_locations[['latitude', 'longitude']]
    #df_locations['latitude'] = df_locations['latitude'].astype(float)
    #df_locations['longitude'] = df_locations['longitude'].astype(float)

    st.map(df_locations)
    #st.write(df_locations)



with allLocations:
  st.header('Historical Data (Footfall)')
  st.text('Showing the footfall of all centers from historical data!')

  store_names = tini.get_store_names()
  #st.text('Here is a list of all Stores: ')
  #st.text(store_names)

  all_locations_dict = tini.get_stores_ds_alltime()
  stores_selected = st.multiselect("Select one or multiple locations", store_names)

  if st.button("Run!"):
      st.write(f'{stores_selected} - ready to run...' )

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
      st.write(fig_2)
      #st.write(df_con)

      st.write(show_line_plot(df_con))

      #st.text("Showing line plot")
      ##df_con_3 = df_con
      #df_con_3 = df_con.copy()
      #df_con_3.set_index('ds', inplace=True)
      #df_con_3 = df_con_3.resample('M').sum() #last()  #.sum() works
      #fig_3 = px.line(df_con_3)
      #st.write(fig_3)
      #st.write(df_con_3)
