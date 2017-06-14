# -*- coding: utf-8 -*-
#
import csv

in_file = 'data/myCallsData.csv'

def csv2dict(in_file, key, value):
    new_dict = {}
    with open(in_file, 'rb') as fin:
        reader = csv.reader(fin, delimiter=',')
        fieldnames = next(reader)
        reader = csv.DictReader(fin, fieldnames=fieldnames, delimiter=',')
        tempDict = {}
        for row in reader:
            if(value == '通信时长'):
                new_dict[row[key]] = new_dict.get(row[key],0) + int(row[value])
            elif(value == '亲密分析'):
                new_dict[row[key]] = int(row['亲密性'])
            else:
                new_dict[row[key]] = row[value]
    return new_dict

def _analyse_correlation_coefficient(data, attri_1, attri_2):
    print ('the correlation_coefficient analyse of '+str(attri_1)+" & "+str(attri_2))
    sum_1 = 0.0
    sum_2 = 0.0
    mean_1 = 0.0
    mean_2 = 0.0
    count = 0
    acc = 0.0
    for element in data:
        sum_1 += float(element[attri_1])
        sum_2 += float(element[attri_2])
        count += 1
        acc += float(element[attri_1])*float(element[attri_2])
    mean_1 = sum_1/count
    mean_2 = sum_2/count

    dev_sum_1 = 0.0
    dev_sum_2 = 0.0
    stand_dev_1 = 0.0
    stand_dev_2 = 0.0
    for element in data:
        dev_sum_1 += pow((float(element[attri_1])-mean_1),2)
        dev_sum_2 += pow((float(element[attri_2])-mean_2),2)
    stand_dev_1 = (dev_sum_1/count) ** 0.5
    stand_dev_2 = (dev_sum_2/count) ** 0.5

    coe = (acc - count * mean_1 * mean_2)/((count-1)*stand_dev_1*stand_dev_2)
    print "correlation coefficient is: "+str(coe)
    print ('*******')

def _analyse_chi_square(data, attri_1, attri_2):
    print ('the chi_square analyse of '+str(attri_1)+" & "+str(attri_2))
    cate_sum_1 = {}
    cate_sum_2 = {}
    sample_real = {}
    count = 0
    for element in data:
        cate_sum_1[element[attri_1]] = cate_sum_1.get(element[attri_1],0) + 1
        cate_sum_2[element[attri_2]] = cate_sum_2.get(element[attri_2],0) + 1
        sample_real[str(element[attri_1])+'&'+str(element[attri_2])] = sample_real.get(str(element[attri_1])+'&'+str(element[attri_2]),0) + 1
        count += 1

    sample_predict = {}
    chi_square = 0.0

    for cate1 in cate_sum_1.keys():
        for cate2 in cate_sum_2.keys():
            sample_predict[str(cate1)+'&'+str(cate2)] = float(cate_sum_1.get(cate1)*cate_sum_2.get(cate2))/count
            sample_real[str(cate1)+'&'+str(cate2)] = sample_real.get(str(cate1)+'&'+str(cate2),0)
            chi_square += pow(sample_real[str(cate1)+'&'+str(cate2)]-sample_predict[str(cate1)+'&'+str(cate2)],2)/sample_predict[str(cate1)+'&'+str(cate2)]
    # print sample_real
    # print sample_predict
    print "chi_squre value is: " + str(chi_square)
    print ('*******')


if __name__ == "__main__":
    print ('Start preProgressing the data')
    print ('---------------------------------------')
    print ('Start reading the data')

    callData = []

    sumCallTimeDict = csv2dict(in_file,'对方号码','通信时长')
    sumCloseCallTimeDict = csv2dict(in_file,'对方号码','亲密分析')

    temp_dict = {}
    for pnum in sumCallTimeDict.keys():
        temp_dict = {}
        temp_dict['对方号码'] = pnum
        temp_dict['总通信时长'] = str(sumCallTimeDict[pnum])
        temp_dict['亲密性'] = str(sumCloseCallTimeDict[pnum])
        callData.append(temp_dict)

    print ('Done reading')
    print ('---------------------------------------')



    # 相关性分析
    print ('Start analysing correlation')
    _analyse_correlation_coefficient(callData,'总通信时长','亲密性')
    _analyse_chi_square(callData,'总通信时长','亲密性')
    print ('Done analysing correlation')
    print ('---------------------------------------')
    print ('finish')
