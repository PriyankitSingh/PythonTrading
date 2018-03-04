import numpy as np
import pandas as pd 
import pickle

def processDataForLabels(ticker):
	numDays = 5 # markets are open 5 days a week
	dataframe = pd.read_csv('sp500JoinedCloses.csv', index_col=0)
	tickers = dataframe.columns.values.tolist()
	dataframe.fillna(0, inplace=True)
	for i in range(1, numDays + 1):
		# percentage price change in the past i days. Formula = (today's price - price in i days)/today's price
		# shift -i shifts up, etting the future data
		dataframe['{}_{}d'.format(ticker, i)] = (dataframe[ticker].shift(-i) - dataframe[ticker]) / dataframe[ticker]
	dataframe.fillna(0, inplace=True)
	return tickers, dataframe

'''
pass in a whole week's prices and 
'''
def buy_sell_hold(*args):
	cols = [c for c in args]
	requirement = 0.02 # how much percentage change is required to trigger a buy or a sell
	for col in cols:
		if col > requirement:
			return 1
		if col < -requirement:
			return -1
	return 0

