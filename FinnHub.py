import requests
import os
import datetime
import csv
from calendar import monthrange
class FinnHub:


    def run(self):
        self.Dates = self.getDates()
        self.absPath = os.getcwd()
        self.URLConnect()
        self.writeData()

    def __init__(self,start,end,Ticker,Interval,forSMVI):
        self.Dates = []
        self.tempMonth = ['','January','February','March','April','May','June','July','August','September','October','November','December']
        self.key = 'c1vv82l37jkoemkedus0'
        self.start = start
        self.end = end
        self.start_end = [start,end]
        self.Ticker = Ticker.upper()
        self.Interval = Interval
        self.forSMVI = forSMVI
        self.Format = 'csv'
        self.rawData = []
        self.allData = []
        self.run()

    def toUnix(self,months,years):
        unixed = []
        print(years)
        years = [int(i) for i in years]
        months = [self.tempMonth.index(i) for i in months]
        print(months)
        print(years)
        unixed.append(int(datetime.datetime(years[0],months[0],1).timestamp()))
        unixed.append(int(datetime.datetime(years[1],months[1],self.getDaysInMonth(months[1],years[1])).timestamp()))
        return unixed

    def getDaysInMonth(self,month,year):
        return monthrange(year,month)[1]

    def getDates(self):
        months = []
        years = []
        if self.start == self.end: #Runs if one month is selected
            year = self.start[len(self.start)-4:]
            dateHolder = [year]
        else:
            for startend in self.start_end:
                years.append(startend[len(startend)-4:])
                months.append(startend[:len(startend)-5:])
        unixed = self.toUnix(months,years)
        print('unixed: ', unixed)
        return unixed


    def URLConnect(self):
        monthInSeconds = 2629746
        start = self.Dates[0]
        final = self.Dates[1]
        prevStart = start
        end = start + monthInSeconds
        index = 0
        while end < final:
            prevStart = prevStart + monthInSeconds
            end = end + monthInSeconds
            startime = str(prevStart)
            endtime = str(end)
            self.Interval = str(self.Interval)
            print('Connecting to URL')
            print(startime,',',endtime)
            print('Self.Interval:',self.Interval)
            r = requests.get(
                'https://finnhub.io/api/v1/stock/candle?symbol=' + self.Ticker + '&resolution=' + self.Interval + '&from=' + startime + '&to=' + endtime + '&format=' + self.Format + '&token=' + self.key)
            data = str(r.content).split("\\n")
            self.headers = ['time','open','high','low','close','volume']
            data.pop(0)
            print('Data: ',data)
            data.remove("'")
            self.rawData.append(data)

    def writeData(self):
        if self.forSMVI: path = self.absPath + '/Data/DIA_Data.csv'
        else: path = self.absPath + '/Data/Data.csv'
        with open(path,'w',newline='') as file:
            for data in self.rawData:
                for line in data:
                    self.allData.append(line)
                    file.write(line + '\n')