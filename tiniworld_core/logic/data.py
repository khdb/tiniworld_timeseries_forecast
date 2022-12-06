import os
import pandas as pd
from tiniworld_core.data_sources.local_disk import get_data
from tiniworld_core.logic.params import LOCAL_REGISTRY_PATH

from prophet import Prophet
from prophet.diagnostics import cross_validation
from prophet.serialize import model_to_json, model_from_json
from prophet.plot import plot_cross_validation_metric, performance_metrics, plot_yearly
from plotly.subplots import make_subplots

import itertools
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import json
import streamlit as st


#KHD: 28.11.2022

class Tiniworld:

    def ping(self):
        """
        You call ping I print pong.
        """
        print("pong")
#
# *** getting data ***
#
    #load data from folder
    def get_raw_data(self) -> pd.DataFrame:
        '''
        including item translation to english
        split adults and kids
        '''
        df = get_data("ticket-sales") #filename without the file extenstion
        return df
    # get the dictionary containing all locations as DF
    def get_stores_ds_alltime(self) -> dict:
        """
        This function returns a Python dict.
        Its keys should be 'store_code'
        Its values should be pandas.DataFrames loaded from csv files.
        with the key 'all' it returns a dataset for all the company.
        """

        df = get_data("ticket-sales") #filename without the file extenstion

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

        # update: integrated a new key for 'all' aka whole company
        all_company = self.get_all_company()
        dict_loc['all'] = all_company['all']
        return dict_loc

    def get_all_company(self) -> dict:
        '''
        returns a dict with {'all': df}
        '''
        raw = self.get_raw_data()
        raw['ds']= pd.to_datetime(raw.loc[:,'docDate'])
        # df_all_company = raw.groupby('ds').sum('qty').reset_index()#[['ds','qty']]
        df_all_company = raw
        df_all_company['y'] = df_all_company['qty']
        all = {'all':df_all_company}
        return all

    def get_store_names(self) -> list:
        '''
        returns a list with all the store_codes
        '''
        all_df = self.get_stores_ds_alltime()
        keys = list(all_df.keys())
        return keys

    def get_ratio(self,store=None):
        '''
        returns a pd.DataFrame with total sale, sale per adult, sale per kid
        percentage of adults and percentage of kids for each store.
        If given a store_code, it returns the percentage of kids for this store.
        '''
        df = self.get_raw_data().groupby('store_code').sum(numeric_only=True)
        df['Kids %'] = df['Kids']/(df['Adults']+df['Kids'])
        df['Adults %'] = 1-df['Kids %']
        # drop 'Result'
        df = df.drop('Result',axis=1)
        y = list(df.index)
        # remove all none playgrounds
        l = [(i[:2])=='TW' for i in y]
        df = df[l]
        #add sales ranking
        df = df.sort_values('qty',ascending=False)
        df['rank'] = (df.reset_index().index)+1

        if not store:
            return df
        else:
            return round(df.loc[store,'Kids %'],2)
#
#  *** modeling ***
#
    def load_model(self,store_name):
        #path containing saved models
        model_path = os.path.join(os.path.expanduser(LOCAL_REGISTRY_PATH), f"{store_name}_prophet_model.json")
        with open(model_path, 'r') as fin:
            model = model_from_json(json.load(fin))  # Load model
        return model

    def train_model(self,df):

        #initiate and train a model on a DF
        model = Prophet()
        # add holiday seasonality
        model.add_country_holidays(country_name='VN')
        model.fit(df)

        return model

    def make_future(self,location,forecast=60):
        '''
        model = trained model
        forecast = int(number of days to forecast)

        '''
        model = self.load_model(location)
        future = model.make_future_dataframe(periods=forecast)

        return future

    def predict_model(self,location,forecast=60):
        '''
        model = trained model
        forecast = int(number of days to forecast)

        '''
        model = self.load_model(location)
        future = model.make_future_dataframe(periods=forecast)
        pred = model.predict(future)

        return pred
#
# *** Crossvaldation ***
#
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

    def cv_and_save_all_models(self,all_over = False):
        '''
        Does a crossvalidation for each location,
        trains a model each with the best parameters and saves it.
        Returns a report.
        '''
        report = pd.DataFrame(columns=['changepoint_prior_scale','seasonality_prior_scale','location','mae'])

        if not all_over:
            df_all = self.get_stores_ds_alltime()
            store_names = self.get_store_names()

        else:
            df_all = self.get_all_company()
            store_names = ['all']

        n = len(store_names)

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
#
#  *** plotting stuff ***
#
    def plot_info(self,location,forecast=7,*args):
        '''
        forecast = int(number of days to forecast)
        location = str(store code)

        '''
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

        model = self.load_model(location)
        pred = self.predict_model(location,forecast)

        # fig1 = model.plot_components(pred)
        fig2 = plot_yearly(model)

        return fig, fig2

    def plot_forecast(self,location,forecast=60):
        '''
        forecast = int(number of days to forecast)
        location = str(store code)
        '''
        #get all Data
        df_all = self.get_stores_ds_alltime()

        #select one location
        df = df_all[location]


        future = self.make_future(location,forecast)
        pred = self.predict_model(location,forecast)

        fc_time = (future.ds.max()-df.ds.max()).days

        df = df.groupby('ds').sum().reset_index()

        layout = {
            # to highlight the prediction we use shapes and create a rectangular
            'shapes': [
                # highlight from enddate of datat + days of prediction
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
                    'name' : 'forecast',
                    'fillcolor': '#00ff77',
                    'opacity': 0.2,
                    'line': {
                        'width': 0,
                    }
                }

            ]
        }

        # Create figure
        fig = go.Figure()

        y_max = df['y'].max()

        # plot y
        fig.add_trace(go.Scatter(x=df['ds'],
                                y=df['y'],
                                name='Ticket sales',
                                mode='markers',
                                marker=dict(color='black')))
        # plot yhat
        fig.add_trace(go.Scatter(x=pred['ds'],
                                y=pred['yhat'],
                                name='Predictions',
                                mode='lines',
                                line=dict(color='red', width=3)
                                ))
        # plot upper CI
        fig.add_trace(go.Scatter(x=pred['ds'],
                                y=pred['yhat_upper']*0.8,
                                name='yhat_upper',
                                mode='lines',
                                line=dict(color='gray', width=1)
                                ))
        # plot lower CI
        fig.add_trace(go.Scatter(x=pred['ds'],
                                y=pred['yhat_lower']*1.2,
                                xsrc='2020-01-01',
                                name='yhat_lower',
                                mode='lines',
                                fill='tonexty',
                                line=dict(color='gray', width=1)
                                ))


        # Add range slider
        fig.update_layout(xaxis=dict(
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
                            ))

        fig.update_layout(yaxis_range=[0,y_max],
                        title=f"Tickets sold in the last 2 years and forecast for {forecast} days",
                        template= "plotly_white"
                        )
        fig.update_layout(layout)

        # use fig.show() to render the graphig/plot i.e. in Jupyter Notebook
        #fig.show()
        # return the fig object to use in Streamlit app, otherwise the graphic
        # will trigger the browser to open a new tab to render the graphic as standalone.
        return fig

    def plot_trend(self,location,forecast=0):
        '''
        forecast = int(number of days to forecast)
        location = str(store code)

        If forecast is 0 it gives back a simple plot for just the given data.
        If forecast is more than 0 it gives back a plot with more details and interactivity

        Returns a a value of the trend, and a fig of the graph
        '''
        #get all Data
        df_all = self.get_stores_ds_alltime()

        #select one location
        df = df_all[location]


        future = self.make_future(location,forecast)
        pred = self.predict_model(location,forecast)

        fc_time = (future.ds.max()-df.ds.max()).days

        df = df.groupby('ds').sum(numeric_only= True).reset_index()

        trend = round(float(pred.loc[pred.index[-1],'trend'])-float(pred.loc[pred.index[-2:-1],'trend']),2)

        fig = go.Figure()

        fig.add_trace(go.Scatter(x=pred['ds'],
                                        y=pred['trend'],
                                        name='Ticket sales',
                                        mode='lines',
                                        marker=dict(color='black')))
        fig.update_layout(
            yaxis_title="Ticket Sales per day"
            )
        if not forecast == 0:
            # plot upper trend variance
            fig.add_trace(go.Scatter(x=pred['ds'],
                                            y=pred['trend_upper'],
                                            name='Trend hight',
                                            mode='lines',
                                            line=dict(color='gray', width=1)
                                            ))
            # plot lower trend variance
            fig.add_trace(go.Scatter(x=pred['ds'],
                                            y=pred['trend_lower'],
                                            name='Trend low',
                                            mode='lines',
                                            fill='tonexty',
                                            line=dict(color='gray', width=1)
                                            ))
            # Add range slider
            fig.update_layout(xaxis=dict(
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
                            ))
        layout = {
        # to highlight the prediction we use shapes and create a rectangular
        'shapes': [
            # highlight from enddate of datat + days of prediction
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
                'name' : 'forecast',
                'fillcolor': '#00ff77',
                'opacity': 0.2,
                'line': {
                    'width': 0,
                }
            }

        ]
        }
        fig.update_layout(layout)


        fig.update_layout(title=f"Trend",
                                template= "plotly_white"
                                )
        fig.update_layout(layout)
        return fig


    def plot_sales(self,n):
        '''
        Scatter plot - total ticket sale per day
        '''
        df = self.get_stores_ds_alltime()[n]
        df = df.groupby('ds').sum().reset_index()

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['ds'],
                                y=df['y'],
                                name='Ticket sales',
                                mode='markers',
                                marker=dict(color='black')))
        fig.update_layout(
                        yaxis_title="Ticket Sales per day",
                        title=f"Tickets sold in the last 2 years",
                        template= "plotly_white"
                        )
        return fig

    def plot_monthly(self,n):
        '''
        plot seasonal trend - year
        '''
        model = self.load_model(n)
        data,_ = plot_yearly(model)
        date, value = data.get_data()

        fig = go.Figure()

        fig.add_trace(go.Scatter(x=date,
                                y=value,
                                name='Ticket sales',
                                mode='lines',
                                line_shape='spline',
                                line=dict(color='black')
                                ))
        fig.update_layout(
                        yaxis_title="Trend",
                        xaxis_title="Day of year",
                        title=f"Season Trend",
                        template= "plotly_white"
                        )
        return fig


    def plot_weekday(self,n):
        '''
        plot seasonal trend - week
        '''
        df = self.get_stores_ds_alltime()[n]
        df['day_name'] = df['ds'].dt.day_name()
        sorter = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
        sorterIndex = dict(zip(sorter,range(len(sorter))))
        df['Day_id'] = df['day_name'].map(sorterIndex)
        df = df.sort_values('Day_id')
        df.reset_index()
        df_dow = df.groupby('day_name').sum('y')[['y']]
        df_dow = df_dow.reset_index()
        df_dow['Day_id'] = df_dow['day_name'].map(sorterIndex)
        df_dow = df_dow.sort_values('Day_id')

        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(go.Box(x=df.day_name,
                                y=df['y'],
                                name='distribution sales'),
                                secondary_y= True)

        fig.add_trace(go.Scatter(x=df_dow.day_name,
                                y=df_dow['y'],
                                name='absolute sales',
                                mode='lines',
                                marker=dict(color='black')),
                                secondary_y=False)


        fig.update_layout(
                        yaxis_title="Ticket Sales",
                        title=f"Sales per weekday",
                        template= "plotly_white"
                        )

        fig.update_yaxes(title_text="absolut sales per weekday", secondary_y=False)
        fig.update_yaxes(title_text="distribution sales per weekday", secondary_y=True)

        return fig
