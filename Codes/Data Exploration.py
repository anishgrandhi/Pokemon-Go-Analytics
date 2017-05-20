# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 11:29:57 2017
Get highly correlated pairs - http://stackoverflow.com/questions/17778394/list-highest-correlation-pairs-from-a-large-correlation-matrix-in-pandas
@author: Anish
"""
#import necessary modules
import pandas as pd
import json
import matplotlib.pyplot as plt
from pandas.tools.plotting import scatter_matrix

#open the json file
with open("data.json",'r') as f:
    timedict = json.load(f)

#load the information into Pandas DF and use describe()
df = pd.DataFrame.from_dict(timedict, orient='index')
df = df.interpolate()
print df.describe()

#plot the scatter matrix
scatter_matrix(df, figsize=(15,15))#, diagonal='kde')
print plt.show()

#Get the top 20 correlated pairs
def get_redundant_pairs(df):
    '''Get diagonal and lower triangular pairs of correlation matrix'''
    pairs_to_drop = set()
    cols = df.columns
    for i in range(0, df.shape[1]):
        for j in range(0, i+1):
            pairs_to_drop.add((cols[i], cols[j]))
    return pairs_to_drop

def get_top_abs_correlations(df, n=5):
    au_corr = df.corr(method='pearson', min_periods=1000).abs().unstack()
    labels_to_drop = get_redundant_pairs(df)
    au_corr = au_corr.drop(labels=labels_to_drop).sort_values(ascending=False)
    return au_corr[0:n]

print("Top Absolute Correlations")
print(get_top_abs_correlations(df, 20))

#Plots for file sizes
columns = ['android_file_size','ios_file_size']
df[columns].plot(fontsize=10,figsize=(12,12),title='iOS and Android File Size')

#Plots for Android Ratings
ratings = ['android_ratings_1','android_ratings_2','android_ratings_3','android_ratings_4','android_ratings_5','android_total_ratings']
df[ratings].plot(fontsize=10,figsize=(12,12),title='Android Ratings')

#Plots for iOS Ratings
ratings = ['ios_all_ratings','ios_current_ratings']
df[ratings].plot(fontsize=10,figsize=(12,12),title='iOS Ratings')