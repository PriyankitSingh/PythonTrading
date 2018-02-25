import os
import bs4 as bs
import pandas as pd
import pickle
import requests
import numpy as np
import datetime as dt
import matplotlib.pyplot as pyplot
from matplotlib import style
import pandas_datareader.data as web

style.use('ggplot')

def saveSP500Tickers():
	resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
	soup = bs.BeautifulSoup(resp.text, 'lxml')
	table = soup.find('table', {'class':'wikitable sortable'})
	tickers = []
	for row in table.findAll('tr')[1:]:
		ticker = row.findAll('td')[0].text
		tickers.append(ticker)

	with open("sp500tickers.pickle", "wb") as f:
		pickle.dump(tickers, f)
	print (tickers)
	return tickers

'''
Get all the S&P 500 data from yahoo once so we don't have to redownload data at every run.
Should grab new data every day because prices are updated daily
'''
def getDataYahoo(reloadSP500=False):
	if reloadSP500:
		tickers = saveSP500Tickers()
	else:
		with open("sp500tickers.pickle", "rb") as f:
			tickers = pickle.load(f)
	if not os.path.exists('stock_dfs'):
		os.makedirs('stock_dfs')
	
	start = dt.datetime(2000, 1, 1)
	end = dt.datetime(2018, 1, 1)

	# loop through all tickers and grab their data
	for ticker in tickers[:25]: # TODO: currently only grabbing 25 to reduce the amount of data
		if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
			print('Downloading {}'.format(ticker))
			try:
				df = web.DataReader(ticker, 'yahoo', start, end)
				df.to_csv('stock_dfs/{}.csv'.format(ticker))
			except Exception as e:
				print ('could not download {}'.format(ticker))
		else:
			print ('already have {}'.format(ticker))

def compileSP500Data():
	with open("sp500tickers.pickle", "rb") as f:
		tickers = pickle.load(f)
	mainDataframe = pd.DataFrame()

	for count, ticker in enumerate (tickers[:25]):
		try:
			df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
			df.set_index('Date', inplace=True)
			df.rename(columns = {'Adj Close': ticker}, inplace=True)
			df.drop(['Open', 'Close', 'High', 'Low', 'Volume'], 1, inplace=True)
		except Exception as e:
			print('Could not find {}'.format(ticker))	

		if mainDataframe.empty:
			mainDataframe = df
		else:
			mainDataframe = mainDataframe.join(df, how='outer')

		if count% 10 == 0:
			print(count)

		mainDataframe.to_csv('sp500JoinedCloses.csv')


'''
Generate a correlation table of dataframe
'''
def visualiseData():
	df = pd.read_csv('sp500JoinedCloses.csv')
	df_corr = df.corr()
	data = df_corr.values
	fig = pyplot.figure()
	ax = fig.add_subplot(1, 1, 1)
	
	heatmap = ax.pcolor(data, cmap=pyplot.cm.RdYlGn)
	# make a legend
	fig.colorbar(heatmap)
	ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False)
	ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)
	ax.invert_yaxis()
	ax.xaxis.tick_top()

	column_labels = df_corr.columns
	row_lables = df_corr.index

	ax.set_xticklabels(column_labels)
	ax.set_yticklabels(row_lables)
	pyplot.xticks(rotation=90)
	heatmap.set_clim(-1, 1)
	pyplot.tight_layout()
	pyplot.show()

