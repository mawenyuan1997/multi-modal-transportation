# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 08:21:46 2018

@author: liumo
"""

import pandas as pd

mul=pd.read_csv('data/multimodal.csv')
mul=mul.set_index(['origin','destination'])
best=pd.read_csv('data/multimodal_all_ebike.csv')
best=best.set_index(['origin','destination'])
top1=pd.read_csv('data/iteration_times_1_3.csv')
top1=top1.set_index(['origin','destination'])

top10=pd.read_csv('data/iteration_times_10_3.csv')
top10=top10.set_index(['origin','destination'])


top5=pd.read_csv('data/iteration_times_5_3.csv')
top5=top5.set_index(['origin','destination'])

top50=pd.read_csv('data/iteration_times_50_3.csv')
top50=top50.set_index(['origin','destination'])

top100=pd.read_csv('data/iteration_times_100_3.csv')
top100=top100.set_index(['origin','destination'])



tt=0
db=0
d1=0
d10=0
d5=0
d50=0
d100=0

for (i,j) in top1.index:
    db += mul.loc[(i,j),'time']-best.loc[(i,j),'time']
    d1 += mul.loc[(i,j),'time']-top1.loc[(i,j),'time']
    d10 += mul.loc[(i,j),'time']-top10.loc[(i,j),'time']
    d5 += mul.loc[(i,j),'time']-top5.loc[(i,j),'time']
    d50 += mul.loc[(i,j),'time']-top50.loc[(i,j),'time']
    d100 += mul.loc[(i,j),'time']-top100.loc[(i,j),'time']
    
    tt += mul.loc[(i,j),'time']
    
db
d1
d10    
d10/ db 
d1 / db


db / tt
d10 / tt *100


d1 / tt*100
d5 / tt*100
d10 / tt*100
d50 / tt*100
d100 / tt*100
db / tt*100

comp=pd.read_csv('data/compare_with_api.csv')

comp=comp.set_index(['origin','destination'])
comp

import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import pandas as pd


taxi=pd.read_csv('data/taxitime.csv')
x=np.array(comp['api_time'])
y=np.array(comp['multimodal_time'])
s=1
plt.scatter(x, y, s, c="b", alpha=1, marker='.')
#plt.plot(y,z,c='r',linestyle=':')
plt.plot(y,y,c='r',linestyle=':',label = 'y=x')
plt.xlabel('Google API time')
plt.ylabel('multimodal time')
plt.legend()
plt.title('Compare the multimodal time with Google API transit time')
plt.savefig('Comparison with Google API',dpi = 1000)    

taxi=taxi.set_index(['PULocationID','DOLocationID'])

for (i,j) in comp.index:
    comp.loc[(i,j),'taxitime']=taxi.loc[(i,j),'duration']

plot=comp[(comp.taxitime < 20000 )& (comp.multimodal_time >0)] 
x=np.array(plot['taxitime'])
y=np.array(plot['multimodal_time'])
s=1
plt.scatter(x, y, s, c="b", alpha=1, marker='.')
#plt.plot(y,z,c='r',linestyle=':')
plt.plot(y,y,c='r',linestyle=':')
plt.xlabel('taxi time')
plt.ylabel('multimodal time')
plt.title('Compare the multimodal time with taxi time')
plt.savefig('Comparison with taxi time',dpi = 1000)    

withoutbike=pd.read_csv('data/multimodal_without_bike.csv')
withoutbike=withoutbike.set_index(['origin','destination'])
for (i,j) in comp.index:
    withoutbike.loc[(i,j),'api']=comp.loc[(i,j),'api_time']


withoutbike=withoutbike[withoutbike.api > 0]
x=np.array(withoutbike['api'])
y=np.array(withoutbike['time'])
s=1
plt.scatter(x, y, s, c="b", alpha=1, marker='.')
#plt.plot(y,z,c='r',linestyle=':')
plt.plot(y,y,c='r',linestyle=':')
plt.xlabel('taxi time')
plt.ylabel('multimodal time')
plt.title('Compare the multimodal time with taxi time')
withoutbike.to_csv('result.csv')
#plt.savefig('Comparison with taxi time',dpi = 1000) 



withoutbike=pd.read_csv('data/multimodal_time.csv')
withoutbike=withoutbike.set_index(['origin','destination'])
for (i,j) in temp.index:
    withoutbike.loc[(i,j),'api']=temp.loc[(i,j),'api']


withoutbike=withoutbike[withoutbike.api > 0]
x=np.array(withoutbike['api'])
y=np.array(withoutbike['time'])
s=1
plt.scatter(x, y, s, c="b", alpha=1, marker='.')
#plt.plot(y,z,c='r',linestyle=':')
plt.plot(y,y,c='r',linestyle=':')
plt.xlabel('api time')
plt.ylabel('multimodal time withoutbike')
plt.title('multimodal time withoutbike VS api time')
#plt.savefig('multimodal time withoutbike VS api time',dpi =500)
#withoutbike.to_csv('multimodal time withoutbike VS api time.csv')   


temp=pd.read_csv('multimodal time withoutbike VS api time.csv')
temp=temp.set_index(['origin','destination'])





cp=pd.read_csv('multimodal time vs api time_departuretime.csv')
cp=cp.set_index(['origin','destination'])
cw=pd.read_csv('data/multimodal_time_all_withoutbike.csv')
withoutbike=cw.set_index(['origin','destination'])
for (i,j) in cp.index:
    withoutbike.loc[(i,j),'api']=cp.loc[(i,j),'api_time']
withoutbike.to_csv('withoutbike_api_compare_departure.csv')
withoutbike=pd.read_csv('withoutbike_api_compare_departure.csv')
wr=withoutbike[(withoutbike.origin == 1) | \
               ( withoutbike.origin == 132) | \
                (withoutbike.origin == 138 )| \
                (withoutbike.destination == 1) |\
                (withoutbike.destination == 132) |\
                (withoutbike.destination == 138)]
wo=withoutbike[(withoutbike.origin != 1) & \
               ( withoutbike.origin != 132) & \
                (withoutbike.origin != 138 )& \
                (withoutbike.destination != 1) &\
                (withoutbike.destination != 132) &\
                (withoutbike.destination != 138)]
wr=wr.set_index(['origin','destination'])
wo=wo.set_index(['origin','destination'])
wo=wo[wo.api > 0]
wr=wr[wr.api > 0]
x1=np.array(wo['api'])
y1=np.array(wo['time'])
x2=np.array(wr['api'])
y2=np.array(wr['time'])

s=1
plt.scatter(x1, y1, s, c="blue", alpha=1, marker='.',label='no airport')
plt.scatter(x2, y2, s, c="orange", alpha=1, marker='.',label = 'from / to airport')
#plt.plot(y,z,c='r',linestyle=':')
plt.plot(x1,x1,c='r',linestyle=':')
plt.xlabel('Google API')
plt.ylabel('multimodal time')
plt.title('multimodal time vs Google API time withoutbike')
plt.legend()
plt.savefig('multimodal time vs Google API time withoutbike_departure_time',dpi=300)

wo.to_csv('without_airport_departuretime.csv')




withoutbike=pd.read_csv('data/multimodal_time.csv')
for (i,j) in withoutbike.index:
    if (i,j) in temp.index:
        withoutbike.loc[(i,j),'api']=temp.loc[(i,j),'api']
    

wr=withoutbike[(withoutbike.origin == 1) | \
               ( withoutbike.origin == 132) | \
                (withoutbike.origin == 138 )| \
                (withoutbike.destination == 1) |\
                (withoutbike.destination == 132) |\
                (withoutbike.destination == 138)]
wo=withoutbike[(withoutbike.origin != 1) & \
               ( withoutbike.origin != 132) & \
                (withoutbike.origin != 138 )& \
                (withoutbike.destination != 1) &\
                (withoutbike.destination != 132) &\
                (withoutbike.destination != 138)]
#wo=pd.read_csv('withoutairport1.csv')
wr=wr.set_index(['origin','destination'])
wo=wo.set_index(['origin','destination'])
#wo1=wo1.set_index(['origin','destination'])
for (i,j) in wo.index:
    wo.loc[(i,j),'api']= temp.loc[(i,j),'api']
for (i,j) in wr.index:
    wr.loc[(i,j),'api']= temp.loc[(i,j),'api']


#full=wo1.append(wr)

wo=wo[wo.api > 0]
wr=wr[wr.api > 0]

x1=np.array(wo['api'])
y1=np.array(wo['time'])
x2=np.array(wr['api'])
y2=np.array(wr['time'])
s=1
plt.scatter(x1, y1, s, c="blue", alpha=1, marker='.',label='no airport')
plt.scatter(x2, y2, s, c="orange", alpha=1, marker='.',label = 'from / to airport')
#plt.plot(y,z,c='r',linestyle=':')
plt.plot(x1,x1,c='r',linestyle=':')
plt.xlabel('Google API')
plt.ylabel('multimodal time')
plt.title('multimodal time vs Google API time withoutbike')
plt.legend()
plt.savefig('multimodal time vs Google API time withoutbike',dpi = 500)



#wo.to_csv('withoutairport.csv')   




multimodal=pd.read_csv('data/multimodal.csv')
multimodal=multimodal.set_index(['origin','destination'])
taxitime=pd.read_csv('data/taxitime.csv')
taxitime=taxitime.set_index(['PULocationID','DOLocationID'])
for (i,j) in multimodal.index:
    multimodal.loc[(i,j),'taxitime']=taxitime.loc[(i,j),'duration']
    
man=pd.read_csv('data/taxi_zone_lookup.csv')
man=man[man.Borough=='Manhattan']
manha=pd.DataFrame()
for i in man.LocationID:
    for j in man.LocationID:
        if i !=j:
            try: 
                manha=manha.append(multimodal.loc[i,j])
            except:
                print(str(i)+":"+str(j))

manha=manha[manha.taxitime<40000]
x=np.array(manha['time'])#multimodal time
y=np.array(manha['taxitime'])# taxitime

#z=np.multiply(y,1.1)    
s=1
plt.scatter(x, y, s, c="b", alpha=1, marker='+')
#plt.plot(y,z,c='r',linestyle=':')
plt.plot(y,y,c='r',linestyle=':')
plt.xlabel('multimodal time')
plt.ylabel('taxi time')
plt.title('Manhattan')