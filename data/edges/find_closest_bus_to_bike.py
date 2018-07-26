import simplejson
import json
import urllib.request
import csv
import numpy as np
dir_url = "https://maps.googleapis.com/maps/api/directions/json?"
key = "AIzaSyDSkg58EylmbXSOr3YZNRgC6lfF7LhoVO4"
bike_station = {}
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

exist_bike_id = set()
with open("closest_bus_to_bike.csv") as f:
      reader = csv.reader(f)
      for row in reader:
            exist_bike_id.add(row[0])

with open("../bikeStation_coordinates.csv") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
            id, lat, lon = row[0], float(row[1]), float(row[2])
            bike_station[id] = lat, lon

bus_station = {}
for zone in ['Brooklyn', 'Bronx', 'Queens', 'Manhattan', 'Staten']:
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
with open("closest_bus_to_bike.csv", 'a') as file:
        for bike_id, (bike_lat, bike_lon) in bike_station.items():
            if bike_id in exist_bike_id:
                  continue
            dist = []
            s = str(bike_lat) + ',' + str(bike_lon)
            for bus_id, (bus_lat, bus_lon) in bus_station.items():
                  if distance(bus_lat, bus_lon, bike_lat, bike_lon) > 1:
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
                  # print((bike_id, t))
                  dist.append((bus_id, t))
            if no_route: break
            m = [float('inf'),float('inf'),float('inf'),float('inf'),float('inf')]
            i= ['null','null','null','null','null']
            for id, t in dist:
                  for j in range(5):
                        if t < m[j]:
                              m = m[:j] + [t] + m[j : 4]
                              i = i[:j] + [id] + i[j : 4]
                              break
            
            if i[0] != 'null':
                  print("for bike station:" + bike_id)
                  print("closest bus stations:" + str(i))
                  print("time:" + str(m))
                  file.write(bike_id+','+str(i[0])+','+str(m[0])+\
                                    ','+str(i[1])+','+str(m[1])+\
                                    ','+str(i[2])+','+str(m[2])+\
                                    ','+str(i[3])+','+str(m[3])+\
                                    ','+str(i[4])+','+str(m[4]))
                  file.write('\n')
            else:
                  print("for bike station:" + bike_id)
                  print("closest bus stations:" + str(i))
