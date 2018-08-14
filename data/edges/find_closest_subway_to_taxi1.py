# -*- coding: utf-8 -*-
"""
Created on Mon Aug  6 23:32:19 2018

@author: liumo
"""

import simplejson
import json
import urllib.request
import csv
import numpy as np
dir_url = "https://maps.googleapis.com/maps/api/directions/json?"
#key = "AIzaSyBBtnqDUIJ39Y_hzdpWdP-PEXRTEFSSBes"
key = 'AIzaSyD9qLYqbM5x7BKNlyDyJFQU74qU-irhMN8'
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
one_mile = 1.609344


'''
exist_taxi_id = set()
with open("closest_subway_to_taxi.csv") as f:
      reader = csv.reader(f)
      for row in reader:
            exist_taxi_id.add(row[0])
'''
with open("../zone_latlon1.csv") as f:
      reader = csv.reader(f)
      next(reader)
      for row in reader:
            # if row[0][-1] in ['N', 'S']:
            #       continue
            id, lat, lon = row[0], float(row[1]), float(row[2])
            taxi_station[id] = lat, lon
subway_station = {}
with open("../subway_gtfs/stops.txt") as f:
      reader = csv.reader(f)
      next(reader)
      for row in reader:
            id, lat, lon = row[0], float(row[4]), float(row[5])
            if id[-1] not in ['N','S']:
                subway_station[id] = lat, lon            

no_route = False
with open("closest_subway_to_taxi1.csv", 'a') as file:
      for taxi_id, (taxi_lat, taxi_lon) in taxi_station.items():
            file.write(taxi_id)
            dist = []
            s = str(taxi_lat) + ',' + str(taxi_lon)
            for subway_id, (subway_lat, subway_lon) in subway_station.items():
                  if distance(taxi_lat, taxi_lon, subway_lat, subway_lon) > one_mile:
                        continue
                  e = str(subway_lat) + ',' + str(subway_lon)
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
                  # print((subway_id, t))
                  file.write(','+subway_id)
                  file.write(','+str(t))                                                   
                  #dist.append((subway_id, t))
            if no_route: break
            file.write(','+'null'+'\n')
            print(taxi_id)






#########################

