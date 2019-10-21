# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 17:56:54 2019

@author: shawn
"""
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import os.path
#url="https://www.boxofficemojo.com/weekend/chart/?yr=2018&wknd=01&p=.htm"
#
#req=requests.get(url)
#
#dfs=pd.read_html(req.text)
#给定年份和周数，获取某一周所有上映的影片的周末票房情况对应的df
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

#使用方法：获取一系列周的数据
#df=getWeekendsData([(2018,1,53)])
def getWeekendsData(arr):
    df=None
    for item in arr:
        for wk in range(item[1],item[2]):
            df=getWeekendData(item[0],wk) if df is None else df.append(getWeekendData(item[0],wk))
            print("{} {} is done".format(item[0],wk))
    return df

#把数据写入week.csv
def getWeekendsDataAndWrite(arr):
    df=getWeekendsData(arr)
    if(os.path.exists("week.csv")):
        dff=pd.read_csv("week.csv")
        df=dff.append(df)
    df.to_csv("week.csv",index=False)
    return

def getStarLinks():
    url="https://www.boxofficemojo.com/people/?view=Actor&pagenum=1&sort=sumgross&order=DESC&&p=.htm"
    req=requests.get(url)
    soup=BeautifulSoup(req.text,"html.parser")
    links=soup.select("a[href^='./chart/?view=Actor&id=']")
    url1="www.boxofficemojo.com/people"
    #print([(url1+link['href'][1:]) for link in links])
    #抓取特定的链接
    links=[(url1+link['href'][1:]) for link in links]
    return links