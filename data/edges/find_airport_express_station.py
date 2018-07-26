import simplejson
import json
import urllib.request
import csv
import numpy as np
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

port_authority = (40.756936, -73.990275)
byrant_park = (40.753597, -73.983233)
grand_central = (40.752726, -73.977229)
def add(f, lat, lon, id):
    if distance(lat, lon, port_authority[0], port_authority[1]) < 0.5:
        f.write('port_authority,' + id + ',3000' + '\n')
    elif distance(lat, lon, byrant_park[0], byrant_park[1]) < 0.5:
        f.write('byrant_park,' + id + ',3600' + '\n')
    elif distance(lat, lon, grand_central[0], grand_central[1]) < 0.5:
        f.write('grand_central,' + id + ',4200' + '\n')

with open('Newark_express_stations.csv','w') as file:
    with open("../lirr_gtfs/stops.txt") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            id, lat, lon = row[0], float(row[3]), float(row[4])
            add(file,lat,lon,'lirr_'+id)
            
    for zone in ['Brooklyn', 'Bronx', 'Queens', 'Manhattan', 'Staten']:
        with open("../bus_gtfs/"+zone+"_stops.txt") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if zone=='Staten':
                        id, lat, lon = row[0], float(row[2]), float(row[3])
                else:
                        id, lat, lon = row[0], float(row[3]), float(row[4])
                add(file,lat,lon,id)
    with open("../bikeStation_coordinates.csv") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            id, lat, lon = row[0], float(row[1]), float(row[2])
            add(file,lat,lon,'bike_'+id)
    with open("../zone_latlon.csv") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            id, lat, lon = row[0], float(row[1]), float(row[2])
            add(file,lat,lon,id)
    with open("../subway_gtfs/stops.txt") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            id, lat, lon = row[0], float(row[4]), float(row[5])
            add(file,lat,lon,id)
                
