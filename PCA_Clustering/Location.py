import requests
import csv
import json

final_longitude, final_latitude = [], []

key_words = []
with open("meituan.csv", encoding="utf8") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        key_words.append(row[0])
for key_word in key_words:
    api = "https://restapi.amap.com/v3/place/text?key=9013e06e0781b4f712e29a674d2c0d2f&keywords=" + str(
        key_word) + "&city=西安&output=json"
    response = requests.get(api)
    print(key_word)
    try:
        longitude, latitude = json.loads(response.text)['pois'][0]['location'].split(",")
    except IndexError:
        try:
            longitude, latitude = json.loads(response.text)['sug_address']['location'].split(',')
        except KeyError:
            longitude, latitude = 0, 0
    final_longitude.append(longitude)
    final_latitude.append(latitude)
with open("meituan.csv", encoding='utf8') as f:
    reader = csv.reader(f)
    next(reader)
    name, sales, send_time, distance, start_price, delivery_price, mean_price, score = [], [], [], [], [], [], [], []
    for row in reader:
        name.append(row[0])
        sales.append(row[1])
        send_time.append(row[2])
        distance.append(row[3])
        start_price.append(row[4])
        delivery_price.append(row[5])
        mean_price.append(row[6])
        score.append(row[7])

with open("meituan.csv", 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(
        ['name', 'sales', 'send_time', 'distance', 'start_price', 'delivery_price', 'mean_price', 'score', 'latitude',
         'longitude'])
    for i in range(len(name)):
        writer.writerow(
            [name[i], sales[i], send_time[i], distance[i], start_price[i], delivery_price[i], mean_price[i], score[i],
             final_latitude[i],
             final_longitude[i]])

