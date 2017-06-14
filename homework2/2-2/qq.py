# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

def getPercentageValue(nums,per):
    length = len(nums)
    if per == 0.5 and length%2 != 0:
        return (nums[length/2-1]+nums[length/2])/2
    else:
        return nums[int(per*length)-1]


# A班	19	18	18	15	18	11	16	19	17	17	20	17	19	20	20	15	15	16	--
# B班	19	15	20	20	17	18	18	15	16	18	15	19	20	19	19	16	17	13	15

# 两班成绩的数据集
classAResults = [19,18,18,15,18,11,16,19,17,17,20,17,19,20,20,15,15,16]
classBResults = [19,15,20,20,17,18,18,15,16,18,15,19,20,19,19,16,17,13,15]

# 数据集预处理
classAResults.sort()
classBResults.sort()
# 获得每个成绩出现的频数
classAResultsCount = {}
classBResultsCount = {}
for ra in classAResults:
    classAResultsCount[ra] = classAResultsCount.get(ra,0)+1
for rb in classBResults:
    classBResultsCount[rb] = classBResultsCount.get(rb,0)+1
# 获得最小和最大成绩
minResult = min(min(classAResults),min(classBResults))
maxResult = max(max(classAResults),max(classBResults))
# 计算分位数
classAResultsQuartile = {}
classBResultsQuartile = {}
temp = 0;
for rac in classAResultsCount.keys():
    theCount = classAResultsCount.get(rac)
    temp = temp + theCount
    classAResultsQuartile[rac] = (temp-0.5)/len(classAResults)
temp = 0
for rbc in classBResultsCount.keys():
    theCount = classBResultsCount.get(rbc)
    temp = temp + theCount
    classBResultsQuartile[rbc] = (temp-0.5)/len(classBResults)

# 求得分位数点
classAQ1 = getPercentageValue(classAResults,0.25)
classAMiddle = getPercentageValue(classAResults,0.5)
classAQ3 = getPercentageValue(classAResults,0.75)

classBQ1 = getPercentageValue(classBResults,0.25)
classBMiddle = getPercentageValue(classBResults,0.5)
classBQ3 = getPercentageValue(classBResults,0.75)

# 绘制分位数图
plt.figure(figsize=(10,8))
classaFig = plt.subplot(211)
classaFig.set_xlim([0, 1])
classaFig.set_ylim([minResult-1, maxResult+1])
classbFig = plt.subplot(212)
classbFig.set_xlim([0, 1])
classbFig.set_ylim([minResult-1, maxResult+1])

plt.sca(classaFig)
plt.title('class A')
plt.xlabel('f value')
plt.ylabel('Score')
plt.subplots_adjust(hspace = 0.3)
for x in classAResultsQuartile.keys():
    if x == classAQ1:
        classaFig.plot(classAResultsQuartile[x], x, 'r*')
    elif x == classAMiddle:
        classaFig.plot(classAResultsQuartile[x], x, 'r*')
    elif x == classAQ3:
        classaFig.plot(classAResultsQuartile[x], x, 'r*')
    else:
        classaFig.plot(classAResultsQuartile[x], x, 'co')

plt.sca(classbFig)
plt.title('class B')
plt.xlabel('f value')
plt.ylabel('Score')
for x in classBResultsQuartile.keys():
    if x == classBQ1:
        classbFig.plot(classBResultsQuartile[x], x, 'r*')
    elif x == classBMiddle:
        classbFig.plot(classBResultsQuartile[x], x, 'r*')
    elif x == classBQ3:
        classbFig.plot(classBResultsQuartile[x], x, 'r*')
    else:
        classbFig.plot(classBResultsQuartile[x], x, 'co')


plt.show()
