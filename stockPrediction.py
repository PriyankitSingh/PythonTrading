import datetime as dt
import pandas as pd 
import dataFetcher as df
import matplotlib.pyplot as pyplot
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
from matplotlib import style
import pandas_datareader.data as web

style.use('ggplot')


def getData():
	start = dt.datetime(2000, 1, 1)
	end = dt.datetime(2018, 1, 1)

	dataframe = web.DataReader('TSLA', 'yahoo', start, end)
	dataframe.to_csv('tsla.csv')

def readCSV(filename):
	dataframe = pd.read_csv(filename, parse_dates=True, index_col=0)
	return dataframe

def multiplot(dataframe):
	ax1 = pyplot.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
	ax2 = pyplot.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1)
	ax1.plot(dataframe.index, dataframe['Adj Close'])
	ax1.plot(dataframe.index, dataframe['100ma'])
	ax2.bar(dataframe.index, dataframe['Volume'])
	pyplot.show()

'''
Do a 100 point moving average
'''
def rollingAverages(dataframe, amount):
	dataframe['100ma'] = dataframe['Adj Close'].rolling(window=amount).mean()
	dataframe.dropna(inplace=True)

'''
This is important is the compny had a stock split. Converts data in form open high low close
'''
def resampleOHLC(dataframe):
	df_ohlc = dataframe['Adj Close'].resample('10D').ohlc()
	df_volume = dataframe['Volume'].resample('10D').sum()
	df_ohlc.reset_index(inplace=True)
	# convert date to mdates
	df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)

	ax1 = pyplot.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
	ax2 = pyplot.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1)
	ax1.xaxis_date()
	candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')
	ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)
	pyplot.show()


def plotcandlesticks(dataframe):
	ax1 = pyplot.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
	ax2 = pyplot.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1)
	# do the rest here

if __name__== "__main__":
	# getData()
	dataframe = readCSV('tsla.csv')

	## plot the adjusted close
	# dataframe['Adj Close'].plot()
	# pyplot.show()

	# print(dataframe[['Open', 'High']].head())
	## calculate a 100 moving average and add that to a new column
	# rollingAverages(dataframe, 100)
	# resampleOHLC(dataframe)
	# print(dataframe.head())
	# df.saveSP500Tickers()
	df.getDataYahoo()
	df.compileSP500Data()
	df.visualiseData()
	# multiplot(dataframe)
