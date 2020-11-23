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

        with open("dataByPCA.csv", encoding='utf8') as f:
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
            delta /= K
            print("第{}次循环的delta为{}".format(cnt, delta))
            print(cluster)
            if delta == 0 or cnt >= 100:
                total_dist = 0
                for m in range(K):
                    for idx in cluster[m]:
                        total_dist += self.calculate_distance(self.specimen[idx], mean_vector[m])
                final_dist.append(total_dist)

                return cluster
            else:
                mean_vector = temp
            cnt += 1


if __name__ == '__main__':
    test = clustering()
    test.data_ready()
    # K = 10
    # gap = [0 for _ in range(10)]
    # for j in range(100):
    #     final_dist = []
    #     for i in range(K):
    #         test.clustering(i + 1)
    #         print("K={}已完成".format(i + 1))
    #
    #     for i in range(K):
    #         gap[i] += np.log(final_dist[i])
    # for m in range(K):
    #     gap[m] /= 100
    #
    # final_dist = []
    # for i in range(K):
    #     test.clustering(i + 1)
    # for i in range(K):
    #     gap[i] -= np.log(final_dist[i])
    # print(gap)
    # print("Max index is {}".format(gap.index(max(gap))))

    # K = gap.index(max(gap)) + 1
    K = 3
    feature = []
    for i in range(K):
        feature.append([])
    for i in range(K):
        for j in range(3):
            feature[i].append([])
    feature = [[[] for i in range(3)] for _ in range(K)]

    final_dist = []
    res = test.clustering(K)
    print(res)
    category = {}
    for i in range(len(res)):
        for item in res[i]:
            category[item] = i
    color_map = ['red', 'blue', 'green', 'yellow', 'pink', 'purple']

    with open('dataByPCA.csv', encoding='utf8') as f:
        reader = csv.reader(f)
        header = next(reader)
        i = 0

        for row in reader:
            feature[category[i]][0].append(float(row[1]))
            feature[category[i]][1].append(float(row[2]))
            feature[category[i]][2].append(float(row[3]))
            i += 1
    fig = plt.figure()
    ax1 = plt.axes(projection='3d')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    for i in range(K):
        ax1.scatter3D(feature[i][0], feature[i][1], feature[i][2], c=color_map[i])
    plt.title("西北大学外卖店家信息聚类结果")
    ax1.set_xlabel("经PCA处理后的特征一")
    ax1.set_ylabel("经PCA处理后的特征二")
    ax1.set_zlabel("经PCA处理后的特征三")
    plt.savefig("PCA处理后聚类的情况")
    plt.show()
