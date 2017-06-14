# -*- coding: utf-8 -*-

import csv

def format_time(s,d):
    with open(s,'rd') as fin:
        with open(d,'wd') as fout:

            title = fin.readline()
            fout.write(title)

            lines = fin

            for line in lines:
                line = line.split(',')
                t = line[1]

                minute_str = t.split('分')
                if len(minute_str) == 1:
                    minute = 0
                else:
                    minute = int(minute_str.pop(0))
                second_str = minute_str[0].rstrip('秒')
                second = int(second_str)
                line[1] = str(minute*60+second)

                line = ','.join(line)
                fout.write(line)

if __name__ == "__main__":
    print ('Start countint the time')
    format_time('myCalls.csv','myCallsData.csv')
