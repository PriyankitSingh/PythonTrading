import numpy as np
import pandas as pd 
import pickle
from collections import Counter
import mlPreprocessing as preproc 
from sklearn import svm, cross_validation, neighbors
from sklearn.ensemble import VotingClassifier, RandomForestClassifier

def createModel(ticker):
	X, y, dataframe = preproc.extractFeaturesets(ticker)
	# do a 70-30 split on training and test data
	XTrain, XTest, yTrain, yTest = cross_validation.train_test_split(X, y, test_size=0.3)
	# define a classifier, try different ones
	classifier = neighbors.KNeighborsClassifier()
	classifier.fit(XTrain, yTrain) # train the classifier
	confidence = classifier.score(XTest, yTest)
	print('accuracy: ', confidence)
	# pickle the classifier to avoid retraining it again. This can be used to test different models 
	# against the same data without spending an eternity on training the classifiers
	
	# make a prediction on random values
	predictions = classifier.predict(XTest)

	print('prediction: ', Counter(predictions))
	return confidence

createModel('MMM')