import os,sqlite3,re,hashlib,time
import pandas as pd
import numpy as np
# 路径
datapath = os.path.join(r'/home/pi/Documents/data/asoproject/20190723')
dbpath = os.path.join(datapath,'aso20190723.db')
conn = sqlite3.connect(dbpath)
cur  = conn.cursor()


# tool func
def create_table(tablename,var_dict,conn = conn,cur = cur):
    var_define = ','.join(['{} {}'.format(k,v) for k,v in var_dict.items()])
    create_table_cmd = 'create table if not exists {} ({})'.format(tablename,var_define)
    try:
        cur.execute(create_table_cmd)
        conn.commit()
        print('{} created'.format(tablename))
    except:
        print('wrong in create {}'.format(tablename))
def insert_data(tablename, df, datahashornot = True, conn = conn , cur = cur):
    df_columns = df.columns.tolist()
    if datahashornot:
        hash_sha256 = hashlib.sha256()
        insert_cmd = 'insert into {}(datahash,{}) values ({}?)'.format(tablename,','.join(df_columns),'?,'*(len(df_columns)))
    else:
        insert_cmd = 'insert into {}({}) values ({}?)'.format(tablename,','.join(df_columns),'?,'*(len(df_columns)-1))
    for r in df.itertuples(index = False):
        if datahashornot:
            hash_sha256.update(str(tuple(r)).encode())
            datahash = hash_sha256.hexdigest()
            tempdata = (datahash,)+tuple(r)
        else:
            tempdata = tuple(r)
        try:
            cur.execute(insert_cmd,tempdata)
            conn.commit()
        except:
            print('wrong')
    print('complete insert')
def insertlog(logtext,conn =conn, cur = cur):
    hash_sha256 = hashlib.sha256()
    hash_sha256.update(logtext.encode())
    loghash = hash_sha256.hexdigest()
    tempcmd = 'insert into changelog (loghash, date,log) values (?,?,?)'
    cur.execute(tempcmd,(loghash, time.asctime(),logtext))
    conn.commit()