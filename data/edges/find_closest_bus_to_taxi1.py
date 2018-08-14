import simplejson
import json
import urllib.request
import csv
import numpy as np
dir_url = "https://maps.googleapis.com/maps/api/directions/json?"
key = "AIzaSyD9qLYqbM5x7BKNlyDyJFQU74qU-irhMN8"
taxi_station = {}
one_mile = 1.609344
def distance(lat1, lon1, lat2, lon2):
      from math import sin, cos, sqrt, atan2, radians
      R = 6373.0
      lat1 = radians(lat1)
      lon1 = radians(lon1)
      lat2 = radians(lat2)
      lon2 = radians(lon2)
      dlon = lon2 - lon1
      dlat = lat2 - lat1
      a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
      c = 2 * atan2(sqrt(a), sqrt(1 - a))
      return R * c



with open("../zone_latlon1.csv") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
            id, lat, lon = row[0], float(row[1]), float(row[2])
            taxi_station[id] = lat, lon

bus_station = {}
#for zone in ['Manhattan','Bronx','Brooklyn','Staten','Queens','NYC']:
for zone in ['Queens']:
    with open("../bus_gtfs/"+zone+"_stops.txt") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
                # if row[0][-1] in ['N', 'S']:
                #       continue
                if zone=='Staten':
                    id, lat, lon = row[0], float(row[2]), float(row[3])
                else:
                    id, lat, lon = row[0], float(row[3]), float(row[4])
                bus_station[id] = lat, lon

no_route = False
with open("closest_bus_to_taxi1.csv", 'a') as file:
        for taxi_id, (taxi_lat, taxi_lon) in taxi_station.items():
            if taxi_id != '132':
                continue
            print(taxi_id)
            file.write('\n'+taxi_id)
            dist = []
            s = str(taxi_lat) + ',' + str(taxi_lon)
            for bus_id, (bus_lat, bus_lon) in bus_station.items():
                  if distance(bus_lat, bus_lon, taxi_lat, taxi_lon) > one_mile *2:
                        continue
                  e = str(bus_lat) + ',' + str(bus_lon)
                  query = dir_url + "origin=" + s + "&destination=" + e + \
                        "&mode=walking"+"&key=" + key
                  with urllib.request.urlopen(query) as f:
                        response = json.loads(f.read().decode())
                  if len(response['routes']) == 0:
                        print('no route')
                        if response['status']=="ZERO_RESULTS":
                              continue
                        print(query)
                        no_route = True
                        break
                  t = response["routes"][0]["legs"][0]["duration"]["value"]
                  # print((taxi_id, t))
                  file.write(','+bus_id)
                  file.write(','+str(t))
            if no_route: break
            file.write(','+'null')