#KHD: 25.11.2022

import pandas as pd  #1
import streamlit as st
siteHeader = st.container()
dataExploration = st.container()
newFeatures = st.container()
modelTraining = st.container()

taxi_data = pd.read_csv('data/taxi_data.csv')  #2
distribution_pickup = pd.DataFrame(taxi_data['PULocationID'].value_counts())   #3
st.bar_chart(distribution_pickup)    #4

with siteHeader:
  st.title('Welcome to the Awesome project!')
  st.text('In this project I look into ...And I try ... I worked with the dataset from ...')

max_depth = st.slider('What should be the max_depth of the model?',
    min_value=10, max_value=100,
    value=20,
    step=10)

number_of_trees = st.selectbox('How many trees should there be?',
    options=[100,200,300,'No limit'],
    index=0)

st.text('Here is a list of features: ')
st.write(taxi_data.columns)
input_feature = st.text_input('Which feature would you like to input to the model?',
  'PULocationID')

with dataExploration:
  st.header('Dataset: Iris flower dataset')
  st.text('I found this dataset at...I decided to work with it because ...')



with newFeatures:
  st.header('New features I came up with')
  st.text('Let\'s take a look into the features I generated.')

with modelTraining:
  st.header('Model training')
  st.text('In this section you can select the hyperparameters!')
