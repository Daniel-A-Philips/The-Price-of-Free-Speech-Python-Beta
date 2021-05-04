import requests
class FinnHub:

    def __init__(self,start,end,Ticker,Interval,forSMVI):
        self.key = 'c1vv82l37jkoemkedus0'
        self.start = start
        self.end = end
        self.Ticker = Ticker.upper()
        self.Interval = Interval
        self.forSVMI = forSMVI
        self.Format = 'csv'
        self.rawData = []

    def URLConnect(self,start,end):
        start = str(start)
        end = str(end)
        self.Interval = str(self.Interval)
        print('Connecting to URL')
        r = requests.get(
            'https://finnhub.io/api/v1/stock/candle?symbol=' + self.Ticker + '&resolution=' + self.Interval + '&from=' + start + '&to=' + end + '&format=' + self.Format + '&token=' + self.key)
        data = str(r.content).split("\\n")
        data.pop(0)
        data.remove("'")
        print(str(data))
        self.rawData.append(data)

    def writeData(self):
        csvwriter = open('test.csv','w')
        for data in self.rawData:
            for line in data:
                csvwriter.write(line + '\n')

    def run(self):
        self.URLConnect(self.start,self.end)
        self.writeData()



a = FinnHub(1615298999,1615502599,'AAPL',15,False)
a.URLConnect(1615298999,1615502599)
a.writeData()