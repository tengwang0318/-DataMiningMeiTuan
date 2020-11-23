import numpy as np
import matplotlib.pyplot as plt
import csv


def sigmoid(x):
    return 1 / (1 + np.exp(x))


def sigmoid_d(x):
    return (1 / (1 + np.exp(x))) * (1 - 1 / (1 + np.exp(x)))


def tanh_d(x):
    return 1 - np.tanh(x) ** 2


def softMax(x):
    res = np.zeros((len(x), len(x[0])))
    for i in range(len(x)):
        res[i] = np.exp(x[i]) / np.sum(np.exp(x[i]))
    return res


class Neural:
    def __init__(self, learn_rate=0.01):
        self.X = np.zeros((86, 7))
        self.Y = np.zeros((86, 4))
        self.learn_rate = learn_rate
        with open("final_data.csv", encoding='utf8') as f:
            reader = csv.reader(f)
            next(reader)
            i = 0
            for row in reader:
                self.X[i] = [int(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6]),
                             float(row[7])]
                self.Y[i][int(row[8]) - 1] = 1

                i += 1

        X_max, Y_max = self.X.max(axis=0), self.Y.max(axis=0)
        X_min, Y_min = self.X.min(axis=0), self.Y.min(axis=0)

        for i in range(len(self.X)):
            self.X[i] = (X_max - self.X[i]) / (X_max - X_min)

    def layer_size(self, n_h_input):
        n_x = self.X.shape[1]
        n_h = n_h_input
        n_y = self.Y.shape[1]
        return n_x, n_h, n_y

    def initialize_parameters(self, n_x, n_h, n_y):
        w1 = np.random.rand(n_x, n_h)
        b1 = np.random.rand(1, n_h)
        w2 = np.random.rand(n_h, n_y)
        b2 = np.random.rand(1, n_y)
        parameters = {"w1": w1,
                      "b1": b1,
                      "w2": w2,
                      "b2": b2}
        return parameters

    def forward_propagation(self, parameters):
        w1 = parameters['w1']
        b1 = parameters['b1']
        w2 = parameters['w2']
        b2 = parameters['b2']
        Z1 = self.X.dot(w1) + b1
        # A1 = sigmoid(Z1)
        A1 = np.tanh(Z1)
        Z2 = A1.dot(w2) + b2
        A2 = softMax(Z2)

        cache = {"Z1": Z1,
                 "A1": A1,
                 "Z2": Z2,
                 "A2": A2}
        return A2, cache

    def compute_cost(self, cache, parameters):
        A2 = cache['A2']
        cost = 0
        for i in range(len(self.Y)):
            for j in range(len(self.Y[0])):
                cost += -np.log(A2[i][j]) * self.Y[i][j]
        return cost

    def backward_propagation(self, parameters, cache):
        m = self.X.shape[0]
        w1 = parameters['w1']
        w2 = parameters['w2']
        A1 = cache['A1']
        A2 = cache['A2']
        Z1 = cache['Z1']
        dz2 = A2 - self.Y
        dw2 = 1 / m * (np.dot(A1.T, dz2))
        db2 = 1 / m * (np.sum(dz2, axis=0, keepdims=True))

        # temp = np.multiply(sigmoid(w1), np.ones(w1.shape) - sigmoid(w1))
        dz1 = np.multiply(dz2.dot(w2.T), tanh_d(Z1))
        dw1 = (1 / m) * np.dot(self.X.T, dz1)
        db1 = (1 / m) * np.sum(dz1, axis=0, keepdims=True)

        grads = {
            'dz1': dz1,
            'dw1': dw1,
            'db1': db1,
            'dz2': dz2,
            'dw2': dw2,
            'db2': db2,
        }
        return grads

    def update_parameters(self, parameters, grads):
        w1 = parameters['w1']
        w2 = parameters['w2']
        b1 = parameters['b1']
        b2 = parameters['b2']
        dw1 = grads['dw1']
        dw2 = grads['dw2']
        db1 = grads['db1']
        db2 = grads['db2']

        w1 -= self.learn_rate * dw1
        b1 -= self.learn_rate * db1
        w2 -= self.learn_rate * dw2
        b2 -= self.learn_rate * db2
        parameters = {'w1': w1, 'b1': b1, 'w2': w2, 'b2': b2}
        return parameters

    def nn_model(self, n_h_input, num_iterations=10000, print_cost=True):
        n_x, n_h, n_y = self.layer_size(n_h_input)
        parameters = self.initialize_parameters(n_x, n_h, n_y)
        for i in range(num_iterations):
            # 前向传播
            a2, cache = self.forward_propagation(parameters)
            cost = self.compute_cost(cache, parameters)
            grads = self.backward_propagation(parameters, cache)
            parameters = self.update_parameters(parameters, grads)
            if print_cost and i % 1000 == 0:
                print('迭代第%i次，代价函数为：%f' % (i, cost))
            # print(cost)
        w1 = parameters['w1']
        w2 = parameters['w2']
        b1 = parameters['b1']
        b2 = parameters['b2']
        right_cnt = 0
        Z1 = self.X.dot(w1) + b1
        A1 = sigmoid(Z1)
        Z2 = np.dot(A1, w2) + b2
        A2 = softMax(Z2)
        res = np.zeros((len(self.Y), len(self.Y[0])))
        for j in range(len(A2)):
            max_idx = np.argmax(A2[j])
            res[j][max_idx] = 1
        print(res)
        temp = res - self.Y
        # print(temp)
        for j in range(len(self.Y)):
            if np.max(temp[j]) == 0:
                right_cnt += 1

        print("正确率为", right_cnt / len(self.Y))


test = Neural()
test.nn_model(100)
