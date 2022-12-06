#KHD: 25.11.2022

from tiniworld_core.logic.data import Tiniworld
import pandas as pd  #1
import streamlit as st
import numpy as np
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import plotly.express as px


from tiniworld_core.logic.params import LOCAL_DATA_PATH
from webapp.methods import AppFunktion

# instanciating Tiniworld class
tini = Tiniworld()
AF = AppFunktion()

st.set_page_config(page_title="Tiniworld Locations", page_icon="📈", layout="wide")

with st.sidebar:
    AF.sidebar()

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
    location_file = f"{LOCAL_DATA_PATH}/tw_location_info.csv" #Load OK

    df_locations = pd.read_csv(location_file)
    df_locations = df_locations[['latitude', 'longitude']]

    st.map(df_locations)


# with allLocations:
#     st.header('Historical Data (Footfall)')
#     st.text('Showing the footfall of all centers from historical data!')

#     store_names = tini.get_store_names()

#     all_locations_dict = tini.get_stores_ds_alltime()
