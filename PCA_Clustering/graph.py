import matplotlib.pyplot as plt
import csv

sales, send_time, distance, start_price, delivery_price, mean_price, score = [], [], [], [], [], [], []
with open("meituan.csv", encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        sales.append(int(row[1]))
        send_time.append(int(row[2]))
        distance.append(float(row[3]))
        start_price.append(float(row[4]))
        delivery_price.append(float(row[5]))
        mean_price.append(float(row[6]))
        score.append(float(row[7]))
fig = plt.figure()
plt.rcParams['font.sans-serif'] = ['SimHei']
# 订单量分类
# (0,100) && (100,300) && (300,500) && (500,10000) && (1000,2000) && >2000
temp_sales = [0] * 6
for item in sales:
    if item < 100:
        temp_sales[0] += 1
    elif 100 <= item < 300:
        temp_sales[1] += 1
    elif 300 <= item < 500:
        temp_sales[2] += 1
    elif 500 <= item < 1000:
        temp_sales[3] += 1
    elif 1000 <= item < 2000:
        temp_sales[4] += 1
    else:
        temp_sales[5] += 1
plt.title("西北大学长安校区周边外卖月销量情况的饼状图")
plt.pie(temp_sales, autopct='%1.1f%%', labels=['0-99', '100-299','299-499', '500-999', '1000-1999', '2000-inf'])
plt.savefig("H:\\meituanProject\\graph\\西北大学长安校区周边外卖销量情况的饼状图.png")
plt.show()
# 按照预计送达时间分类
# (0,30) && (30,40) && (40,50) && (50,60) && (60,inf)
temp_send_time = [0] * 5
for item in send_time:
    if item < 30:
        temp_send_time[0] += 1
    elif 30 <= item < 40:
        temp_send_time[1] += 1
    elif 40 <= item < 50:
        temp_send_time[2] += 1
    elif 50 <= item < 60:
        temp_send_time[3] += 1
    else:
        temp_send_time[4] += 1

plt.title("西北大学长安校区周边外卖预计送达时间饼状图")
plt.pie(temp_send_time, autopct='%1.1f%%', labels=['0-29min', '30min-39min', '40min-49min', '50min-59min', '60min-inf'])

plt.savefig("H:\\meituanProject\\graph\\西北大学长安校区周边外卖预计送达时间饼状图.png")
plt.show()
# 距离
# (0,0.5),(0.5,1),(1,2),(2,3),(3,4),(4,5),(5,7),(7,inf)
temp_distance = [0] * 8
for item in distance:
    if item < 0.5:
        temp_distance[0] += 1
    elif 0.5 <= item < 1:
        temp_distance[1] += 1
    elif 1 <= item < 2:
        temp_distance[2] += 1
    elif 2 <= item < 3:
        temp_distance[3] += 1
    elif 3 <= item < 4:
        temp_distance[4] += 1
    elif 4 <= item < 5:
        temp_distance[5] += 1
    elif 5 <= item < 7:
        temp_distance[6] += 1
    else:
        temp_distance[7] += 1
plt.title("西北大学长安校区周边外卖距离饼状图")

plt.pie(temp_distance, autopct='%1.1f%%',
        labels=['0-0.5km', '0.5km-1km', '1km-2km', '2km-3km', '3km-4km', '4km-5km', '5km-7km', '7km-inf'])
plt.savefig("H:\\meituanProject\\graph\\西北大学长安校区周边外卖距离饼状图.png")
plt.show()
# 起始配送费用
# (0,10),(10,20),(20,30),(30,50),(50,100),(100,inf)
temp_start_price = [0] * 6
for item in start_price:
    if item < 10:
        temp_start_price[0] += 1
    elif 10 <= item < 20:
        temp_start_price[1] += 1
    elif 20 <= item < 30:
        temp_start_price[2] += 1
    elif 30 <= item < 50:
        temp_start_price[3] += 1
    elif 50 <= item < 100:
        temp_start_price[4] += 1
    else:
        temp_start_price[5] += 1
plt.title("西北大学长安校区周边外卖起送价饼状图")
plt.pie(temp_start_price, autopct='%1.1f%%', labels=['0元-10元', '10元-20元', '20元-30元', '30元-50元', '50元-100元', '100元-inf'])

plt.savefig("H:\\meituanProject\\graph\\西北大学长安校区周边外卖起送价饼状图.png")
plt.show()
# 配送费用
# (0,2),(2,5),(5,7),(7,10),(10,inf)
temp_delivery_price = [0] * 5
for item in delivery_price:
    if item <= 2:
        temp_delivery_price[0] += 1
    elif 2 < item <= 5:
        temp_delivery_price[1] += 1
    elif 5 < item <= 7:
        temp_delivery_price[2] += 1
    elif 7 < item <= 10:
        temp_delivery_price[3] += 1
    else:
        temp_delivery_price[4] += 1
plt.title("西北大学长安校区周边外卖配送费用饼状图")
plt.pie(temp_delivery_price, autopct='%1.1f%%', labels=['0-2元', '2元-5元', '5元-7元', '7元-10元', '10元-inf'])

plt.savefig("H:\\meituanProject\\graph\\西北大学长安校区周边外卖配送费用饼状图.png")
plt.show()
# 平均价格，剔除异常值
# (10,20),(20,30),(30,40),(40,50),(50,inf)
temp_mean_price = [0] * 5
for item in mean_price:
    if 10 <= item < 20:
        temp_mean_price[0] += 1
    elif 20 <= item < 30:
        temp_mean_price[1] += 1
    elif 30 <= item < 40:
        temp_mean_price[2] += 1
    elif 40 <= item < 50:
        temp_mean_price[3] += 1
    else:
        temp_mean_price[4] += 1
plt.title("西北大学长安校区周边外卖人均价格饼状图")
plt.pie(temp_mean_price, autopct='%1.1f%%', labels=['10元-20元', '20元-30元', '30元-40元', '40元-50元', '50元-inf'])
plt.savefig("H:\\meituanProject\\graph\\西北大学长安校区周边外卖人均价格饼状图.png")
plt.show()
# 得分情况
# (0,3),(3,3.5),(3.5,4),(4,4.5),(4.5,4.8),(4.8,5)
temp_score = [0] * 6
for item in score:
    if item < 3:
        temp_score[0] += 1
    elif 3 <= item < 3.5:
        temp_score[1] += 1
    elif 3.5 <= item < 4:
        temp_score[2] += 1
    elif 4 <= item < 4.5:
        temp_score[3] += 1
    elif 4.5 <= item < 4.8:
        temp_score[4] += 1
    else:
        temp_score[5] += 1
plt.title("西北大学长安校区周边外卖平均得分饼状图")

plt.pie(temp_score, autopct='%1.1f%%', labels=['0-3分', '3分-3.5分', '3.5分-4分', '4分-4.5分', '4.5分-4.8分', '4.8分-5分'])
plt.savefig("H:\\meituanProject\\graph\\西北大学长安校区周边外卖平均得分饼状图.png")
plt.show()
