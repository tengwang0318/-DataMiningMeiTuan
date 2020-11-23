import numpy as np
import csv


class PCA:
    def __init__(self):
        self.specimen = np.zeros((125, 7))
        self.names = []
        self.latitude, self.longitude = [], []

    # 读取数据并进行中心化处理
    def data_ready(self):
        with open("meituan.csv", encoding='utf8') as f:
            reader = csv.reader(f)
            header = next(reader)
            i = 0

            for row in reader:
                self.specimen[i] = [row[1], row[2], row[3], row[4], row[5], row[6], row[7]]
                self.names.append(row[0])
                self.latitude.append(row[8])
                self.longitude.append(row[9])

                i += 1
            means = self.specimen.mean(axis=0)
            # maxs, mins = self.specimen.max(axis   =0), self.specimen.min(axis=0)
            for i in range(len(self.specimen)):
                for j in range(len(self.specimen[i])):
                    self.specimen[i][j] = self.specimen[i][j] - means[j]
                    # self.specimen[i][j] = (self.specimen[i][j] - mins[j]) / (maxs[j] - mins[j])
        temp_specimen = np.cov(self.specimen.T)

        eigenValues, eigenVector = np.linalg.eig(temp_specimen)
        temp = 0
        for i in range(3):
            temp += eigenValues[i]
        print("前三项特征值的占比为{}".format(temp / sum(eigenValues)))
        # print(eigenValues)
        # for idx, val in enumerate(eigenValues):
        #     print(idx, val)
        print(eigenVector)
        max_eigenvector = eigenVector[:3].T

        with open('dataByPCA.csv', 'w', encoding='utf8', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "feature1", "feature2", "feature3", "latitude", "longitude"])
            fin_data = self.specimen.dot(max_eigenvector)
            # print(fin_data)
            for i in range(125):
                writer.writerow([self.names[i], fin_data[i][0], fin_data[i][1], fin_data[i][2], self.latitude[i],
                                 self.longitude[i]])


test = PCA()
test.data_ready()
