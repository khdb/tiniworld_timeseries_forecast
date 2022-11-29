import os
import pandas as pd
from tiniworld_core.data_sources.local_disk import get_data
from tiniworld_core.logic.params import LOCAL_REGISTRY_PATH

from prophet import Prophet
import plotly.express as px
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import json
from prophet.serialize import model_to_json, model_from_json

#KHD: 28.11.2022

class Tiniworld:
    # get the dictionary containing all locations as DF
    def get_stores_ds(self) -> dict:
        """
        This function returns a Python dict.
        The timeperiod is just between the covit gaps.
        Its keys should be 'store_code'
        Its values should be pandas.DataFrames loaded from csv files
        """

        df = get_data("ticket-sales") #filename without the file extenstion
        #print("df columns: ", df.columns)

        #From David
        ## start of cleaning pipeline
        #add column with date as datetime and right name for prophet (ds)
        df['ds']=pd.to_datetime(df['docDate'])

        #remove date before first covit gap
        df = df[df['ds']>='2020-05-28']

        #add column with target 'y'
        df.loc[:,'y'] = df['qty']

        #find the 30 locations with the most data - treshold is entries in dataset for one location
        treshold = 2300
        store_list = df.groupby('store_code').count()[(df.groupby('store_code').count()>treshold)['y']]

        #extract location keys
        store_code = store_list.index

        #create  Dictionary of DataFrames for every location
        dict_loc = {}
        for n in (store_code):
            dict_loc[n]=df[df['store_code']==n]

        #get data until second covit break for a forecast to impute the break
        dict_loc_fp = {}
        for n in (store_code):
            dict_loc_fp[n]=dict_loc[n][[dict_loc[n]['ds']<'2021-07-20'][0]]


        #End from David

        return dict_loc_fp

    def get_stores_ds_alltime(self) -> dict:
        """
        This function returns a Python dict.
        Its keys should be 'store_code'
        Its values should be pandas.DataFrames loaded from csv files
        """

        df = get_data("ticket-sales") #filename without the file extenstion
        #print("df columns: ", df.columns)

        #From David
        ## start of cleaning pipeline
        #add column with date as datetime and right name for prophet (ds)
        df['ds']=pd.to_datetime(df['docDate'])

        #add column with target 'y'
        df.loc[:,'y'] = df['qty']

        #find the 30 locations with the most data - treshold is entries in dataset for one location
        treshold = 2300
        store_list = df.groupby('store_code').count()[(df.groupby('store_code').count()>treshold)['y']]

        #extract location keys
        store_code = store_list.index

        #create  Dictionary of DataFrames for every location
        dict_loc = {}
        for n in (store_code):
            dict_loc[n]=df[df['store_code']==n]


        #End from David

        return dict_loc

    def get_store_names(self):
        all_df = self.get_stores_ds_alltime()
        keys = list(all_df.keys())
        return keys

    def get_raw_data(self) -> pd.DataFrame:
        df = get_data("ticket-sales") #filename without the file extenstion
        return df

    def train_model(self,df):

        #initiate and train a model on a DF
        model = Prophet()
        # add holiday seasonality
        model.add_country_holidays(country_name='VN')
        model.fit(df)

        return (model)

    def predict_model(self,model,forecast):
        #
        future = model.make_future_dataframe(periods=forecast)
        pred = model.predict(future)

        return pred

    def plot_info(self,location):

        forecast=90

        #get all Data

        df_all = self.get_stores_ds_alltime()

        #select one location
        df = df_all[location]

        #prepare Data
        df = df.groupby('ds').sum(numeric_only=False)[['y']].reset_index()

        # Plot that shows the historical data by day of the week
        dayofweek_colors = {0:'k',1:'r',2:'g',3:'b',4:'c',5:'m',6:'y'}
        days = ['Mo','Tu','We','Th','Fr','Sa','So']
        plt.close()
        fig, ax = plt.subplots(figsize=(12,6))
        ax.scatter(df['ds'], df['y'], c=df['ds'].dt.dayofweek.map(dayofweek_colors))
        handles = [mpatches.Patch(color=v, label=k) for v, k in zip(dayofweek_colors.values(), days)]
        legend = ax.legend(handles=handles,title="Day of the week")
        ax.add_artist(legend)
        plt.show()

        model = self.train_model(df)
        pred = self.predict_model(model,forecast)

        fig1 = model.plot_components(pred)

        return pred

    def save_all_models(self):
        all_df = self.get_stores_ds_alltime()
        keys = list(all_df.keys())

        #ouput path for saving models
        save_path = os.path.join(os.path.expanduser(LOCAL_REGISTRY_PATH),"")
        #f'../model/{store_name}_prophet_model.json'

        for k in keys:

            model = self.train_model(all_df[k])

            with open(f'{save_path}/{k}_prophet_model.json', 'w') as fout:
                json.dump(model_to_json(model), fout)  # Save model
            print(f'saving {k}')
        return keys

    def load_model(self,store_name):
        #path containing saved models
        model_path = os.path.join(os.path.expanduser(LOCAL_REGISTRY_PATH), f"{store_name}_prophet_model.json")
        with open(model_path, 'r') as fin:
            model = model_from_json(json.load(fin))  # Load model
        return model

    def ping(self):
        """
        You call ping I print pong.
        """
        print("pong")
