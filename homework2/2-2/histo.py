# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt


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

# 绘制直方图
maxPeople = 7
bins = np.arange(0,20)
plt.xticks(bins)
plt.xlim(minResult-1,maxResult+1)
plt.ylim(0,maxPeople)

global rap,rbp

for rac in classAResultsCount.keys():
    rap = plt.axvspan(rac - 0.5, rac + 0.5, ymin = 0, ymax = 1.0*classAResultsCount[rac]/maxPeople, fc = 'yellow', ec = 'black', alpha = 0.3, label='classA')

for rbc in classBResultsCount.keys():
    rbp = plt.axvspan(rbc - 0.5, rbc + 0.5, ymin = 0, ymax = 1.0*classBResultsCount[rbc]/maxPeople, fc = 'blue', ec = 'black', alpha = 0.3, label='classB')

plt.legend(handles=[rap,rbp], loc = 'upper right')
plt.title('Math-Midterm-Results')
plt.xlabel('Score')
plt.ylabel('Number of Students')

plt.show()
