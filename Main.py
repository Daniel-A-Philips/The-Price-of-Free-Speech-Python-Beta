import time

from Gui import Gui
from Stock import Stock
import PySimpleGUI as sg
from Correlation import Correlation

class GuiRunner:

    def __init__(self):
        self.main()

    def parseHandles(self,handles):
        handles = handles.replace(" ","")
        return handles.split(",")
    
    def getMonths(self,values):
        endMonth = values['EndMonth']
        startMonth = values['StartMonth']
        start = self.gui.Months[0:self.gui.Months.index(endMonth)]
        end = self.gui.Months[self.gui.Months.index(startMonth)+1:len(self.gui.Months)]
        self.gui.window.FindElement('EndMonth').Update(values=end,value=values['EndMonth'],size=(10,10))
        self.gui.window.FindElement('StartMonth').Update(values=start, value=values['StartMonth'], size=(10, 10))

    def main(self):
        self.gui = Gui()
        self.Intervals = ['1 Minute', '5 Minutes', '15 Minutes', '30 Minutes', '60 Minutes', '1 Day', '1 Week', '1 Month']
        prevTicker = ''
        while True:
            event,values = self.gui.data()
            self.getMonths(values)
            if not values['Ticker'] == prevTicker:
                self.gui.updateTickers()
                prevTicker = values['Ticker']
            if event == sg.WIN_CLOSED or event == 'Exit': exit()
            elif event == 'Run':
                toEnter = [ values['Ticker'],
                            self.Intervals.index(values['Interval']),
                            values['StartMonth'],
                            values['EndMonth'],
                          ]
                self.gui.update('SD',"Calculating...")
                self.gui.update('SMVI',"Calculating...")
                self.gui.update('Terminal','Calculating...')
                allSlices = self.gui.Months
                if values['Handle'] == '' or values['Handle'] == 'Handle':
                    sg.popup('Error, please enter a valid Twitter handle')
                    continue
                print(type(toEnter[1]))
                stock = Stock(toEnter[0],toEnter[1],toEnter[2],toEnter[3],allSlices,False)
                if stock.hasErrors:
                    self.gui.update('Terminal','An error occured')
                else:
                    SDToDisplay = str(stock.SDToDisplay)[0:8]
                    self.gui.update('SD',SDToDisplay)
                    print('Calculating baseline...')
                    self.gui.update('Terminal','Calculating baseline...')
                    DIA = Stock('DIA',toEnter[1],toEnter[2],toEnter[3],allSlices,True)
                    self.gui.update('Terminal','Calculating SVMI')
                    time.sleep(1)
                    cor = Correlation(stock,DIA,self.parseHandles(values['Handle']))
                    SMVI = str(cor.SMVI * float(SDToDisplay))[0:8]
                    self.gui.update('SMVI',SMVI)
                    self.gui.update('Terminal','Done!')

runner = GuiRunner()


