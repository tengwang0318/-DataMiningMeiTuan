import numpy as np
import csv
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class clustering:
    def __init__(self):
        self.specimen = np.zeros((125, 3))

    # 使用欧氏距离
    def calculate_distance(self, x, y):
        res = 0
        for i in range(len(x)):
            res += (x[i] - y[i]) ** 2
        return np.sqrt(res)

    # 读取数据并进行归一化处理
    def data_ready(self):

        with open("meituan.csv", encoding='utf8') as f:
            reader = csv.reader(f)
            header = next(reader)
            i = 0
            for row in reader:
                self.specimen[i] = [row[1], row[2], row[3]]
                i += 1

        max_numbers_col, min_numbers_col = self.specimen.max(axis=0), self.specimen.min(axis=0)

        for i in range(len(self.specimen)):
            for j in range(len(self.specimen[0])):
                self.specimen[i][j] = (self.specimen[i][j] - min_numbers_col[j]) / (
                        max_numbers_col[j] - min_numbers_col[j]) * 100

    # 分三组，好中差
    def clustering(self):
        # 初始化阶段，先找出3个样本作为初始矩阵向量
        cnt = 1  # 记循环次数
        mean_vector = np.zeros((3, 3))
        temp = set()
        i = 0
        cluster = [[] for _ in range(3)]
        while i != 3:
            ran_data = np.random.randint(0, len(self.specimen))
            if ran_data not in temp:
                mean_vector[i] = self.specimen[ran_data]
                cluster[i].append(ran_data)
                temp.add(ran_data)
                i += 1

        while True:
            # 令第i个簇为空集
            cluster[np.random.randint(0, 3)] = []

            # 计算出每个样本到各均值向量的距离
            for i in range(0, len(self.specimen)):
                first_distance, second_distance, third_distance = \
                    self.calculate_distance(self.specimen[i], mean_vector[0]), \
                    self.calculate_distance(self.specimen[i], mean_vector[1]), \
                    self.calculate_distance(self.specimen[i], mean_vector[2])
                if first_distance == min(first_distance, second_distance, third_distance):
                    found, m = False, 0
                    while m < 3 and not found:
                        n = 0
                        while n < len(cluster[m]) and not found:
                            if cluster[m][n] == i:
                                cluster[m].remove(i)
                                found = True
                            n += 1
                        m += 1
                    cluster[0].append(i)
                elif second_distance == min(first_distance, second_distance, third_distance):

                    found, m = False, 0
                    while m < 3 and not found:
                        n = 0
                        while n < len(cluster[m]) and not found:
                            if cluster[m][n] == i:
                                cluster[m].remove(i)
                                found = True
                            n += 1
                        m += 1
                    cluster[1].append(i)

                else:
                    found, m = False, 0
                    while m < 3 and not found:
                        n = 0
                        while n < len(cluster[m]) and not found:
                            if cluster[m][n] == i:
                                cluster[m].remove(i)
                                found = True
                            n += 1
                        m += 1
                    cluster[2].append(i)

            # 计算新的均值向量
            temp = np.zeros((3, len(self.specimen[0])))
            for i in range(3):
                length = len(cluster[i])
                for item in cluster[i]:
                    temp[i] += self.specimen[item]
                for j in range(len(temp[i])):
                    temp[i][j] /= length

            delta = 0
            for i in range(3):
                for j in range(3):
                    delta += (temp[i][j] - mean_vector[i][j]) ** 2
            delta /= 3
            print("第{}次循环的delta为{}".format(cnt, delta))
            print(cluster)
            if delta == 0:
                return cluster
                break
            else:
                mean_vector = temp
            cnt += 1


if __name__ == '__main__':
    test = clustering()
    test.data_ready()
    res = test.clustering()
    fig = plt.figure()
    ax1 = plt.axes(projection='3d')
    first_feature1, first_feature2, first_feature3 = [], [], []
    second_feature1, second_feature2, second_feature3 = [], [], []
    third_feature1, third_feature2, third_feature3 = [], [], []
    with open('meituan.csv', encoding='utf8') as f:
        reader = csv.reader(f)
        header = next(reader)
        i = 0
        for row in reader:
            if i in res[0]:
                first_feature1.append(float(row[1]))
                first_feature2.append(float(row[2]))
                first_feature3.append(float(row[3]))
            elif i in res[1]:
                second_feature1.append(float(row[1]))
                second_feature2.append(float(row[2]))
                second_feature3.append(float(row[3]))
            else:
                third_feature1.append(float(row[1]))
                third_feature2.append(float(row[2]))
                third_feature3.append(float(row[3]))

            i += 1
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    ax1.scatter3D(first_feature1, first_feature2, first_feature3, c='blue')
    ax1.scatter3D(second_feature1, second_feature2, second_feature3, c='green')
    ax1.scatter3D(third_feature1,third_feature2,third_feature3,c="red")
    ax1.set_xlabel("销售量")
    ax1.set_ylabel("配送时间")
    ax1.set_zlabel("距离")
    plt.title("西北大学外卖店家信息聚类结果")
    plt.savefig("未经PCA出来后的聚类情况")
    plt.show()
