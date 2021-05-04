class Interaction:

    def __init__(self,Ticker,Interval,StartSlice,EndSlice,Handle,forSMVI):
        self.Ticker = Ticker
        self.Interval = Interval
        self.StartSlice  = StartSlice
        self.EndSlice = EndSlice
        self.Hanlde = Handle
        self.forSMVI = forSMVI
    
    def run():
        print("Running Interaction")
        self.stock = Stock(self.Ticker,self.Interval,self.StartSlice,self.EndSlice,self.forSMVI)
