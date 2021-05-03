class FinnHub:

    def __init__(self,start,end,Ticker,Interval,forSMVI):
        self.start_end = []
        self.start_end.append(start)
        self.start_end.append(end)
        self.Ticker = Ticker.upper()
        self.Interval = Interval
        self.forSVMI = forSMVI