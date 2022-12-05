# Use to test functions
from tiniworld_core.logic.data import Tiniworld

tini = Tiniworld()
#tini.ping()
#store_dataset = tini.get_stores_ds()
store_dataset = tini.get_stores_ds_alltime() # new since 02.12.2022
#save the fitted model on disk
#tini.save_all_models() #works
#tini.cv_and_save_all_models() # 01.12.2022

# 02.12.2022
# fit a model for the entire business (all locations together,
# to see how is the performance and trend of the business)
tini.cv_and_save_all_models(all_over=True) #
model = tini.load_model('TW-PS002')
print("loaded model: ", type(model))

#df_dict = tini.get_data_test()
#tini.get_data()
print("Number of of locations: ", len(store_dataset))
print("Locations available: ", store_dataset.keys() )
