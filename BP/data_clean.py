import csv

name, sales, send_time, distance, start_price, delivery_price, mean_price, score, restaurant_type = [], [], [], [], [], [], [], [], []
with open("meituanBPclean.csv", encoding='utf8') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        if 6 <= float(row[3]) < 100:
            continue
        elif float(row[3]) >= 100:
            distance.append(float(row[3]) / 1000)
        else:
            distance.append(float(row[3]))
        name.append(row[0])
        sales.append(int(row[1]))
        send_time.append(float(row[2]))

        start_price.append(float(row[4]))
        delivery_price.append(float(row[5]))
        mean_price.append(float(row[6]))
        score.append(float(row[7]))
        restaurant_type.append(int(row[8]))
with open("final_data.csv", 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['name', 'sales', 'send_time', 'distance', 'start_price', 'delivery_price', 'mean_price', 'score',
                     'restaurant_type'])
    for i in range(len(name)):
        writer.writerow(
            [name[i], sales[i], send_time[i], distance[i], start_price[i], delivery_price[i], mean_price[i], score[i],
             restaurant_type[i]])
