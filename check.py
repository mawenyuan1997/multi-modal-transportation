import csv
import simplejson
import json
import urllib.request
multi_time = {}
with open('data/multimodal.csv') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        multi_time[row[0],row[1]] = float(row[2])

api_time = {}
with open('data/api_time.csv') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        api_time[row[0],row[1]] = float(row[2])

with open('data/compare_with_api.csv','w') as file:
    file.write('origin,destination,api_time,multimodal_time,difference\n')
    for (o,d),t in multi_time.items():
        if (o,d) in api_time:
            file.write(o+','+d+','+str(api_time[o,d])+','+str(multi_time[o,d])+','+str(abs(api_time[o,d]-multi_time[o,d]))+'\n')
        else:
            print(o+','+d+' not in')
            continue
            # query = dir_url + "origin=" + zone_loc[o] + "&destination=" + zone_loc[d] +\
            #         "&departure_time=1532857500&mode=transit" + "&key=" + key
            # with urllib.request.urlopen(query) as f:
            #     response = json.loads(f.read().decode())
            # if len(response["routes"])==0:
            #     print("no routes")
            #     print(query)
            #     continue
            # duration = response["routes"][0]["legs"][0]["duration"]["value"]
            # print(o,d,duration)
            # file.write(o+','+d+','+str(duration)+','+str(multi_time[o,d])+','+str(duration-multi_time[o,d])+'\n')
    

