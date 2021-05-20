import os
from datetime import date
from calendar import monthrange
import PySimpleGUI as sg
from Stock import Stock
from Gui import Gui
import csv
from WarningWindow import WarningWindow
from AutoComplete import predictor


warning = WarningWindow()
gui = Gui()
complete = predictor()
prevTicker = ''
while True:
    event,values = gui.data()
    if not values['Ticker'] == prevTicker:
        gui.updateTickers()
        prevTicker = values['Ticker']
    if event == sg.WIN_CLOSED or event == 'Exit': exit()
    elif event == 'Run':
        toEnter = [ values['Ticker'],
                    values['Interval'],
                    values['StartMonth'],
                    values['EndMonth'],
                  ]
        gui.update('SD',"Calculating...")
        gui.update('SMVI',"Calculating...")
        gui.update('Terminal','Calculating...')
        allSlices = gui.Months
        if values['Handle'] == '' or values['Handle'] == 'Handle':
            sg.popup('Error, please enter a valid Twitter handle')
            continue
        stock = Stock(toEnter[0],toEnter[1],toEnter[2],toEnter[3],allSlices,False)
        if stock.hasErrors:
            gui.update('Terminal','An error occured')
        else:
            SDToDisplay = str(stock.SDToDisplay)[0:8]
            gui.update('SD',SDToDisplay)
            print('Calculating baseline...')
            gui.update('Terminal','Calculating baseline...')
            DIA = Stock('DIA',toEnter[1],toEnter[2],toEnter[3],allSlices,True)
            gui.update('Terminal','Calculating SVMI')
