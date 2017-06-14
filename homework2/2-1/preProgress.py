# -*- coding: utf-8 -*-

import csv
import matplotlib.pyplot as plt

def csv2dict(in_file, key, value):
    new_dict = {}
    with open(in_file, 'rb') as fin:
        reader = csv.reader(fin, delimiter=',')
        fieldnames = next(reader)
        reader = csv.DictReader(fin, fieldnames=fieldnames, delimiter=',')
        for row in reader:
            if(value == '通信时长'):
                new_dict[row[key]] = new_dict.get(row[key],0) + int(row[value])
            elif(value == '通信次数'):
                new_dict[row[key]] = new_dict.get(row[key],0) + 1
            elif(value == '亲密分析'):
                if(int(row['亲密性']) == 1):
                    new_dict[row[key]] = new_dict.get(row[key],0) + int(row['通信时长'])
            else:
                new_dict[row[key]] = row[value]
    return new_dict


def getAverage(nums):
    length = len(nums)
    sum = 0;
    for i in nums:
        sum += i
    return sum/length

def getPercentageValue(nums,per):
    length = len(nums)
    if per == 0.5 and length%2 != 0:
        return (nums[length/2-1]+nums[length/2])/2
    else:
        return nums[int(per*length)-1]


if __name__ == "__main__":
    print ('Start preProgressing the data')

    #在表格中读取到’对方号码’-‘通信时长’的字典，即计算出每个号码的通信总时长
    sumCallTimeDict = csv2dict('myCallsData.csv','对方号码','通信时长')
    #对通信时长进行升序排序，并填充到数组中
    sumCallTime = [];
    sumCallTimeDict = sorted(sumCallTimeDict.items(),lambda x, y: cmp(x[1], y[1]))
    for phoneNum,callTime in sumCallTimeDict:
        sumCallTime.append(callTime)

    #获取‘对方号码’-‘通信次数’的字典
    sumCallCountDict = csv2dict('myCallsData.csv','对方号码','通信次数')
    #对通信次数进行降序排序
    sumCallCountDict = sorted(sumCallCountDict.items(),lambda x, y: cmp(x[1], y[1]),reverse = True)

    #求得各个统计数据
    time_average = getAverage(sumCallTime)
    time_middle = getPercentageValue(sumCallTime,0.5)
    time_min = sumCallTime[0]
    time_max = sumCallTime[len(sumCallTime)-1]
    time_q1 = getPercentageValue(sumCallTime,0.25)
    time_q3 = getPercentageValue(sumCallTime,0.75)

    call_mode_phone = sumCallCountDict[0][0]
    call_mode = sumCallCountDict[0][1]

    #输出计算得到的各个统计值
    print "总通信时长均值： "+str(time_average)
    print "总通信时长中位数： "+str(time_middle)
    print "总通信时长五数概括： "+" min："+str(time_min)+"；  q1："+str(time_q1)+"；  middle："+str(time_middle)+"；  q3："+str(time_q3)+"；  max："+str(time_max)
    print "总通信次数众数： "+str(call_mode)+",  通信方为："+str(call_mode_phone)

    #获取标记为“亲密关系”的人的通信时长数据
    sumCloseCallTimeDict = csv2dict('myCallsData.csv','对方号码','亲密分析')
    sumCloseCallTime = [];
    sumCloseCallTimeDict = sorted(sumCloseCallTimeDict.items(),lambda x, y: cmp(x[1], y[1]))
    for phoneNum,callTime in sumCloseCallTimeDict:
        sumCloseCallTime.append(callTime)

    #绘制盒图
    pltData=[sumCallTime,sumCloseCallTime]

    fig = plt.figure(figsize=(6,8))

    plt.boxplot(pltData,
                notch=False,  # box instead of notch shape
                sym='bx',     # red squares for outliers
                vert=True)   # horizontal box aligmnent

    plt.xticks([y+1 for y in range(len(pltData))], ['all_object', 'close_object'])
    plt.ylabel('sumCallTime')
    plt.xlabel('callObject')
    t = plt.title('My SumPhoneCallTime Box plot')
    plt.show()
