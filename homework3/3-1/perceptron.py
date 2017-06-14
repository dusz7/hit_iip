# -*- coding: utf-8 -*-
import numpy as np
from array import array

class Perceptron(object):

    # eta:学习率
    # iteration_num:迭代次数
    def __init__(self, eta = 0.1, iteration_num = 20):
        self.eta = eta
        self.iteration_num = iteration_num

    def iteration(self, X, y):
        #wights[0]为bias，随机权值从零开始
        self.wights = np.zeros(1 + X.shape[1])
        self.error_sample_num = []

        for time in range(self.iteration_num):
            errors = 0
            #将X向量、预测值和对应的真实结果进行比较、运算
            for xi, true_y in zip(X, y):
                is_corrent = true_y - self.predict(xi)
                if is_corrent != 0.0:
                    self.wights[1:] += self.eta * true_y * xi
                    self.wights[0] += self.eta * true_y * 1
                errors += int(is_corrent != 0.0)
            self.error_sample_num.append(errors)
        return self

    def net_in_method(self,xi):
        return np.dot(xi, self.wights[1:]) + 1 * self.wights[0]

    def predict(self, xi):
        return np.where(self.net_in_method(xi) >= 0.0, 1, -1)

    def verify(self,X,y):
        errors = 0
        for xi, true_y in zip(X,y):
            is_corrent = true_y - self.predict(xi)
            errors += int(is_corrent != 0.0)
        return errors

    def roc(self,X,y):
        buf = array("d")
        pos_true_num = 0
        neg_true_num = 0
        for xi, true_y in zip(X,y):
            buf.append(true_y)
            buf.append(self.net_in_method(xi))
            if true_y > 0:
                pos_true_num += 1
            else:
                neg_true_num += 1
        # print('in the test data, the postive sample num is %d, the negtive sample num is %d' %(pos_true_num,neg_true_num))
        rocs = np.frombuffer(buf, dtype=[('t',float),('y',float)])
        rocs = np.sort(rocs, order = 'y')
        roc_x = []
        roc_y = []
        roc_x.append(1)
        roc_y.append(1)
        index_now = 0
        pos_true_num_now = 0
        for roc in rocs:
            index_now += 1
            if roc['t'] > 0:
                pos_true_num_now += 1

            pos_predict_neg_true_num = neg_true_num - (index_now - pos_true_num_now)
            pos_predict_pos_true_num = pos_true_num - pos_true_num_now
            roc_x.append(float(pos_predict_neg_true_num)/neg_true_num)
            roc_y.append(float(pos_predict_pos_true_num)/pos_true_num)

        roc_x.append(0)
        roc_y.append(0)

        return [roc_x,roc_y]
