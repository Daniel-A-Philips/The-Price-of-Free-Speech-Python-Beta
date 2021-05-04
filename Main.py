import os
from datetime import date
from calendar import monthrange
import PySimpleGUI as sg

def getDates():
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    days = []
    toReturn = []
    today_date = date.today()
    year = today_date.year
    for i in range(1,13):
        toReturn.append(date(year-1,i,1))
        days.append(monthrange(year-1, i)[1])
    for f in range(1,13):
        toReturn.append(date(year,f,1))
        days.append(monthrange(year, f)[1])
    return toReturn

Intervals = [1, 5, 15, 30, 60, 'Day', 'Week', 'Month']
Months = getDates()
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
    print(values)
    if event == sg.WIN_CLOSED or event == "Exit":
        exit()
    else:
        window['-SD-'].update("SD test")
        window['-SMVI-'].update("SMVI test")
        getDates()

