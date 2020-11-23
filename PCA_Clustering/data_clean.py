import csv

name, sales, send_time, distance, start_price, delivery_distance, mean_price, score, latitude, longitude = [], [], [], [], [], [], [], [], [], []

file_name = "H:/meituanProject/result/meituan.csv"
with open(file_name, encoding='utf8') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        name.append(row[0])

        sales.append(row[1])
        send_time.append(row[2])
        if "." not in row[3]:
            distance.append(int(row[3]) / 1000)
        else:
            distance.append(float(row[3]))
        start_price.append(int(row[4]))
        if "." not in row[5]:
            delivery_distance.append(int(row[5]))
        else:
            delivery_distance.append(float(row[5]))
        mean_price.append(int(row[6]))
        score.append(float(row[7]))

with open("meituan.csv", 'w', encoding='utf-8-sig', newline="") as f:
    writer = csv.writer(f)
    writer.writerow(
        ['name', 'sales', 'send_time', 'distance', 'start_price', 'delivery_price', 'mean_price', 'score', 'latitude',
         'longitude'])
    for i in range(len(name)):
        writer.writerow(
            [name[i], sales[i], send_time[i], distance[i], start_price[i], delivery_distance[i], mean_price[i],
             score[i]])
