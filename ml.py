# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 19:46:21 2019

@author: shawn
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from re import sub
from decimal import Decimal
#%matplotlib inline

def moneyToNum(money):
    value = Decimal(sub(r'[^\d.]', '', money))
    return int(value)


dataset = pd.read_csv('dataframe.csv')
dataset["Weekend Gross_y"]=[moneyToNum(m) for m in dataset["Weekend Gross_y"]]
dataset["Total Gross_y"]=[moneyToNum(m) for m in dataset["Total Gross_y"]]
dataset["Weekend Gross_x"]=[moneyToNum(m) for m in dataset["Weekend Gross_x"]]
sns.pairplot(dataset)
plt.show()

X=dataset.iloc[:,1:5]
y=dataset.iloc[:,6].values

from sklearn.preprocessing import  MinMaxScaler
sc= MinMaxScaler()
X= sc.fit_transform(X)
y= y.reshape(-1,1)
y=sc.fit_transform(y)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,random_state=0)

from keras import Sequential
from keras.layers import Dense
def build_regressor():
    regressor = Sequential()
    regressor.add(Dense(units=4, input_dim=4))
    regressor.add(Dense(units=1))
    regressor.compile(optimizer='adam', loss='mean_squared_error',  metrics=['mae','accuracy'])
    return regressor

from keras.wrappers.scikit_learn import KerasRegressor
regressor = KerasRegressor(build_fn=build_regressor, batch_size=32,epochs=100)
results=regressor.fit(X_train,y_train)
y_pred= regressor.predict(X_test)

fig, ax = plt.subplots()
ax.scatter(y_test, y_pred)
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
plt.show()