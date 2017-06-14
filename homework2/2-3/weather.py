# -*- coding: utf-8 -*-
import csv
import copy

in_file = 'data/TrainingData.csv'
#需要处理的属性
saved_attribute = ['Solar.radiation_64','target_1_57','weekday','Sample.Baro.Pressure_52','WindSpeed..Resultant_1']


def _standardized_min_max(data, attri, new_min, new_max):
    print ('the min_max standardize of '+str(attri))
    old_min = float(data[0][attri])
    old_max = old_min

    for element in data:
        if float(element[attri]) < old_min:
            old_min = float(element[attri])
        if float(element[attri]) > old_max:
            old_max = float(element[attri])

    old_sclar = old_max - old_min
    new_sclar = new_max - new_min
    for element in data:
        element[attri] = (float(element[attri]) - old_min)/old_sclar*new_sclar + new_min
    print ('*******')

def _standardized_z_score(data, attri):
    print ('the z_score standardize of '+str(attri))
    theSum = 0.0
    count = 0
    mean = 0.0
    for element in data:
        theSum += float(element[attri])
        count += 1
    mean = theSum/count

    theDevSum = 0.0
    stand_dev = 0.0
    for element in data:
        theDevSum += pow((float(element[attri])-mean),2)
    stand_dev = (theDevSum/count) ** 0.5
    # print stand_dev
    for element in data:
        element[attri] = (float(element[attri])-mean)/stand_dev
    print ('*******')

def _standardized_decimal(data, attri):
    print ('the decimal standardize of '+str(attri))
    theMax = abs(float(data[0][attri]))
    theJ = 0
    for element in data:
        if abs(float(element[attri])) > theMax:
            theMax = abs(float(element[attri]))
    while theMax > 1:
        theMax = theMax/10
        theJ += 1
    # print theJ
    for element in data:
        element[attri] = float(element[attri])/pow(10,theJ)
    print ('*******')

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

    print "chi_squre value is: " + str(chi_square)
    print ('*******')




if __name__ == "__main__":
    print ('Start preProgressing the data')
    print ('---------------------------------------')
    print ('Start reading the data')

    weatherData = []

    with open(in_file, 'rb') as fin:
        reader = csv.reader(fin, delimiter=',')
        fieldnames = next(reader)
        reader = csv.DictReader(fin, fieldnames=fieldnames, delimiter=',')
        tempDict = {}
        for row in reader:
            tempDict = {}
            for attri in saved_attribute:
                tempDict[attri] = row[attri]
            weatherData.append(tempDict)
        print ('Done reading')
    print ('---------------------------------------')
    # print(weatherData)

    # 处理缺失值
    print ('Start handling missing value')
    solarSum = 0.0
    solarCount = 0
    targetSum = 0.0
    targetCount = 0
    pressureSum = 0.0
    pressureCount = 0
    windSpeedSum = 0.0
    windSpeedCount = 0

    for element in weatherData:
        # print element['Solar.radiation_64']
        if element['Solar.radiation_64'] != 'NA':
            solarSum += float(element['Solar.radiation_64'])
            solarCount += 1
        if element['target_1_57'] != 'NA':
            targetSum += float(element['target_1_57'])
            targetCount += 1
        if element['Sample.Baro.Pressure_52'] != 'NA':
            pressureSum += float(element['Sample.Baro.Pressure_52'])
            pressureCount += 1
        if element['WindSpeed..Resultant_1'] != 'NA':
            windSpeedSum += float(element['WindSpeed..Resultant_1'])
            windSpeedCount += 1

    for element in weatherData:
        if element['Solar.radiation_64'] == 'NA':
            element['Solar.radiation_64'] = solarSum/solarCount
        if element['target_1_57'] == 'NA':
            element['target_1_57'] = targetSum/targetCount
        if element['Sample.Baro.Pressure_52'] == 'NA':
            element['Sample.Baro.Pressure_52'] = pressureSum/pressureCount
        if element['WindSpeed..Resultant_1'] == 'NA':
            element['WindSpeed..Resultant_1'] = windSpeedSum/windSpeedCount
    print ('Done handling missing value')
    print ('---------------------------------------')

    # 对“WindSpeed..Resultant_1”属性进行规范化
    print ('Start standardizing')
    print ('the target attribute is WindSpeed..Resultant_1')
    temp1 = copy.deepcopy(weatherData)
    _standardized_min_max(temp1,'WindSpeed..Resultant_1',0.0,2.0)
    temp2 = copy.deepcopy(weatherData)
    _standardized_z_score(temp2,'WindSpeed..Resultant_1')
    temp3 = copy.deepcopy(weatherData)
    _standardized_decimal(temp3,'WindSpeed..Resultant_1')
    print ('Done standardizing')
    print ('---------------------------------------')

    # 相关性分析
    print ('Start analysing correlation')
    _analyse_correlation_coefficient(weatherData,'Solar.radiation_64','target_1_57')
    _analyse_chi_square(weatherData, 'weekday', 'Sample.Baro.Pressure_52')
    print ('Done analysing correlation')
    print ('---------------------------------------')
    print ('finish')
