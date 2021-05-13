import os
from datetime import date
from calendar import monthrange
import PySimpleGUI as sg
class Gui:

    def __init__(self):
        self.run()

    def format(self,foo):
        toReturn = foo.strftime('%B'),foo.strftime('%Y')
        toReturn = ' '.join(toReturn)
        return toReturn

    def getDates(self):
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        days = []
        toReturn = []
        today_date = date.today()
        latestMonth = today_date.strftime('%B')
        latestMonth_Index = months.index(latestMonth)+1
        tempMonthIndex = latestMonth_Index
        year = today_date.year
        lastYear = []
        for i in range(0,12):
            if tempMonthIndex+i == 13: break
            lastYear.append(date(year-1,tempMonthIndex+i,1))
            days.append(monthrange(year-1, tempMonthIndex+i)[1])
        tempMonthIndex = latestMonth_Index-1
        thisYear = []
        for f in range(0,latestMonth_Index):
            thisYear.append(date(year,tempMonthIndex-f+1,1))
            days.append(monthrange(year, tempMonthIndex-f+1)[1])
        thisYear.reverse()
        toReturn = lastYear + thisYear
        return toReturn

    def update(self,key,text):
        self.window[key].update(text)

    def data(self):
        return self.window.read()

    def run(self):
        self.Intervals = [1, 5, 15, 30, 60, 'Day', 'Week', 'Month']
        self.Months = []
        for month in self.getDates():
            self.Months.append(self.format(month))
        self.layout = [
                 [sg.Text('Stock Ticker',size=(15,1)),sg.Input("Ticker",key='Ticker',size=(10,1))],
                 [sg.Text('Twitter Handle',size=(15,1)),sg.Input("Handle",key='Handle',size=(10,1))],
                 [sg.Text('Data Interval',size=(15,1)),sg.Combo(self.Intervals,default_value = self.Intervals[3],key='Interval')],
                 [sg.Text('Start Month',size=(15,1)),sg.Combo(self.Months,default_value = self.Months[0],key='StartMonth')],
                 [sg.Text('End Month',size=(15,1)),sg.Combo(self.Months,default_value = self.Months[len(self.Months)-1],key='EndMonth')],
                 [sg.Text('SD:',size=(5,1)),sg.Text(size=(10,1),key='SD')],
                 [sg.Text('SMVI:',size=(5,1)),sg.Text(size=(10,1),key='SMVI')],
                 [sg.Button('Run'),sg.Text('Please enter in your information',size=(28,1),key='Terminal')],
                 [sg.Button("Exit")]
                 ]
        sg.theme('Reddit')
        self.window = sg.Window("The Price of Free Speech",self.layout)