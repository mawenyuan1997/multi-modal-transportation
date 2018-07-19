import simplejson
import json
import urllib.request
import csv
import numpy as np
dir_url = "https://maps.googleapis.com/maps/api/directions/json?"
key = "AIzaSyBBtnqDUIJ39Y_hzdpWdP-PEXRTEFSSBes"
taxi_station = {}
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

exist_taxi_id = set()
with open("closest_lirr_to_taxi.csv") as f:
      reader = csv.reader(f)
      for row in reader:
            exist_taxi_id.add(row[0])

with open("../zone_latlon.csv") as f:
      reader = csv.reader(f)
      next(reader)
      for row in reader:
            # if row[0][-1] in ['N', 'S']:
            #       continue
            id, lat, lon = row[0], float(row[1]), float(row[2])
            taxi_station[id] = lat, lon
lirr_station = {}
with open("../lirr_gtfs/stops.txt") as f:
      reader = csv.reader(f)
      next(reader)
      for row in reader:
            id, lat, lon = row[0], float(row[3]), float(row[4])
            lirr_station[id] = lat, lon

with open("closest_lirr_to_taxi.csv", 'a') as file:
      for taxi_id, (taxi_lat, taxi_lon) in taxi_station.items():
            if taxi_id in exist_taxi_id:
                  continue
            dist = []
            s = str(taxi_lat) + ',' + str(taxi_lon)
            for lirr_id, (lirr_lat, lirr_lon) in lirr_station.items():
                  if distance(lirr_lat, lirr_lon, taxi_lat, taxi_lon) > 3:
                        continue
                  e = str(lirr_lat) + ',' + str(lirr_lon)
                  query = dir_url + "origin=" + s + "&destination=" + e + \
                        "&mode=walking"+"&key=" + key
                  with urllib.request.urlopen(query) as f:
                        response = json.loads(f.read().decode())
                  if len(response['routes']) == 0:
                        continue
                  t = response["routes"][0]["legs"][0]["duration"]["value"]
                  # print((taxi_id, t))
                  dist.append((lirr_id, t))
            m = [float('inf'),float('inf'),float('inf'),float('inf'),float('inf')]
            i= ['null','null','null','null','null']
            for id, t in dist:
                  for j in range(5):
                        if t < m[j]:
                              m = m[:j] + [t] + m[j : 4]
                              i = i[:j] + [id] + i[j : 4]
                              break
            print("for taxi station:" + taxi_id)
            print("closest lirr stations:" + str(i))
            print("time:" + str(m))
            if i[0] != 'null':
                  file.write(taxi_id+','+str(i[0])+','+str(m[0])+\
                                    ','+str(i[1])+','+str(m[1])+\
                                    ','+str(i[2])+','+str(m[2])+\
                                    ','+str(i[3])+','+str(m[3])+\
                                    ','+str(i[4])+','+str(m[4]))
                  file.write('\n')
            else:
                  print()
