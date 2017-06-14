# -*- coding: utf-8 -*-
import csv
from array import array
import random
import numpy as np
import matplotlib.pyplot as plt
from perceptron import *
from centerClassification import *

training_data_file = 'data/trnOverTraj30K.csv'
testing_data_file = 'data/tstOverTraj10K.csv'


if __name__ == "__main__":

    X = np.array
    y = np.array
    test_X = np.array
    test_y = np.array
    print ('---------------------------------------')
    print ('Start preparing')
    print ('    Start reading the training data')
    with open(training_data_file, 'rb') as fin:
        reader = csv.reader(fin, delimiter=',')
        buf = array("d")
        negs = 0;
        for row in reader:
            if row[22] == '-1':
                negs += 1
            for e in row:
                buf.append(float(e))
        na = np.frombuffer(buf, dtype=np.float).reshape(-1, 23)
        X = na[:,0:22]
        y = na[:,22]
        y = y.astype(int)
        print ('    the neg sample num in the training data is %d' %(negs))
    print ('    Done reading')
    print ('    Start reading the testing data')
    with open(testing_data_file, 'rb') as fin:
        reader = csv.reader(fin, delimiter=',')
        buf = array("d")
        for row in reader:
            for e in row:
                buf.append(float(e))
        na = np.frombuffer(buf, dtype=np.float).reshape(-1, 23)
        test_X = na[:,0:22]
        test_y = na[:,22]
        test_y = test_y.astype(int)
    print ('    Done reading')
    print('')

    # set up model
    print ('---------------------------------------')
    print ('Start setting up model')
    print ('    Perceptron method')
    ppn = Perceptron(0.02, 30)
    ppn.iteration(X,y)
    print ('    Done')
    # plt.plot(range(1,len(ppn.error_sample_num)+1),ppn.error_sample_num,marker='o')
    # plt.show()
    # print (ppn.wights)
    print ('    Center classification method')
    cc = CenterClassification()
    cc.classify(X,y)
    print ('    Done')
    print ('Done')
    print ('')

    # verify model
    print ('---------------------------------------')
    print ('Start verifying the models')
    perceptron_errors = ppn.verify(test_X, test_y)
    perceptron_correct_rate = 1 - (float(perceptron_errors)/len(test_y))
    print ('     the perceptron method correct rate is %f' %(perceptron_correct_rate))
    centerClassification_errors = cc.verify(test_X,test_y)
    centerClassificationn_correct_rate = 1 - (float(centerClassification_errors)/len(test_y))
    print ('     the centerClassification method correct rate is %f' %(centerClassificationn_correct_rate))
    print ('Done')
    print ('')

    # unbanlance learning
    print ('---------------------------------------')
    print ('Start setting up model with banlance training data')
    new_X = np.array
    new_y = np.array
    with open(training_data_file, 'rb') as fin:
        reader = csv.reader(fin, delimiter=',')
        buf = array("d")
        negs = 0;
        chosen = 0;
        for row in reader:
            if row[22] == '-1':
                negs += 1
                if random.randint(1,4) != 2:
                    continue
                chosen += 1
            for e in row:
                buf.append(float(e))
        na = np.frombuffer(buf, dtype=np.float).reshape(-1, 23)
        new_X = na[:,0:22]
        new_y = na[:,22]
        new_y = new_y.astype(int)
        print ('    the neg sample num is %d' %(chosen))
    ppn_new = Perceptron(0.02, 30)
    ppn_new.iteration(new_X,new_y)
    cc_new = CenterClassification()
    cc_new.classify(new_X,new_y)
    perceptron_errors_new = ppn_new.verify(test_X, test_y)
    perceptron_correct_rate_new = 1 - (float(perceptron_errors_new)/len(test_y))
    print ('     the perceptron method correct rate is %f' %(perceptron_correct_rate_new))
    centerClassification_errors_new = cc_new.verify(test_X,test_y)
    centerClassificationn_correct_rate_new = 1 - (float(centerClassification_errors_new)/len(test_y))
    print ('     the centerClassification method correct rate is %f' %(centerClassificationn_correct_rate_new))


    # draw roc curve
    print ('---------------------------------------')
    print ('Start drawing roc curve')
    perceptron_roc_points = ppn.roc(test_X,test_y)
    centerClassification_roc_points = cc.roc(test_X,test_y)
    perceptron_roc_points_new = ppn_new.roc(test_X,test_y)
    centerClassification_roc_points_new = cc_new.roc(test_X,test_y)
    
    plt.figure(1)
    plt.plot([0,1], [0,1], 'r-.')
    plt.plot(perceptron_roc_points[0],perceptron_roc_points[1],'b',label = 'perceptron')
    plt.plot(centerClassification_roc_points[0],centerClassification_roc_points[1],'g',label = 'centerClassification')
    plt.legend(loc=4)
    plt.xlabel('False positive rate')
    plt.ylabel('True positive rate')
    plt.title('roc curve')

    plt.figure(2)
    plt.plot([0,1], [0,1], 'r-.')
    plt.plot(perceptron_roc_points_new[0],perceptron_roc_points_new[1],'y',label = 'perceptron_balance')
    plt.plot(centerClassification_roc_points_new[0],centerClassification_roc_points_new[1],'c',label = 'centerClassification_balance')
    plt.legend(loc=4)
    plt.xlabel('False positive rate')
    plt.ylabel('True positive rate')
    plt.title('roc curve with balance data')

    plt.show()
