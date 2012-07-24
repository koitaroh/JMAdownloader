#!/usr/bin/env python
# coding: UTF-8
#
# @see http://www.crummy.com/software/BeautifulSoup/documentation.html
#
import os
import urllib2
import csv
from bs4 import BeautifulSoup
 
def str2float(str):
    try:
        return float(str)
    except:
        return 0.0
dic = {}

if __name__ == "__main__":
    filename = "JMAObihiro.csv" 
    writecsv = csv.writer(file(filename, 'w'), lineterminator='\n')
    monthcounter = 1
    yearcounter = 1961
    header = ("year","month","day","SunshineDuration","Tmin","Tmax","rainfall","windspeed")
    writecsv.writerow(header)
    for yearcounter in range(1961,2013): 
        for monthcounter in range(1,13):
        #while monthcounter < 13:
            url =  'http://www.data.jma.go.jp/obd/stats/etrn/view/daily_s1.php?prec_no=20&block_no=47417&year='
            year = str(yearcounter)
            month = str(monthcounter)
            # サーバーから気象データのページを取得
            html = urllib2.urlopen(url+year+'&month='+month).read() 
            soup = BeautifulSoup(html)
            trs = soup.find('table', { 'class' : 'data2_s' })

            for tr in trs.findAll('tr')[4:]:
                tds = tr.findAll('td')
                if tds[1].string == None:   # その月がまだ終わってない場合、途中でデータがなくなる
                    break;
                
                day              = str(tds[0].find('a').string)   # 日付
                if tds[3].string != "×" or None or "///" or "#":
                    precipitation    = str2float(tds[3].string)
                else:
                    precipitation    = -9999       # 降水量
                if tds[6].string != "×" or None or "///" or "#":
                    temperatureavg = str2float(tds[6].string)
                else:
                    temperatureavg  = -9999       # 気温 - 平均
                if tds[7].string != "×" or None or "///" or "#":
                    temperaturehigh = str2float(tds[7].string)
                else:
                    temperaturehigh = -9999# 気温 - 最高
                if tds[8].string != "×" or None or "///" or "#":
                    temperaturelow = str2float(tds[8].string) 
                else:
                    temperaturelow  = -9999      # 気温 - 最低
                if tds[16].string != "×" or None or "///" or "#":
                    sunshineduration = str2float(tds[16].string)
                else:
                    sunshineduration = -9999      # 日照時間
                if tds[11].string != "×" or None or "///" or "#":
                    windspeed = str2float(tds[11].string)
                else:
                    windspeed = -9999
                #dic['day']              = str(tds[0].find('a').string)   # 日付
                #dic['precipitation']    = str2float(tds[1].string)       # 降水量
                #dic['temperature.avg']  = str2float(tds[4].string)       # 気温 - 平均
                #dic['temperature.high'] = str2float(tds[5].string)       # 気温 - 最高
                #dic['temperature.low']  = str2float(tds[6].string)       # 気温 - 最低
                #dic['sunshine duration']= str2float(tds[13].string)      # 日照時間
 
                #list.append(dic)
                row = (year,month,day,sunshineduration,temperaturelow,temperaturehigh,precipitation,windspeed)
                writecsv.writerow(row)
    # 最後に結果を表示する
        #for dic in list:
            #print dic
            #monthcounter += 1
        #yearcounter += 1
