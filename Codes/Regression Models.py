# -*- coding: utf-8 -*-
"""
Code References - 
http://machinelearningmastery.com/evaluate-performance-machine-learning-algorithms-python-using-resampling/
http://machinelearningmastery.com/metrics-evaluate-machine-learning-algorithms-python/
http://stackoverflow.com/questions/41753795/sklearn-timeseriessplit-cross-val-predict-only-works-for-partitions
"""

import pandas as pd
import json
  
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import TimeSeriesSplit
from sklearn import model_selection
from sklearn import linear_model


with open("data.json",'r') as f:
    timedict = json.load(f)
    
df = pd.DataFrame.from_dict(timedict, orient='index')
df = df.interpolate()
df.index = pd.to_datetime(df.index)

df['Date'] = pd.to_datetime(df.index)
df['Date'] = df['Date'].astype('int64')//1e9

feature_cols = ['Date','android_file_size','android_avg_rating','android_ratings_5']
#feature_cols = ['Date', 'android_ratings_2', 'android_ratings_4', 'android_ratings_5']
X = df[feature_cols]
Y = df.android_total_ratings
#Y = df.ios_all_ratings

X = pd.DataFrame(X)
Y = pd.DataFrame(Y)

test_size = 0.33
seed = 7
kfold = model_selection.ShuffleSplit(n_splits=10, test_size=test_size, random_state=seed)
#model0 = LinearRegression()
model = linear_model.Ridge()
model2 = linear_model.Lasso()
#results = model_selection.cross_val_score(model, X, Y, cv=kfold)
results = model_selection.cross_val_score(model, X, Y, cv=TimeSeriesSplit(n_splits=2).split(df))
print("Accuracy: %.3f%% (%.3f%%)") % (results.mean()*100.0, results.std()*100.0)

new_record = pd.DataFrame([[1478044200,259.0,4239138.0,0,4.0,77.0,4239138.0]],
                          columns=['Date','ios_file_size','android_total_ratings',
                          'ios_all_ratings','android_avg_rating','android_file_size'
                          'android_ratings_5'])
    
#new_record = pd.DataFrame([[1478044200,277695.0,832416.0,4239138.0,0.0]],columns=['Date', 'android_ratings_2', 'android_ratings_4', 'android_ratings_5','ios_all_ratings'])

df = pd.concat([df,new_record])

X_train = X[:14700]
Y_train = Y[:14700]

X_test = X[14700:14701]
Y_test = Y[14700:14701]

model3 = linear_model.ElasticNet()
model3.fit(X_train, Y_train)
print model3.intercept_
print model3.coef_
print model3.predict(X_test)

