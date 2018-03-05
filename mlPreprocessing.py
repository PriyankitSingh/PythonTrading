import numpy as np
import pandas as pd 
import pickle
from collections import Counter
from sklearn import svm, cross_validation, neighbors
from sklearn.ensemble import VotingClassifier, RandomForestClassifier

'''
calculate the percentage change in stock prices over the period of a week
'''
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
pass in a whole week's prices. Checks the percentage change and returns 1 for buy, -1 for sell and 0 for hold.
These labels will be used as a class for machine learning.
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

'''
Create a featureset for machine learning with X as percentage change and y as class label of buy, sell and hold
'''
def extractFeaturesets(ticker):
	tickers, dataframe = processDataForLabels(ticker)
	dataframe['{}_target'.format(ticker)] = list(map(buy_sell_hold, 
		dataframe['{}_1d'.format(ticker)], 
		dataframe['{}_2d'.format(ticker)], 
		dataframe['{}_3d'.format(ticker)],
		dataframe['{}_4d'.format(ticker)],
		dataframe['{}_5d'.format(ticker)]))
	vals = dataframe['{}_target'.format(ticker)].values.tolist() ## TODO: do we need this?
	stringValue = [str(i) for i in vals]
	print('data spread: ', Counter(stringValue))
	dataframe.fillna(0, inplace=True)
	dataframe = dataframe.replace([np.inf, -np.inf], np.nan) # replace infinities
	dataframe.dropna(inplace=True)
	# define features for ml which is percent change for yesterday
	dataframe_values = dataframe[[ticker for ticker in tickers]].pct_change()
	dataframe_values = dataframe_values.replace([np.inf, -np.inf], 0)
	dataframe_values.fillna(0, inplace=True)
	# X is percentage price change (feature set), y is the label
	X = dataframe_values.values
	y = dataframe['{}_target'.format(ticker)].values
	return X, y, dataframe

if __name__== "__main__":
	extractFeaturesets('MMM')


