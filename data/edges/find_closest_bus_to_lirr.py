import simplejson
import json
import urllib.request
import csv
import numpy as np
dir_url = "https://maps.googleapis.com/maps/api/directions/json?"
key = "AIzaSyCmCsBj8nNVrl5HQ8BIVTojycRW0ebbIcE"
lirr_station = {}
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

exist_lirr_id = set()
with open("closest_bus_to_lirr.csv") as f:
      reader = csv.reader(f)
      for row in reader:
            exist_lirr_id.add(row[0])

with open("../lirr_gtfs/stops.txt") as f:
      reader = csv.reader(f)
      next(reader)
      for row in reader:
            id, lat, lon = row[0], float(row[3]), float(row[4])
            lirr_station[id] = lat, lon

bus_station = {}
with open("../bus_gtfs/stops.txt") as f:
      reader = csv.reader(f)
      next(reader)
      for row in reader:
            # if row[0][-1] in ['N', 'S']:
            #       continue
            id, lat, lon = row[0], float(row[3]), float(row[4])
            bus_station[id] = lat, lon

with open("closest_bus_to_lirr.csv", 'a') as file:
      for lirr_id, (lirr_lat, lirr_lon) in lirr_station.items():
            if lirr_id in exist_lirr_id:
                  continue
            dist = []
            s = str(lirr_lat) + ',' + str(lirr_lon)
            for bus_id, (bus_lat, bus_lon) in bus_station.items():
                  if distance(bus_lat, bus_lon, lirr_lat, lirr_lon) > 4:
                        continue
                  e = str(bus_lat) + ',' + str(bus_lon)
                  query = dir_url + "origin=" + s + "&destination=" + e + \
                        "&mode=walking"+"&key=" + key
                  with urllib.request.urlopen(query) as f:
                        response = json.loads(f.read().decode())
                  if len(response['routes']) == 0:
                        print('no route')
                        continue
                  t = response["routes"][0]["legs"][0]["duration"]["value"]
                  # print((lirr_id, t))
                  dist.append((bus_id, t))
            m = [float('inf'),float('inf'),float('inf'),float('inf'),float('inf')]
            i= ['null','null','null','null','null']
            for id, t in dist:
                  for j in range(5):
                        if t < m[j]:
                              m = m[:j] + [t] + m[j : 4]
                              i = i[:j] + [id] + i[j : 4]
                              break
            print("for lirr station:" + lirr_id)
            print("closest bus stations:" + str(i))
            print("time:" + str(m))
            if i[0] != 'null':
                  file.write(lirr_id+','+str(i[0])+','+str(m[0])+\
                                    ','+str(i[1])+','+str(m[1])+\
                                    ','+str(i[2])+','+str(m[2])+\
                                    ','+str(i[3])+','+str(m[3])+\
                                    ','+str(i[4])+','+str(m[4]))
                  file.write('\n')
            else:
                  print()
