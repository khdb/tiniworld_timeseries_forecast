# Class for tiniworld locations
import numpy as np
import pandas as pd
from tiniworld_core.data_sources.local_disk import get_location_data

# Private method: https://www.geeksforgeeks.org/private-methods-in-python/
#KHD: 07.12.2022
class TWLocation:

    '''
    DataFrames containing all orders as index,
    and various properties of these orders as columns
    '''
    def __init__(self):
        # Assign an attribute ".data" to all new instances of Order
        #self.data = self.__get_data()
        self.location_dictionary = self.__get_data() # Key of the dictionary is the store_code
        self.lat_lon_dict = self.__build_loc_dict() #Key of the dictionary is the tulpe consist of Lat Lon


    def ping(self):
        """
        You call ping I print pong.
        """
        print("pong")


    # This is a private method
    def __get_data(self):
        df = self.__get_raw_data()
        # Turn the df into a dictionary with the store_code as key and other columns/values as pd series
        location_dictionary = df.set_index('store_code').T.to_dict('series')
        return location_dictionary


    # #This is a private method, load data from folder
    def __get_raw_data(self) -> pd.DataFrame:
        '''
        including item translation to english
        split adults and kids
        '''
        df = get_location_data("tw_location_info") #filename without the file extenstion
        return df

    # This is a private method
    def __build_loc_dict(self):
        lat_lon_dict = {}
        for k, v in self.location_dictionary.items():
            tp = (v['latitude'], v['longitude'])
            lat_lon_dict[tp] = v

        return lat_lon_dict


    # get_location_by_store_code(store_code)
    def get_location_by_store_code(self, store_code):
        #my_list = self.get_data()
        #a = my_list['TW-PS001']
        #a = my_list[store_code]
        a_location = self.location_dictionary[store_code]
        return a_location
        #get_location_by_store_code('TW-PS002')

    #get_location_by_lat_lon(10.801603, 106.617807)
    def get_location_by_lat_lon(self, lat, lon):
        tp = (lat, lon)
        return self.lat_lon_dict[tp]
