import csv

names = []
scores = []
addresses = []
mean_prices = []
comments = []
# 评论、得分、人均价格缺失情况，直接取0
with open("dataminer.csv", encoding='utf8') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        names.append(row[0])
        temp_score, address_price = row[1].split(" ")[:2]
        score, comment = temp_score.split("分")
        try:
            scores.append(float(score))
        except ValueError:

            scores.append(0)
        try:
            comments.append(int(comment[:-3]))
        except ValueError:
            comments.append(0)

        address, price = address_price.split("人均")
        price = price[1:]
        addresses.append(address)

        try:
            mean_prices.append(int(price))
        except ValueError:
            mean_prices.append(0)
with open("CleanedData.csv", 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["name", 'scores', 'address', 'mean_price', 'comment'])
    for i in range(len(names)):
        if comments[i] != 0 and scores[i] != 0 and mean_prices[i] != 0:
            writer.writerow([names[i], scores[i], addresses[i], mean_prices[i], comments[i]])
