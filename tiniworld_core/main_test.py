# Use to test functions
from tiniworld_core.logic.data import Tiniworld

tini = Tiniworld()
#tini.ping()
store_dataset = tini.get_stores_ds()
#save the fitted model on disk
#tini.save_all_models() #works
model = tini.load_model('TW-PS002')
print("loaded model: ", type(model))

#df_dict = tini.get_data_test()
#tini.get_data()
print("Number of of locations: ", len(store_dataset))
print("Locations available: ", store_dataset.keys() )
