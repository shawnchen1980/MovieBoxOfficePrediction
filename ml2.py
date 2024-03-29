# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 21:43:38 2019

@author: shawn
"""

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

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
#%matplotlib inline
#将一个形如$1,000的字符串变为整数1000
def moneyToNum(money):
    value = Decimal(sub(r'[^\d.]', '', money))
    return int(value)


dataset = pd.read_csv('frame4.csv')
#dataset['cat']=0
#dataset.loc[dataset['Gross_x']<4000,'cat']=0
#dataset.loc[(dataset['Gross_x']>4000) & (dataset['Gross_x']<8000),'cat']=1
#dataset.loc[(dataset['Gross_x']>8000) & (dataset['Gross_x']<16000),'cat']=2
#dataset.loc[(dataset['Gross_x']>16000) & (dataset['Gross_x']<40000),'cat']=3
#dataset.loc[(dataset['Gross_x']>40000) & (dataset['Gross_x']<120000),'cat']=4
#dataset.loc[(dataset['Gross_x']>120000) & (dataset['Gross_x']<1000000),'cat']=5
#dataset.loc[(dataset['Gross_x']>1000000) & (dataset['Gross_x']<15000000),'cat']=6
#dataset.loc[dataset['Gross_x']>15000000,'cat']=7
#dataset["Weekend Gross_y"]=[moneyToNum(m) for m in dataset["Weekend Gross_y"]]
#dataset["Total Gross_y"]=[moneyToNum(m) for m in dataset["Total Gross_y"]]
#dataset["Weekend Gross_x"]=[moneyToNum(m) for m in dataset["Weekend Gross_x"]]

#sns.pairplot(dataset)
#plt.show()
X=dataset.iloc[:,[0,1,2,3,4,5,6,7,8,9,14,15,16,17,18]]
#X=dataset.iloc[:,1:5]
y=dataset.iloc[:,20]
#dummy_y=np_utils.to_categorical(y)


from sklearn.preprocessing import  MinMaxScaler
sc= MinMaxScaler()
X= sc.fit_transform(X)
#y= y.reshape(-1,1)
#y=sc.fit_transform(y)




from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,random_state=0)
clf = LogisticRegression(random_state=0, solver='lbfgs',multi_class='ovr').fit(X_train, y_train)

y_pred=clf.predict(X_test)

#t1=np.argmax(y_pred, axis=1)
#t2=np.argmax(y_test, axis=1)

from sklearn.metrics import confusion_matrix
c1=confusion_matrix(y_test,y_pred)
print(c1)
#
#from keras import Sequential
#from keras.layers import Dense

#
#estimator = KerasClassifier(build_fn=build_model, epochs=100, batch_size=5, verbose=0)
#kfold = KFold(n_splits=10, shuffle=True)
#results = cross_val_score(estimator, X, dummy_y, cv=kfold)
#print("Baseline: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))



#from keras.wrappers.scikit_learn import KerasRegressor
#regressor = KerasRegressor(build_fn=build_regressor, batch_size=32,epochs=100)
#results=regressor.fit(X_train,y_train)
#y_pred= regressor.predict(X_test)
#
#fig, ax = plt.subplots()
#ax.scatter(y_test, y_pred)
#ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
#ax.set_xlabel('Measured')
#ax.set_ylabel('Predicted')
#plt.show()
#from sklearn.metrics import r2_score
#
#print(r2_score(y_test, y_pred))