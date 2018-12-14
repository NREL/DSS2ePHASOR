import re
import pandas as pd
import os
import sys
import numpy as np

def read_dss_masterfile(fname):
    z = {}
    key_list = []
    first_flag = 0
    with open(fname) as f:
        lines = f.readlines()
    json_list =[]
    for y in lines:
        '''
            skip comments
        '''
        if y == '' or y== '\n':
            x = None
            continue
        y = y.strip()    
        x = y    
        if x==None or x[0] == '!':
            continue
        if x[0] == '~' or x[0] == '\t':
            x = x[2:]
        else:
            key_list = [] 
        x = re.split('=| ',x)  
        te = []
        for p in x:
            if p == '':
                continue
            te.append(p)   

        x = te        
        for i in range(0,len(x)-1,2):
            y = x[i]
            y2 = x[i+1]
            if y[0]=='!':
                break
            else:
                if y == 'new' or y == 'New' or y =='NEW':
                    '''
                        create new objects
                    '''
                    new_key = y2.split(".")[0]
                    if new_key in key_list:
                        tmp_key_cnt = len([x for x in key_list if new_key == x.split('+')[0]])
                        new_key = str(new_key)+str('+{}'.format(tmp_key_cnt))
                    key_list.append(new_key)
                    z[new_key] = str(y2.split(".")[1])                        
                else:
                    new_key = str(y)
                    if new_key in key_list:
                        tmp_key_cnt = len([x for x in key_list if new_key == x.split('+')[0]])
                        new_key = str(new_key)+str('+{}'.format(tmp_key_cnt))                       
                    key_list.append(new_key)
                    z[new_key]= str(y2)
    if z!= {}:
#         print('z:',z)
        return (z)

def dss_to_df(fname):
    '''
    read an OpenDSS file and convert it to a pandas DataFrame
    '''
    z = {}
    key_list = []
    first_flag = 0
    with open(fname) as f:
        lines = f.readlines()
    json_list =[]
    for x in lines:
        '''
            skip comments
        '''
        if x==None or x=='' or x[0] == '!':
            z = {}
            continue
        if x[0] == '~' or x[0] == '\t':
            x = x[2:]
        else:
            z = {}
            key_list = [] 
#         x = x.strip()    
        x = re.split('=| |\t',x)  
        if x != []:
            for i in range(0,len(x)-2,2):
                if x[i] == '':
                    continue
                y = x[i]
        #         
                y2 = x[i+1]
                try:
                    y[0]
                except:
                    print("HERE",y,x,i)
    #             print(y)
                if y[0]=='!':
                    break
                else:
                    if y == 'new' or y == 'New' or y =='NEW':
                        '''
                            create new objects
                        '''
                        new_key = y2.split(".")[0]
                        if new_key in key_list:
                            tmp_key_cnt = len([x for x in key_list if new_key == x.split('+')[0]])
                            new_key = str(new_key)+str('+{}'.format(tmp_key_cnt))
                        key_list.append(new_key)
                        z[new_key] = str(y2.split(".")[1])                        
                    else:
                        new_key = str(y)
                        if new_key in key_list:
                            tmp_key_cnt = len([x for x in key_list if new_key == x.split('+')[0]])
                            new_key = str(new_key)+str('+{}'.format(tmp_key_cnt))                       
                        key_list.append(new_key)
                        z[new_key]= str(y2)
        if z!= {}:
            json_list.append(z)     
#             print(z)
    df = pd.DataFrame(json_list)   
    return (df)

phases_123_abc = [
    {'\.1' : '_a'},\
    {'\.2' : '_b'},\
    {'\.3' : '_c'},\
]

def get_3mod_cols(keyname,keyprefix,rowdata):
#     replace column names 
    fbus_split  = rowdata[keyname].split('.')    
    fbus_name = fbus_split[0]
    idx = 1
    for y in fbus_split[1:]:
        bus_id = '{}{}'.format(keyprefix,idx)
        rowdata[bus_id] = fbus_name+str('.{}'.format(y))
        idx = idx+1
    return rowdata   

def split_phases_to_cols(keylist,dataframe):
#      split .1.2.3 to bus1:.1 bus2:.2 bus3:.3
    temp = pd.DataFrame()
    
    for i,x in dataframe.iterrows():
        tmp = x
#         print(x)
        for y in keylist:
            for existing,newkey in y.items():
                tmp = get_3mod_cols(existing,newkey,tmp)
        temp = temp.append(tmp,ignore_index=True)
    return temp

def phase_replace(kv_pair,dataframe,replacement_keys):
#   replace .1:_a .2:_b .3:_c
    for keys in replacement_keys:
        for x in kv_pair:
            for existing, replacement in x.items():
                dataframe[keys].replace('{}'.format(existing),'{}'.format(replacement),regex=True,inplace=True)   

def col_replace(df,df_col_map):
    df_new_cols = []
    for x in df.columns:
        try:
            df_new_cols.append(df_col_map[x])
        except:
            df.drop([x],inplace=True, axis=1)
#             print("Key not found in map : {}".format(x))
    df.columns = df_new_cols
     
def dss_to_df_diff(fname):
    '''
    read an OpenDSS file and convert it to a pandas DataFrame
    '''
# fname = '/Users/dvaidhyn/Desktop/ACES-COSIM/fy19cosim/aces-simulations/nodes/nodes-sce/temp/DSS2ePHASOR/j1_feederfiles/filestoopal/Transformers.dss'
    z = {}
    key_list = []
    first_flag = 0
    with open(fname) as f:
        lines = f.readlines()
    json_list =[]

    for x in lines:
        '''
            skip comments
        '''
        if x==None or x=='' or x[0] == '!':
            z = {}
            newtype = ''
            continue
        if x[0] == '~' or x[0] == '\t':
            x = x[2:]
        else:
            z = {}
            key_list = [] 
#         x = x.strip()    
        x = re.split('=| |\t',x)  
        if x != []:
            for i in range(0,len(x)-1,2):
                if x[i] == '':
                    continue
                y = x[i]
        #         
                y2 = x[i+1]
                try:
                    y[0]
                except:
                    print("HERE",y,x,i)
    #             print(y)
                if y[0]=='!':
                    break
                else:
                    if y == 'new' or y == 'New' or y =='NEW':
                        '''
                            create new objects
                        '''
                        
                        new_key = y2.split(".")[0]
#                         if new_key in act_keys:
#                             new_key_df = new_key
                        if new_key in key_list:
                            tmp_key_cnt = len([x for x in key_list if new_key == x.split('+')[0]])
                            new_key = str(new_key)+str('+{}'.format(tmp_key_cnt))
                        key_list.append(new_key)
                        z[new_key] = str(y2.split(".")[1]).strip()
                            
                    else:
                        new_key = str(y)
                        if new_key in key_list:
                            tmp_key_cnt = len([x for x in key_list if new_key == x.split('+')[0]])
                            new_key = str(new_key)+str('+{}'.format(tmp_key_cnt))                       
                        key_list.append(new_key)
                        z[new_key]= str(y2).strip()
        if z!= {}:
            json_list.append(z)     
#             print(z)
    return (json_list)        