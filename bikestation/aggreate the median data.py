# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 15:32:41 2018

@author: liumo
"""

import pandas as pd

data=pd.read_csv('median_biketime.csv')
data.columns=['startid','endid','bikingtime']
for i in range(25):
    print(i)
    temp=pd.read_csv(str('medianbike_data'+str(i)+'.csv'))
    data=data.append(temp)
    data=data.drop_duplicates()


