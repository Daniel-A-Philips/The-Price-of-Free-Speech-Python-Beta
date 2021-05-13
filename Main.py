import os
from datetime import date
from calendar import monthrange
import PySimpleGUI as sg
from Stock import Stock

def format(foo):
    toReturn = month.strftime('%B'),month.strftime('%Y')
    toReturn = ' '.join(toReturn)
    return toReturn

def getDates():
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    days = []
    toReturn = []
    today_date = date.today()
    latestMonth = today_date.strftime('%B')
    latestMonth_Index = months.index(latestMonth)+1
    tempMonthIndex = latestMonth_Index-1
    year = today_date.year
    for i in range(0,12):
        if tempMonthIndex-i == 0: tempMonthIndex = 12 + i
        toReturn.append(date(year-1,tempMonthIndex-i,1))
        days.append(monthrange(year-1, tempMonthIndex-i)[1])
    tempMonthIndex = latestMonth_Index-1
    for f in range(0,12):
        if tempMonthIndex-f == 0: tempMonthIndex = 12+f
        toReturn.append(date(year,tempMonthIndex-f,1))
        days.append(monthrange(year, tempMonthIndex-f)[1])
    return toReturn

Intervals = [1, 5, 15, 30, 60, 'Day', 'Week', 'Month']
Months = []
for month in getDates():
    Months.append(format(month))
layout = [
         [sg.Text('Stock Ticker',size=(15,1)),sg.Input("Ticker",key='Ticker',size=(10,1))],
         [sg.Text('Twitter Handle',size=(15,1)),sg.Input("Handle",key='Handle',size=(10,1))],
         [sg.Text('Data Interval',size=(15,1)),sg.Combo(Intervals,default_value = Intervals[3],key='Interval')],
         [sg.Text('Start Month',size=(15,1)),sg.Combo(Months,default_value = Months[0],key='StartMonth')],
         [sg.Text('End Month',size=(15,1)),sg.Combo(Months,default_value = Months[len(Months)-1],key='EndMonth')],
         [sg.Text('SD:',size=(5,1)),sg.Text(size=(10,1),key='-SD-')],
         [sg.Text('SMVI:',size=(5,1)),sg.Text(size=(10,1),key='-SMVI-')],
         [sg.Button('Run')],
         [sg.Button("Exit")]
         ]
sg.theme('Reddit')
window = sg.Window("The Price of Free Speech",layout)
while True:
    event,values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        exit()
    elif event == 'Run':
        toEnter = [
                    values['Ticker'],
                    values['Interval'],
                    values['StartMonth'],
                    values['EndMonth'],
                    False
        ]
        window['-SD-'].update("Calculating...")
        window['-SMVI-'].update("Calculating...")
        stock = Stock(toEnter[0],toEnter[1],toEnter[2],toEnter[3],toEnter[4])
        SDToDisplay = str(stock.SDToDisplay)[0:8]
        window['-SD-'].update(SDToDisplay)

