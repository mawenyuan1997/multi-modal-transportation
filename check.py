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

zone_loc = {}
with open('data/zone_latlon.csv') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        zone_loc[row[0]] = row[1] + ',' + row[2]

exist = set()
with open('data/sanity_check.csv') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        exist.add((row[0], row[1]))

dir_url = "https://maps.googleapis.com/maps/api/directions/json?"
key = "AIzaSyBBtnqDUIJ39Y_hzdpWdP-PEXRTEFSSBes"
api_time = {}
with open('data/sanity_check.csv','a') as file:
    file.write('origin,destination,multimodal time by dijkstra,api time\n')
    for (o,d), t in multi_time.items():
        if (o,d) in exist:
            continue
        query = dir_url + "origin=" + zone_loc[o] + "&destination=" + zone_loc[d] +\
                    "&departure_time=1532857500&mode=transit" + "&key=" + key
        with urllib.request.urlopen(query) as f:
            response = json.loads(f.read().decode())
        if len(response["routes"])==0:
            print("no routes")
            continue
        duration = response["routes"][0]["legs"][0]["duration"]["value"]
        file.write(o+','+d+','+str(t)+','+str(duration)+'\n')
        print(o+','+d+','+str(t)+','+str(duration))


