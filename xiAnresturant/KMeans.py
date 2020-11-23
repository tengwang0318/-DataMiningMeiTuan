import numpy as np
import csv
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

np.random.seed(10)


class clustering:
    def __init__(self):
        self.specimen = np.zeros((976, 3))
        self.name = []

    # 使用欧氏距离
    def calculate_distance(self, x, y):
        res = 0
        for i in range(len(x)):
            res += (x[i] - y[i]) ** 2
        return np.sqrt(res)

    # 读取数据并进行归一化处理
    def data_ready(self):

        with open("CleanedData.csv", encoding='utf8') as f:
            reader = csv.reader(f)
            header = next(reader)
            i = 0
            for row in reader:
                self.name.append(row[0])
                self.specimen[i] = [row[1], row[3], row[4]]
                i += 1

        max_numbers_col, min_numbers_col = self.specimen.max(axis=0), self.specimen.min(axis=0)

        for i in range(len(self.specimen)):
            for j in range(len(self.specimen[0])):
                self.specimen[i][j] = (self.specimen[i][j] - min_numbers_col[j]) / (
                        max_numbers_col[j] - min_numbers_col[j]) * 100

    def clustering(self, K):
        # 初始化阶段，先找出3个样本作为初始矩阵向量
        cnt = 1  # 记循环次数
        mean_vector = np.zeros((K, 3))
        temp = set()
        i = 0
        cluster = [[] for _ in range(K)]
        while i != K:
            ran_data = np.random.randint(0, len(self.specimen))
            if ran_data not in temp:
                mean_vector[i] = self.specimen[ran_data]
                cluster[i].append(ran_data)
                temp.add(ran_data)
                i += 1

        while True:
            # 令第i个簇为空集
            cluster[np.random.randint(0, K)] = []

            # 计算出每个样本到各均值向量的距离
            for i in range(0, len(self.specimen)):
                distances = [0 for _ in range(K)]
                for j in range(K):
                    distances[j] = self.calculate_distance(self.specimen[i], mean_vector[j])
                idx = distances.index(min(distances))
                found, m = False, 0
                while m < K and not found:
                    n = 0
                    while n < len(cluster[m]) and not found:
                        if cluster[m][n] == i:
                            cluster[m].remove(i)
                            found = True
                        n += 1
                    m += 1
                cluster[idx].append(i)

            # 计算新的均值向量
            temp = np.zeros((K, len(self.specimen[0])))
            for i in range(K):
                length = len(cluster[i])
                for item in cluster[i]:
                    temp[i] += self.specimen[item]
                for j in range(len(temp[i])):
                    temp[i][j] /= length

            delta = 0
            for m in range(K):
                for n in range(3):
                    delta += (temp[m][n] - mean_vector[m][n]) ** 2
            delta /= 3
            print("第{}次循环的delta为{}".format(cnt, delta))
            print(cluster)
            if delta == 0 or cnt >= 100:

                return cluster
            else:
                mean_vector = temp
            cnt += 1

    # # 分三组，好中差
    # def clustering(self):
    #     # 初始化阶段，先找出3个样本作为初始矩阵向量
    #     cnt = 1  # 记循环次数
    #     # 第一个3为是K值，第二个3为特征值
    #     mean_vector = np.zeros((3, 3))
    #     temp = set()
    #     i = 0
    #     cluster = [[] for _ in range(3)]
    #     while i != 3:
    #         ran_data = np.random.randint(0, len(self.specimen))
    #         if ran_data not in temp:
    #             mean_vector[i] = self.specimen[ran_data]
    #             cluster[i].append(ran_data)
    #             temp.add(ran_data)
    #             i += 1
    #
    #     while True:
    #         # 令第i个簇为空集
    #         cluster[np.random.randint(0, 3)] = []
    #
    #         # 计算出每个样本到各均值向量的距离
    #         for i in range(0, len(self.specimen)):
    #             first_distance, second_distance, third_distance = \
    #                 self.calculate_distance(self.specimen[i], mean_vector[0]), \
    #                 self.calculate_distance(self.specimen[i], mean_vector[1]), \
    #                 self.calculate_distance(self.specimen[i], mean_vector[2])
    #             if first_distance == min(first_distance, second_distance, third_distance):
    #                 found, m = False, 0
    #                 while m < 3 and not found:
    #                     n = 0
    #                     while n < len(cluster[m]) and not found:
    #                         if cluster[m][n] == i:
    #                             cluster[m].remove(i)
    #                             found = True
    #                         n += 1
    #                     m += 1
    #                 cluster[0].append(i)
    #             elif second_distance == min(first_distance, second_distance, third_distance):
    #
    #                 found, m = False, 0
    #                 while m < 3 and not found:
    #                     n = 0
    #                     while n < len(cluster[m]) and not found:
    #                         if cluster[m][n] == i:
    #                             cluster[m].remove(i)
    #                             found = True
    #                         n += 1
    #                     m += 1
    #                 cluster[1].append(i)
    #
    #             else:
    #                 found, m = False, 0
    #                 while m < 3 and not found:
    #                     n = 0
    #                     while n < len(cluster[m]) and not found:
    #                         if cluster[m][n] == i:
    #                             cluster[m].remove(i)
    #                             found = True
    #                         n += 1
    #                     m += 1
    #                 cluster[2].append(i)
    #
    #         # 计算新的均值向量
    #         temp = np.zeros((3, len(self.specimen[0])))
    #         for i in range(3):
    #             length = len(cluster[i])
    #             for item in cluster[i]:
    #                 temp[i] += self.specimen[item]
    #             for j in range(len(temp[i])):
    #                 temp[i][j] /= length
    #
    #         delta = 0
    #         for i in range(3):
    #             for j in range(3):
    #                 delta += (temp[i][j] - mean_vector[i][j]) ** 2
    #         delta /= 3
    #         print("第{}次循环的delta为{}".format(cnt, delta))
    #         print(cluster)
    #         if delta == 0:
    #             return cluster
    #         else:
    #             mean_vector = temp
    #         cnt += 1


if __name__ == '__main__':
    test = clustering()
    test.data_ready()
    res = test.clustering(5)
    fig = plt.figure()
    ax1 = plt.axes(projection='3d')
    first_feature1, first_feature2, first_feature3 = [], [], []
    second_feature1, second_feature2, second_feature3 = [], [], []
    third_feature1, third_feature2, third_feature3 = [], [], []
    fourth_feature1, fourth_feature2, fourth_feature_3 = [], [], []
    fifth_feature1, fifth_feature2, fifth_feature3 = [], [], []
    with open('CleanedData.csv', encoding='utf8') as f:
        reader = csv.reader(f)
        header = next(reader)
        i = 0
        for row in reader:
            if i in res[0]:
                first_feature1.append(float(row[1]))
                first_feature2.append(float(row[3]))
                first_feature3.append(float(row[4]))
            elif i in res[1]:
                second_feature1.append(float(row[1]))
                second_feature2.append(float(row[3]))
                second_feature3.append(float(row[4]))
            elif i in res[2]:
                third_feature1.append(float(row[1]))
                third_feature2.append(float(row[3]))
                third_feature3.append(float(row[4]))
            elif i in res[3]:
                fourth_feature1.append(float(row[1]))
                fourth_feature2.append(float(row[3]))
                fourth_feature_3.append(float(row[4]))
            else:
                fifth_feature1.append(float(row[1]))
                fifth_feature2.append(float(row[3]))
                fifth_feature3.append(float(row[4]))
            i += 1
    plt.rcParams['font.sans-serif'] = ['SimHei']
    ax1.scatter3D(first_feature1, first_feature2, first_feature3)
    ax1.scatter3D(second_feature1, second_feature2, second_feature3, c='orange')
    ax1.scatter3D(third_feature1, third_feature2, third_feature3, c='green')
    ax1.scatter3D(fourth_feature1, fourth_feature2, fourth_feature_3, c='red')
    ax1.scatter3D(fifth_feature1, fifth_feature2, fifth_feature3, c='purple')
    ax1.set_xlabel("得分")
    ax1.set_ylabel("平均价格", rotation=50)
    ax1.set_zlabel("评论数量", rotation=90)
    plt.title("西安市美团店家信息聚类结果")
    plt.savefig('.//result//西安市美团美食店家聚类')
    plt.show()




