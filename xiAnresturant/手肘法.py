import numpy as np
import csv
from matplotlib import pyplot as plt

# np.random.seed(0)

gap = [0 for _ in range(976)]
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
            next(reader)
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
                total_dist = 0
                for m in range(K):
                    for idx in cluster[m]:
                        total_dist += self.calculate_distance(self.specimen[idx], mean_vector[m])
                final_dist.append(total_dist)
                return
            else:
                mean_vector = temp
            cnt += 1


if __name__ == '__main__':
    test = clustering()
    test.data_ready()
    final_dist = []
    K = 30
    for i in range(1, K + 1):
        test.clustering(i)

    # K = 30
    # for j in range(5):
    #     final_dist = []
    #     for i in range(K):
    #         test.clustering(i + 1)
    #         print("K={}已完成".format(i + 1))
    #
    #     for i in range(K):
    #         gap[i] += np.log(final_dist[i])
    # for m in range(976):
    #     gap[m] /= 5
    #
    #
    # final_dist = []
    # for i in range(K):
    #     test.clustering(i + 1)
    # for i in range(20):
    #     gap[i] -= np.log(final_dist[i])
    # print(gap)
    # print("Max index is {}".format(max(gap)))

    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.title("K从{}到{}时各个点到cluster中心的距离的平方的和".format(1, K))
    plt.xlabel("K")
    plt.ylabel("WSS")
    plt.xticks(list(range(1, K + 1)))
    plt.plot(list(range(1, K + 1)), final_dist, 'o-')
    plt.show()
