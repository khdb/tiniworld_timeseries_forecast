import os
import pandas as pd
from tiniworld_core.data_sources.local_disk import get_data

#KHD: 28.11.2022

class Tiniworld:
    # get the dictionary containing all locations as DF
    def get_stores_ds(self) -> dict:
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

    def get_raw_data(self) -> pd.DataFrame:
        df = get_data("ticket-sales") #filename without the file extenstion
        return df


    def ping(self):
        """
        You call ping I print pong.
        """
        print("pong")
