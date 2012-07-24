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
    filename = "JMAMemuro.csv" 
    writecsv = csv.writer(file(filename, 'w'), lineterminator='\n')
    monthcounter = 1
    yearcounter = 1977
    header = ("year","month","day","SunshineDuration","Tmin","Tmax","rainfall","windspeed")
    writecsv.writerow(header)
    for yearcounter in range(1977,2013): 
        for monthcounter in range(1,13):
        #while monthcounter < 13:
            url =  'http://www.data.jma.go.jp/obd/stats/etrn/view/daily_a1.php?prec_no=20&block_no=0115&year='
            year = str(yearcounter)
            month = str(monthcounter)
            # サーバーから気象データのページを取得
            html = urllib2.urlopen(url+year+'&month='+month).read() 
            soup = BeautifulSoup(html)
            trs = soup.find('table', { 'class' : 'data2_s' })

            for tr in trs.findAll('tr')[3:]:
                tds = tr.findAll('td')
                if tds[1].string == None:   # その月がまだ終わってない場合、途中でデータがなくなる
                    break;
            
                day              = str(tds[0].find('a').string)   # 日付
                if tds[1].string == "///":
                    precipitation    = -9999
                else:
                    precipitation    = str2float(tds[1].string)       # 降水量
                if tds[4].string == "///":
                    temperatureavg = -9999
                else:
                    temperatureavg  = str2float(tds[4].string)       # 気温 - 平均
                if tds[5].string == "///":
                    temperaturehigh = -9999
                else:
                    temperaturehigh = str2float(tds[5].string)# 気温 - 最高
                if tds[6].string == "///":
                    temperaturelow = -9999
                else:
                    temperaturelow  = str2float(tds[6].string)      # 気温 - 最低
                if tds[13].string != "///":
                    sunshineduration = -9999
                else:
                    sunshineduration = str2float(tds[13].string)      # 日照時間
                if tds[7].string != "///":
                    windspeed = -9999
                else:
                    windspeed = str2float(tds[7].string)
                row = (year,month,day,sunshineduration,temperaturelow,temperaturehigh,precipitation,windspeed)
                writecsv.writerow(row)