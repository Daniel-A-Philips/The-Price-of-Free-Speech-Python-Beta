import os
import PySimpleGUI as sg

Intervals = [1, 5, 15, 30, 60, 'Day', 'Week', 'Month']

layout = [
         [sg.Text('Stock Ticker',size=(15,1)),sg.Input("Ticker",key='Ticker',size=(10,1))],
         [sg.Text('Twitter Handle',size=(15,1)),sg.Input("Handle",key='Handle',size=(10,1))],
         [sg.Text('Data Interval',size=(15,1)),sg.Combo(Intervals,default_value = Intervals[3],key='Interval')],
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

