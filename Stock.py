from getAllTickers import getAllTickers
from FinnHub import FinnHub
import PySimpleGUI as sg
import datetime
import math
import csv
import os

class Stock:
    def __init__(self,Ticker,Interval,StartSlice,EndSlice,AllSlices,forSMVI):
        self.Ticker = Ticker.upper()
        self.Interval = Interval
        self.StartSlice = StartSlice
        self.EndSlice = EndSlice
        self.AllSlices = AllSlices
        self.forSMVI = forSMVI
        self.AllIntervals = [1, 5, 15, 30, 60, 'Day', 'Week', 'Month']
        self.getTickers()
        self.errorHandling()
        if not self.hasErrors: self.run()

    def getTickers(self):
        self.allTickers = []
        with open(os.getcwd() + '/Data/tickers.csv') as file:
            reader = csv.reader(file)
            for line in reader:
                if not line[0] == 'Symbol': self.allTickers.append(line[0])

    def popup(self,text):
        sg.Popup(text)
        self.hasErrors = True

    def errorHandling(self):
        self.hasErrors = False
        if self.Ticker == 'Ticker':
            self.popup('Error, the asset ticker that has been given has an error')
        elif not self.Interval in self.AllIntervals:
            self.popup('Error, the interval that has been given is incorrect')
        elif not self.StartSlice in self.AllSlices:
            self.popup('Error, the starting time that has been given is incorrect')
        elif not self.EndSlice in self.AllSlices:
            self.popup('Error, the ending time that has been given is incorrect')
        elif self.AllSlices.index(self.EndSlice) < self.AllSlices.index(self.StartSlice):
            self.popup('Error, the ending time is before the starting time')
        elif not self.forSMVI and not self.Ticker in self.allTickers:
            self.getTickers()
            if not self.Ticker in self.allTickers:
                self.popup('Error, the given ticker is invalid')

    def toDate(self,foo,noTime):
        if noTime: return datetime.datetime.fromtimestamp(foo).strftime('%Y-%m-%d')
        return datetime.datetime.fromtimestamp(foo).strftime('%Y-%m-%d %H:%M:%S')

    #Fee fi fo fum, parseToArray to get things done
    def parseToArray(self,fee):
    	fi = []
    	for fo in fee:
    		fi.append(fo.split(','))
    	return fi

    def getAverage(self,foo):
        Open = float(foo[1])
        Close = float(foo[4])
        High = float(foo[2])
        Low = float(foo[3])
        return (Open + Close + High + Low)/4

    def addArrays(self):
        self.headers = self.finnHub.headers
        self.Times = self.Open = self.High = self.Low = self.Close = self.Volume = []
        for line in self.parseToArray(self.finnHub.allData):
            self.Times.append(float(line[0]))
            self.Open.append(float(line[1]))
            self.High.append(float(line[2]))
            self.Low.append(float(line[3]))
            self.Close.append(float(line[4]))
            self.Volume.append(float(line[4]))
        self.allData = {
                        'Times'  :   self.Times,
                        'Open'   :   self.Open,
                        'High'   :   self.High,
                        'Low'    :   self.Low,
                        'Close'  :   self.Close,
                        'Volume' :   self.Volume
                        }
        print('Self.Times:',self.Times)

    # data : a 2D array where each entry is an array, which follows the following format
    # [Times,Open,High,Low,Close,Volume]
    def standardDeviation(self,data):
        N = len(data)
        if N == 0:
            self.popup('Unknown Error, please contact daniel_philips@asl.org')
        tempMu = 0
        Points = []
        for time in data: 
            tempMu += self.getAverage(time)
            Points.append(self.getAverage(time))
        Mu = tempMu/N
        top = 0
        for xi in Points:
            top += (xi - Mu)**2
        sigma = math.sqrt( top / N )
        print('SD:',sigma)
        return sigma
        
    def run(self):
        self.finnHub = FinnHub(self.StartSlice,self.EndSlice,self.Ticker,self.Interval,self.forSMVI)
        self.addArrays()
        self.SDToDisplay = self.standardDeviation(self.finnHub.allData)