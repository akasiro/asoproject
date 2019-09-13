
import os,sqlite3,re,hashlib,time,joblib,sys
import pandas as pd
import numpy as np

sys.path.append(r'/home/pi/Documents/pyproject/asocalsim20190719')
from gen_simtable import aso_calsim


# 路径
datapath = os.path.join(r'/home/pi/Documents/data/asoproject/20190723')

# tool
def load_joblib(name):
        with open(name + '.pkl', 'rb') as f:
            return joblib.load(f)

# 读取数据
dict_intro = load_joblib(os.path.join(datapath,'dict_intro'))
dict_ver = load_joblib(os.path.join(datapath,'dict_ver'))
conn = sqlite3.connect(os.path.join(datapath,'aso20190723.db'))
data1 = pd.read_sql('select appleid, rdtimestamp from baseinfo',conn)
data2 = pd.read_sql('select appleid, timestamp,filename from version',conn)
data = data1.merge(data2, on = 'appleid')
df_type_id = pd.read_sql('select type_code,appleid from id_category20190913',conn)
# 计算
a = aso_calsim(data,df_type_id,dict_intro,dict_ver)
result = a.gentfidftable()
# 保存结果
result.to_csv(os.path.join(r'/home/pi/Documents/data/asoproject/20190913','aso_diff20190913.csv'),index = False)
print('Done')