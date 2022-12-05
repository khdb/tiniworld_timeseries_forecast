from tiniworld_core.logic.data import Tiniworld
import pandas as pd  #1
import streamlit as st
import numpy as np
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import plotly.express as px

# instanciating Tiniworld class
tini = Tiniworld()

st.set_page_config(page_title="Data Exploration", page_icon="📈", layout="wide")

dataExploration = st.container()

# Todo:
# Showing image of the location (tw) once the user selected the location
#with st.sidebar:
#    add_radio = st.radio(
#        "Choose a shipping method",
#        ("Standard (5-15 days)", "Express (2-5 days)")
#    )

with dataExploration:
    st.header('Tiniworld Information')
    #st.text('I found this dataset at...I decided to work with it because ...')

    all_stores_dict = tini.get_stores_ds_alltime()
    store_names_2 = all_stores_dict.keys()
    #st.text(store_names_2)
    #st.text('Here is a list of all Stores: ')
    selected_location = st.selectbox("Select a locations", store_names_2)
    btn_2 = st.button("Go!", "key123")
    if btn_2:
        the_store_df = all_stores_dict[selected_location]
        #add a date column formated date for plotting (without hour, minutes, sec)
        the_store_df['date'] = pd.to_datetime(the_store_df['ds']).dt.strftime('%y-%m-%d')
        #st.text(the_store_df)
        st.write(the_store_df)
        #plt.title(selected_location)
        #sns.scatterplot(the_store_df, y = 'qty',x='ds')
        #plt.show()
        fig, ax = plt.subplots()
        ax.hist(the_store_df['qty'], bins=20)
        st.pyplot(fig)

        st.text("Display a line chart")
        data_new = the_store_df[:50]
        st.line_chart(data=data_new, x='date', y='qty', width=0, height=0, use_container_width=True)

        st.text("Showing scatterplot")
        fig = px.scatter(the_store_df, y = 'qty',x='ds')

        #Animation example
        #fig = px.scatter(the_store_df, y = 'qty',x='store_code',
        #                 animation_frame="date")

        fig.update_layout(width=800)
        st.write(fig)
