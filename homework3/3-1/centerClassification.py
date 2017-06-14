# -*- coding: utf-8 -*-

import numpy as np
from array import array

class CenterClassification(object):


    def classify(self,X,y):
        neg_sample_buf = array('d')
        pos_sample_buf = array('d')
        for xi,true_y in zip(X,y):
            if true_y < 0:
                for fea in xi:
                    neg_sample_buf.append(fea)
            else:
                for fea in xi:
                    pos_sample_buf.append(fea)
        neg_sample_X = np.frombuffer(neg_sample_buf, dtype=np.float).reshape(-1, 22)
        pos_sample_X = np.frombuffer(pos_sample_buf, dtype=np.float).reshape(-1, 22)
        self.neg_class_center = np.mean(neg_sample_X, axis = 0)
        self.pos_class_center = np.mean(pos_sample_X, axis = 0)

    def net_in_method(self,xi):
        neg_class_distance = np.var(np.row_stack((self.neg_class_center,xi)))
        pos_class_distance = np.var(np.row_stack((self.pos_class_center,xi)))
        return (neg_class_distance - pos_class_distance)

    def predict(self,xi):
        if self.net_in_method(xi) > 0:
            return 1
        else:
            return -1

    def verify(self,X,y):
        errors = 0
        for xi,true_y in zip(X,y):
            predict_y = self.predict(xi)
            errors += int(true_y != predict_y)
        return errors

    def roc(self,X,y):
        buf = array("d")
        pos_true_num = 0
        neg_true_num = 0
        for xi, true_y in zip(X,y):
            buf.append(true_y)
            #将（到负类中心的距离减去到正类中心的距离）作为阈值
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
