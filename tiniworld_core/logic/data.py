import os
import pandas as pd
from tiniworld_core.data_sources.local_disk import get_data
from tiniworld_core.logic.params import LOCAL_REGISTRY_PATH

from prophet import Prophet
from prophet.diagnostics import cross_validation
from prophet.serialize import model_to_json, model_from_json
from prophet.plot import plot_cross_validation_metric, performance_metrics

import itertools
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import json


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

    def sum_days(self,df):
        df.groupby

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

    def plot_info(self,location,forecast):

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

    def plot_forecast(self,df: pd.DataFrame, future: pd.DataFrame):
        # df : requiers a df with the recorded data
        # future : requiers a input from prophet.make_future()

        fc_time = (future.ds.max()-df.ds.max()).days
        name = list(df[:1]['store_name'])[0]

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
        fig.update_layout(
            title_text="Tickets sold in the last 2 years and forecast for 2 month"
        )

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

        fig.show()




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


    def cv_model(self,df,location) -> pd.DataFrame:
        '''
        Does a Crossvalidation for a given prepared df(ds,y).
        Finds the best params from a param_grid (defined below) for the df, optimized for MAE.
        Fits and trains a model with this params and saves it to a given folder (LOCAL_REGISTRY_PATH)
        Needs the location code for naming the file.
        Returns a pd.DataFrame with the used parameters.
        '''

        param_grid = {
        'changepoint_prior_scale': [0.05,0.075,0.1],
        'seasonality_prior_scale': [0.0025,0.005,0.0075],
                }

        # Generate all combinations of parameters
        all_params = [dict(zip(param_grid.keys(), v)) for v in itertools.product(*param_grid.values())]

        maes = []  # Store the MAE for each params here
        locations = [] # Store the names of the location here


        # Use cross validation to evaluate all parameters
        for params in all_params:
            model_1 = Prophet(**params)
            model_1.add_country_holidays(country_name='VN') # Add holidays in Vietnam
            model_1.fit(df)  # Fit model with given params

            df_cv_1 = cross_validation(model_1,  horizon='60 days', parallel="processes")
            df_p_1 = performance_metrics(df_cv_1, rolling_window=1)

            maes.append(df_p_1['mae'].values[0])
            locations.append(location)

        # Find the best parameters
        tuning_results = pd.DataFrame(all_params)
        tuning_results['location'] = locations
        tuning_results['mae'] = maes

        # creating output and setup best params
        y = tuning_results.sort_values('mae').head(1)
        x = {'changepoint_prior_scale':list(y['changepoint_prior_scale'])[0],'seasonality_prior_scale':list(y['seasonality_prior_scale'])[0]}

        # retrain with best params
        model_2 = Prophet(**x)
        model_2.add_country_holidays(country_name='VN')
        model_2.fit(df)

        #ouput path for saving models
        save_path = os.path.join(os.path.expanduser(LOCAL_REGISTRY_PATH),"")

        with open(f'{save_path}/{location}_prophet_model.json', 'w') as fout:
            json.dump(model_to_json(model_2), fout)  # Save model
            print(f'saving {location}')

        # return the parameters and MAE for this model
        return y

    def cv_and_save_all_models(self):
        '''
        Does a crossvalidation for each location,
        trains a model each with the best parameters and saves it.
        Returns a report.
        '''
        report = pd.DataFrame(columns=['changepoint_prior_scale','seasonality_prior_scale','location','mae'])
        df_all = self.get_stores_ds_alltime()
        store_names = self.get_store_names()

        #select store
        n = len(store_names)

        # If testing set n to 2
        # n = 2

        for store_nu in range(n):
            location = store_names[store_nu]
            df_one = df_all[store_names[store_nu]]
            df = df_one[['ds','y']]
            df = df.groupby('ds').sum().reset_index()
            y = self.cv_model(df,location)
            report = pd.concat([report,y])
        report.to_csv(f'{LOCAL_REGISTRY_PATH}/report.csv')
        print(f'Done ... saved {n} models and one report to {LOCAL_REGISTRY_PATH}')
        return report
