# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 23:34:19 2019

@author: shawn
"""

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline

dataset = pd.read_csv('frame3.csv')
dataset=dataset.loc[:,['Rank_x','Gross_x','Theaters_x','Total Gross_x','Weeks_y','Gross_y']]
dataset=dataset.loc[dataset["Theaters_x"]!="-"]

X = dataset.iloc[:,0:-1]   
y = dataset.iloc[:,-1]


sc= MinMaxScaler()
X= sc.fit_transform(X)
y= y.values.reshape(-1,1)
y=sc.fit_transform(y)

# define the model
def larger_model():
	# create model
	model = Sequential()
	model.add(Dense(5, input_dim=5, kernel_initializer='normal', activation='relu'))
	model.add(Dense(3, kernel_initializer='normal', activation='relu'))
	model.add(Dense(1, kernel_initializer='normal'))
	# Compile model
	model.compile(loss='mean_squared_error', optimizer='adam')
	return model

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,random_state=0)
estimator = KerasRegressor(build_fn=larger_model, epochs=20, batch_size=100, verbose=True)
estimator.fit(X_train, y_train)
y_pred = estimator.predict(X_test)


print("Mean squared error: %.2f"
      % mean_squared_error(y_test, y_pred))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % r2_score(y_test, y_pred))


train_error =  np.abs(y_test - y_pred)
mean_error = np.mean(train_error)
min_error = np.min(train_error)
max_error = np.max(train_error)
std_error = np.std(train_error)

print(mean_error,min_error,max_error,std_error)
#seed=7
#np.random.seed(seed)
#estimators = []
#estimators.append(('standardize', StandardScaler()))
#estimators.append(('mlp', KerasRegressor(build_fn=larger_model, epochs=50, batch_size=5)))
#pipeline = Pipeline(estimators)
#kfold = KFold(n_splits=10, random_state=seed)
#results = cross_val_score(pipeline, X, Y, cv=kfold, n_jobs=1)
#print("Larger: %.2f (%.2f) MSE" % (results.mean(), results.std()))