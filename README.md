# PythonTrading
Use python to make predictions about S&P 500 companies' stock price

Basic code is from the youtube channel sentdex's playlist about python as a test bench. This is to plug in new strategies 

How to run (might be wrong because readme is updated less often than the code):
- Grab the data by running stockPrediction.py
- To run the correlation code and create a heatmap, add df.visualizeData() to the end of stockPrediction.py
- Preprocess machine learning data by running machineLearning.py
- Make a ML model by running machineLearning.py

TODO: 
- Make machine learning training data with more granular data for increased accuracy
- Create new data for new strategies.
- Use Quantopian for backtesting and better data
- Use days till next earnings announcement data because that has an effect on stock prices. Try to make a different strategy for that.

Bugs: 
-code throws an error when some data cannot be downloaded. have to run the code multiple times to download everything and get rid of the error
