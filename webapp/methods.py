from tiniworld_core.logic.data import Tiniworld
import pandas as pd
import streamlit as st
import datetime as dt

tini = Tiniworld()

if 'store' not in st.session_state:
    st.session_state['store'] = 'TW-PS008'
if 'forecast' not in st.session_state:
    st.session_state['forecast'] = 60
if 'store' not in st.session_state:
    st.session_state['store'] = 'TW-PS008'
if 'forecast' not in st.session_state:
            st.session_state['forecast'] = 60
if 'ratio' not in st.session_state:
            st.session_state['ratio'] = 0
if 'df_ratio' not in st.session_state:
            st.session_state['df_ratio'] = 0
if 'color' not in st.session_state:
            st.session_state['color'] = 'green'
if 'compare' not in st.session_state:
            st.session_state['compare'] = False
if 'store_c' not in st.session_state:
            st.session_state['store_c'] = 'TW-PS002'

class AppFunktion:

    def load_session_state(self):
        if 'store' not in st.session_state:
            st.session_state['store'] = 'TW-PS008'
        if 'forecast' not in st.session_state:
            st.session_state['forecast'] = 60
        if 'store' not in st.session_state:
            st.session_state['store'] = 'TW-PS008'
        if 'forecast' not in st.session_state:
                    st.session_state['forecast'] = 60
        if 'ratio' not in st.session_state:
                    st.session_state['ratio'] = 0
        if 'df_ratio' not in st.session_state:
                    st.session_state['df_ratio'] = 0
        if 'color' not in st.session_state:
                    st.session_state['color'] = 'green'
        if 'compare' not in st.session_state:
                    st.session_state['compare'] = False
        if 'store_c' not in st.session_state:
                    st.session_state['store_c'] = 'TW-PS002'



    def load_data(self,n = st.session_state['store'], t = st.session_state['forecast']):   # n = storecode, t= time of days to forecast
        self.load_session_state()
        pred = tini.predict_model(n,t)
        now = str(dt.date.today())
        last_day = pred['ds'].max()
        first_day = pred['ds'].min()
        period = last_day-first_day

        pred['date_str'] = pred['ds'].map(lambda x : str(x)[:10])
        index_today = (pred[pred['date_str'] == now].index)[0]
        sale_today = round(list(pred[pred.index == index_today].trend)[0],2)
        sale_tomorrow = round(list(pred[pred.index == index_today+1].trend)[0],2)
        trend_today = round(sale_tomorrow-sale_today,2)

        df_store = tini.get_stores_ds_alltime()[n]
        number_od_days = df_store.groupby('ds').sum().shape[0]


        return trend_today, sale_today, pred, number_od_days, df_store, period


    def sidebar(self):
        self.load_session_state()
        store_names = tini.get_store_names()


        sn_df = pd.DataFrame(store_names)
        index_store = int(sn_df[sn_df[0]== st.session_state.store].index[0])


        store_name = st.selectbox("Choose a store code to look at!", store_names, index=index_store,key='n')
        st.session_state['store'] = store_name
        ratio = tini.get_ratio()
        ratio = ratio[ratio.index==st.session_state['store']]
        st.session_state['df_ratio'] = ratio
        st.session_state['ratio'] = round(float(ratio['Kids %']),3)
        st.session_state['sale_overall'] = int(ratio['qty'])
        st.session_state['rank'] = int(ratio['rank'])


        trend_today, sale_today, pred, number_of_days, df_store, period = self.load_data(store_name)

        st.session_state['pred'] = pred
        st.session_state['trend_today'] = trend_today
        st.session_state['sale_today'] = sale_today
        st.session_state['number_of_days'] = number_of_days
        st.session_state['df_store'] = df_store
        st.session_state['store_name'] = list(df_store[:1]['store_name'])[0]
        st.session_state['period'] = int(str(period).split()[0])


    def sidebare_2(self):
        #st.write('_____')
        store_names = tini.get_store_names()
        sn_df = pd.DataFrame(store_names)
        index_store_c = int(sn_df[sn_df[0]== st.session_state.store_c].index[0])
        st.session_state['compare'] = st.checkbox('compare')
        if st.session_state.compare:
            st.session_state['store_c'] = st.selectbox("Choose a store to compare to!", store_names, index=index_store_c, key='c')
