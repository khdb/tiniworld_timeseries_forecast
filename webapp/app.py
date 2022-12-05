#KHD: 25.11.2022

from tiniworld_core.logic.data import Tiniworld
import pandas as pd  #1
import streamlit as st
import numpy as np
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import plotly.express as px

siteHeader = st.container()
projectGoal = st.container()
tiniworldLocations = st.container()
dataExploration = st.container()
modelTraining = st.container()
allCenters = st.container()

# instanciating Tiniworld class
tini = Tiniworld()

#KHD experimental
# Using "with" notation
with st.sidebar:
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )

with siteHeader:
  st.title('The Awesome Time-Series Data Science project!')
  st.text('In this project We look into Forecast and Prediction with Time-series data. We worked with the dataset from a Kids Entertainment and Attractions center')

with projectGoal:
  st.header('Project Goal')
  st.text("What do we want to have as the outcomes?")
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
  known = known.groupby(['docDate']).sum(['qty'])['qty']
  unknown = unknown.groupby(['docDate']).sum(['qty'])['qty']
  to_predict = to_predict.groupby(['docDate']).sum(['qty'])['qty']

  #Plotting
  #known.drop(columns='y', inplace=True)
  #unknown.drop(columns='y', inplace=True)
  #to_predict.drop(columns='y', inplace=True)

  fig_x, ax_ = plt.subplots()
  known.plot(ax=ax_, c='c', marker='o', zorder=3)
  unknown.plot(ax=ax_, c='grey', alpha=0.5)
  to_predict.plot(ax=ax_, c='red', marker='o', markersize=12,
                  linestyle='-')

  ax_.legend(['known', 'future', 'value to predict'])
  ax_.set_ylabel('# Ticket sales')
  ax_.set_xlabel('Date')
  st.pyplot(fig_x)

  #st.write(known)
  #st.write(to_predict)
  #st.write(unknown)
  #st.write(the_store_df)


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

with dataExploration:
  st.header('Dataset: Tiniworld dataset for one location')
  st.text('I found this dataset at...I decided to work with it because ...')

  all_stores_dict = tini.get_stores_ds_alltime()
  store_names_2 = all_stores_dict.keys()
  st.text(store_names_2)
  #st.text('Here is a list of all Stores: ')
  selected_location = st.selectbox("Tiniworld Locations", store_names_2)
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


#with newFeatures:
#  st.header('New features I came up with')
#  st.text('Let\'s take a look into the features I generated.')

with modelTraining:
  st.header('Making prediction for Location')
  st.text('In this section you can select the location name and number of days to forecast in the future!')

  store_names = tini.get_store_names()
  #st.text('Here is a list of all Stores: ')
  #st.text(store_names)

  store_name_select = st.selectbox("Store Name", store_names)

  period_to_forecast = st.slider('What should be the number of days in the future to predict?',
      min_value=10, max_value=100,
      value=20,
      step=10)

#  number_of_trees = st.selectbox('How many trees should there be?',
#      options=[100,200,300,'No limit'],
#      index=0)

  if st.button("Take this"):
      st.write(f'{store_name_select} - {period_to_forecast}' )
      # Load prediction model for this store
      model = tini.load_model(store_name_select)
      forecast = tini.predict_model(model, period_to_forecast) #make prediction for 90 days
      st.write(forecast)
      #fig2 = model.plot_components(forecast)
      #st.plotly_chart(figure_or_data, use_container_width=False, sharing="streamlit", theme=None, **kwargs)
      #st.plotly_chart(fig2)



  st.write("some new plot from David!")
  #tini.plot_forecast('TW-PS073',365) #redo this to prevent open in new browser tab


with allCenters:
  st.header('Entrance ticket sales')
  st.text('Showing ticket sales of all centers!')

  store_names = tini.get_store_names()
  #st.text('Here is a list of all Stores: ')
  #st.text(store_names)

  all_locations_dict = tini.get_stores_ds_alltime()
  stores_selected = st.multiselect("Store Name", store_names)

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


      st.text("Showing line plot")
      #df_con_3 = df_con
      df_con_3 = df_con.copy()
      df_con_3.set_index('ds', inplace=True)
      df_con_3 = df_con_3.resample('M').sum() #last()  #.sum() works
      fig_3 = px.line(df_con_3)
      st.write(fig_3)
      st.write(df_con_3)
