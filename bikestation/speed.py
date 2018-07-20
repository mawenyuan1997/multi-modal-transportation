# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 18:08:24 2018

@author: liumo
"""

import pandas as pd
speed=pd.read_csv('yellow_tripdata_2017-06-complete.csv')
speed=speed.groupby(['PULocationID','DOLocationID']).mean()
speed.columns
zone=pd.read_csv('taxi _zone_lookup.csv')
manha=zone[zone.Borough=='Manhattan']
for k in zone.Borough.drop_duplicates():
    print(k)
    boro=zone[zone.Borough==k]
    for i in boro.LocationID:
        for j in boro.LocationID:
            speed.loc[(i,j),'borough']=k

meanspeed=speed.groupby('borough').mean()
meanspeed.to_csv('avg speed in different borough.csv')
medianspeed=speed.groupby('borough').median()
medianspeed.to_csv('median speed in different borough.csv')


#regenerate the new data file

data=pd.read_csv('multimode_time.csv',header=None)
data=pd.DataFrame(data.values, columns=['PUloc','DOloc','multitime']) 
data=data.set_index(['PUloc','DOloc'])
for (i,j) in data.index:
    try:
        data.loc[(i,j),'distance']=speed.loc[(i,j),'trip_distance']
        data.loc[(i,j),'taxitime']=speed.loc[(i,j),'taxitime']
    except:
        print(i,j)

data.to_csv('newdatafile.csv')

'''
Only in Manhattan

'''



manhattan=pd.DataFrame()
for i in manha.LocationID:
    for j in manha.LocationID:
        try:
            manhattan=manhattan.append(data.loc[(i,j),])
        except:
            print(i,j)
'''

plot

'''

import matplotlib.pyplot as plt
import numpy as np
#import matplotlib

manhattan=manhattan[manhattan.taxitime<20000]
x=np.array(manhattan.distance)
y=np.array(manhattan.taxitime)
z=np.array(manhattan.multitime)
r=np.array(np.divide(z,y))
s=7

plt.scatter(x,z,s,c='y',alpha = 1,marker='.',label='multimodal time')
plt.scatter(x, y, s, c="b", alpha=0.8, marker='+',label='taxi time')
plt.legend()
plt.axis([0,16,0,10000])
plt.xlabel('distance in miles')
plt.ylabel('time')
plt.savefig('time-distance',dpi=1000)

##
plt.xlabel('distance in miles')
plt.ylabel('ratio:  multimodal time/ taxi time ')
plt.scatter(x,r,s,c='b',alpha = 0.8,marker='.')
#plt.axis([0,16,0,4])
plt.savefig('ratio-distance',dpi=1000)
