import simplejson
import json
import urllib.request
import csv
import numpy as np
dir_url = "https://maps.googleapis.com/maps/api/directions/json?"
ele_url = "https://maps.googleapis.com/maps/api/elevation/json?"
# key = "AIzaSyDzn_sbm8dbmfbkqdsxSDeIbI5HRq9lYXE"
key = "AIzaSyBBtnqDUIJ39Y_hzdpWdP-PEXRTEFSSBes"
station_pair_set = set()
with open("trip_info_incomplete.csv") as f:
      reader = csv.reader(f)
      data = [r for r in reader]
for line in data:
      station_pair_set.add((line[0], line[1]))

with open("201804-fordgobike-tripdata.csv") as f:
      reader = csv.reader(f)
      next(reader)
      data = [r for r in reader]

num = 1

with open('trip_info_incomplete.csv','a') as file:
      for line in data:
            num = num + 1
            start_id, end_id = line[3], line[7]
            print("for row " + str(num))
            print("processing pair:" + start_id + "," + end_id)
            if (start_id, end_id) in station_pair_set:
                  print("already in")
                  continue
            if start_id == end_id:
                  print("start and end station are same")
                  continue
            station_pair_set.add((start_id, end_id))

            start_station = line[5] + "," + line[6]
            end_station = line[9] + "," + line[10]
            query = dir_url + "origin=" + start_station + "&destination=" + end_station +\
                  "&mode=bicycling" + "&key=" + key
            print("accessing direction api")
            with urllib.request.urlopen(query) as f:
                  response = json.loads(f.read().decode())
            if len(response["routes"])==0:
                  print("no routes")
                  continue
            distance = response["routes"][0]["legs"][0]["distance"]["value"]
            duration = float(line[0])

            steps = response["routes"][0]["legs"][0]["steps"]
            max_tan = float("-inf")
            start_lat, start_lon = line[5], line[6]
            skip = len(steps) // 10
            num_step = 0
            dist = 0
            for step in steps:
                  dist = dist + step["distance"]["value"]
                  if skip != 0 and num_step % skip != 0:
                        num_step = num_step + 1
                        continue
                  num_step = num_step + 1
                  end_lat, end_lon = str(step["end_location"]["lat"]), str(step["end_location"]["lng"])
                  # dist = step["distance"]["value"]
                  print("accessing elevation api for start station")
                  query1 = ele_url + "locations=" + start_lat + "," + start_lon + "&key=" + key
                  with urllib.request.urlopen(query1) as f:
                        response = json.loads(f.read().decode())
                  if len(response['results']) == 0:
                        print("error:no result")
                        continue
                  start_elevation = float(response['results'][0]['elevation'])
                  print("accessing elevation api for end station")
                  query2 = ele_url + "locations=" + end_lat + "," + end_lon + "&key=" + key
                  with urllib.request.urlopen(query2) as f:
                        response = json.loads(f.read().decode())
                  if len(response['results']) == 0:
                        print("error:no result")
                        continue
                  end_elevation = float(response['results'][0]['elevation'])
                  if dist < 1e-6:
                        tan = float("-inf")
                  else:
                        tan = float((end_elevation - start_elevation) / dist)
                  max_tan = max(max_tan, tan)
                  dist = 0
                  start_lat, start_lon = end_lat, end_lon
            if start_id != end_id:
                  print("distance:" + str(distance) + "   max tan:" + str(max_tan))
                  file.write(start_id + "," + end_id + "," + str(distance)  + "," + str(max_tan))
                  file.write('\n')
