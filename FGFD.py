#!/usr/bin/env python
# coding: utf-8

# In[2]:


import streamlit as st
import pandas as pd
import datetime as dt
import numpy as np
import sys
import pandas as pd
import websocket, json


# In[3]:


from sqlalchemy import create_engine
from threading import *


# In[4]:


engine = create_engine('sqlite:///CryptoDB.db')


# In[5]:


stream = "wss://stream.binance.com:9443/ws/!miniTicker@arr"


# In[6]:


def on_message(ws, message):
    msg = json.loads(message)
    symbol = [x for x in msg if x['s'].endswith('USDT')]
    frame = pd.DataFrame(symbol)[['E','s','c']]
    frame.E = pd.to_datetime(frame.E, unit='ms')
    frame.c = frame.c.astype(float)
    for row in range(len(frame)):
        data = frame[row:row+1]
        data[['E','c']].to_sql(data['s'].values[0], engine, index=False, if_exists='append')

ws = websocket.WebSocketApp(stream, on_message=on_message)
def run(): 
    ws.run_forever()


# In[7]:


t1 = Thread(target = run, args=())
t1.start()


# In[11]:


from sqlalchemy import create_engine
engine = create_engine('sqlite:///CryptoDB.db')


# In[12]:


symbols = pd.read_sql('SELECT name FROM sqlite_master WHERE type="table"',
                     engine).name.to_list()


# In[13]:


st.title('Пересечения SMA')


# In[14]:


def applytechnicals(df):
    df['SMA_1'] = df.c.rolling(1).mean()
    df['SMA_10'] = df.c.rolling(10).mean()
    df.dropna(inplace=True)


# In[15]:


def qry(symbol):
    now = dt.datetime.utcnow()
    before = now - dt.timedelta(minutes=30)
    qry_str = f"""SELECT E,c FROM '{symbol}' WHERE E >= '{before}'"""
    df = pd.read_sql(qry_str,engine)
    df.E = pd.to_datetime(df.E)
    df = df.set_index('E')
    df = df.resample('1min').last()
    applytechnicals(df)
    df['position'] = np.where(df['SMA_1'] > df['SMA_10'], 1 , 0)
    return df


# In[16]:


def check():
    for symbol in symbols:
        if len(qry(symbol).position) > 1:
            if qry(symbol).position[-1] and qry(symbol).position.diff()[-1]:
                st.write(symbol)


# In[ ]:


st.button('Получить пересечения', on_click=check())


# In[ ]:




