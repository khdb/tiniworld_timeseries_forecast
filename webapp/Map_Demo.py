#KHD: 25.11.2022

from tiniworld_core.logic.data import Tiniworld
from tiniworld_core.logic.location import TWLocation

import pandas as pd  #1
import streamlit as st
import numpy as np
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import folium
from streamlit_folium import st_folium #, folium_static

st.set_page_config(page_title="Home", page_icon="📈", layout="wide")

siteHeader = st.container()
theMapDemo = st.container()



# instanciating Tiniworld class
tini = Tiniworld()
twloc = TWLocation()


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

    if "center_clicked" in st.session_state:
        selected_center = st.session_state["center_clicked"]
        st.write(selected_center)



with siteHeader:
  st.title('Data Science project with Timeseries Data')
  #st.text('In this project We look into Forecast and Prediction with Time-series data. We worked with the dataset from a Kids Entertainment and Attractions center')
  #st.text(st.session_state["prev_word_count"])

  st.markdown('''
In this project we look into Forecast and Prediction with Time-series data.
We worked with the dataset from a Kids Entertainment and Attractions center

''')

with theMapDemo:
   st.header('Showing some Map')
   # US location=[38, -96.5]
   map = folium.Map(location=[10.801603, 106.617807], zoom_start=6, scrollWheelZoom=False, tiles='CartoDB positron')
   #st_map = st_folium(map, width=700, height=450)
   #TW-PS002,ATP,Ho Chi Minh,Viet Nam,10.801603,106.617807

   tooltip = "Click me!"

   #folium.Marker(
   #    [10.801603, 106.617807], id="abc", popup="<i>TW-PS002</i>", tooltip="ATP",icon=folium.Icon(color="green"),
   #).add_to(map)
   #folium.Marker(
   #    [21.0260334, 105.9001923], popup="<b>TW-PS003</b>", tooltip=tooltip
   #).add_to(map)

   for k, v in twloc.location_dictionary.items():
       #twloc.location_dictionary
       center_name = k
       lat, lon, short_name = v['latitude'], v['longitude'], v['shortName']
       folium.Marker(
           [lat, lon], popup=f'<i>{center_name}</i>', tooltip=short_name
       ).add_to(map)

   st_map = st_folium(map, width=800, height=600)

   #map.add_child(folium.LatLngPopup())
   #test = folium_static(map)

   location_name = ''
   #if st_map['last_active_drawing']:
   #    #state_name = st_map['last_active_drawing']['properties']['name']
   #    state_name = st_map['last_active_drawing']
   #    print("print somethinog...", state_name)

   if st_map['last_object_clicked']:
       #state_name = st_map['last_active_drawing']['properties']['name']
       location_info = st_map['last_object_clicked']
       #{'lat': 10.801603, 'lng': 106.617807}
       cordinate = (location_info['lat'], location_info['lng'])
       center_clicked = twloc.get_location_by_lat_lon(location_info['lat'], location_info['lng'])
       #if "center_clicked" not in st.session_state:
       st.session_state["center_clicked"] = center_clicked
       print("print somethinog...", center_clicked)




   #print(st_map)
