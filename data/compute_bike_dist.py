import simplejson
import json
import urllib.request
import csv
dir_url = "https://maps.googleapis.com/maps/api/directions/json?"
key = "AIzaSyBrGxSTS1HWzi8BbgFdwIvu7rgrlMaj_WI"
bike_coord = {}
with open("bikeStation_coordinates.csv") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        bike_coord[row[0]] = row[1] + ',' + row[2]

exist = set()
with open("bike_pair_dist.csv") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        exist.add((row[0],row[1]))
with open("edges/bike_pair_traveltime.csv") as f, open("bike_pair_dist.csv",'a') as file:
    reader = csv.reader(f)
    next(reader)
    # file.write('origin,destination,distance\n')
    for row in reader:
        if row[1]==row[2] or (row[1],row[2]) in exist: continue
        start_station, end_station = row[1], row[2]
        if start_station not in bike_coord:
            print(start_station + 'not in coord')
            continue
        if end_station not in bike_coord:
            print(end_station + 'not in coord')
            continue
        query = dir_url + "origin=" + bike_coord[start_station] + "&destination=" + bike_coord[end_station] +\
                  "&mode=bicycling" + "&key=" + key
        with urllib.request.urlopen(query) as f:
            response = json.loads(f.read().decode())
        if len(response["routes"])==0:
            print("no routes")
            print(query)
            continue
        distance = response["routes"][0]["legs"][0]["distance"]["value"]
        file.write(start_station+','+end_station+','+str(distance)+'\n')
        print(start_station,end_station,str(distance))