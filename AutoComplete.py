import os
import csv
import difflib
from fast_autocomplete import AutoComplete as AC

class predictor:

	def getTickers(self):
		self.allTickers = []
		with open(os.getcwd() + '/Data/tickers.csv') as file:
			reader = csv.reader(file)
			for line in reader:
				if not line[0] == 'Symbol': self.allTickers.append(line[0])

	def getClosest(self,current):
		if current == 'Ticker':
			return ['']
		number_to_show = 15
		closest = difflib.get_close_matches(current.upper(),self.allTickers,n=number_to_show)
		return closest

	def __init__(self):
		self.getTickers()
	