from fast_autocomplete import AutoComplete as AC
import difflib
import os
import csv
class predictor:

	def getTickers(self):
		self.allTickers = []
		with open(os.getcwd() + '/Data/tickers.csv') as file:
			reader = csv.reader(file)
			for line in reader:
				if not line[0] == 'Symbol': self.allTickers.append(line[0])

	def getClosest(self,current):
		number_to_show = 15 - (2 * len(current))
		if number_to_show <= 0:
			number_to_show = 1
		closest = difflib.get_close_matches(current.upper(),self.allTickers,n=number_to_show)
		return closest

	def __init__(self):
		self.getTickers()
	