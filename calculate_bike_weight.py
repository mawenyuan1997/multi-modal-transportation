import csv
import pandas as pd
real_usage = {}
basic_usage = {}
best_usage = {}
bike_ids = []
with open('data/bikeStation_coordinates.csv') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        bike_ids.append(row[0])

with open('data/ebike_usage_basic.csv') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        basic_usage[row[0]] = int(row[1])

with open('data/ebike_usage_best.csv') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        best_usage[row[0]] = int(row[1])

with open('data/bikeStartIDs.csv') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        real_usage[row[1]] = int(row[2])

weight = {}
score = {}
for id in bike_ids:
    if id not in real_usage:
        weight[id] = 1
    elif id not in basic_usage:
        weight[id] = real_usage[id] 
    else:
        weight[id] = real_usage[id] / basic_usage[id]
    if id in best_usage:
        score[id] = weight[id] * best_usage[id]
    else:
        score[id] = weight[id]
    print(id,score[id])
print('top 5 are')
score = sorted(list(score.items()), key=lambda x:x[1], reverse=True)
for i in range(5):
    print(score[i])







