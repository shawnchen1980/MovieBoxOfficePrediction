# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 23:11:55 2019

@author: shawn
"""

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests

#url="https://www.boxofficemojo.com/weekend/chart/?yr=2018&wknd=01&p=.htm"
#
#req=requests.get(url)
#
#dfs=pd.read_html(req.text)

def getWeekendData(yr,wk):
    url="https://www.boxofficemojo.com/weekend/chart/?yr={}&wknd={}&p=.htm".format(yr,wk)
    req=requests.get(url)
    df=pd.read_html(req.text)[2]
    df.columns=['TW', 'LW', 'Title','Studio', 'Weekend Gross', '% Change',
 'Theater Count', 'Change', 'Average', 'Total Gross', 'Budget*', 'Week #']
    df=df.drop(index=df.shape[0]-1)
    df=df.drop(index=0)
    df['ith year']=yr
    df['ith week']=wk
    return df

def getWeekendsData(arr):
    df=None
    for item in arr:
        for wk in range(item[1]):
            df=getWeekendData(item[0],wk+1) if df is None else df.append(getWeekendData(item[0],wk+1))
    return df
            

df=getWeekendsData([(2018,10)])
    