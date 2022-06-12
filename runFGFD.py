#!/usr/bin/env python
# coding: utf-8

# In[10]:


from streamlit import cli as stcli
import streamlit as st
import pandas as pd
import datetime as dt
import numpy as np
import sys
import pandas as pd
import websocket, json
from sqlalchemy import create_engine
from threading import *


# In[11]:


if __name__ == '__main__':
    sys.argv = ["streamlit", "run", "FGFD.py"]
    sys.exit(stcli.main())


# In[ ]:




