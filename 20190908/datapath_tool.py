import sys,os,sqlite3,re,hashlib,time
import pandas as pd
import numpy as np
# setting
pd.options.display.max_columns = None
# 路径
datapath = os.path.join(r'/home/pi/Documents/data/asoproject')
dbpath = os.path.join(datapath,'20190723','aso20190723.db')
conn = sqlite3.connect(dbpath)
cur  = conn.cursor()