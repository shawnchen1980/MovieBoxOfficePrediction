# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 23:11:55 2019

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

#抓取前50位影星的链接（拿到这些链接后怎么进一步抓取，自己想一想）
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

def generateDataFrame():
    left=pd.read_csv("oldFilmWithLastithWeek.csv")
    right=left
    df=pd.merge(left,right,left_on=["Title","last ith week"], right_on=["Title","ith week"])
    df=df.loc[:,["Title","LW_x","Weekend Gross_y","Total Gross_y","Week #_x","TW_x","Weekend Gross_x"]]
    df.to_csv("dataframe.csv",index=False)
    return df        

def getWeekendDataByWeek(wk):
    url="https://www.boxofficemojo.com/weekend/by-week/{}/".format(wk)
    req=requests.get(url)
    df=pd.read_html(req.text)[0]
    df=df.iloc[:,0:8]
#    df["week"]=wk
    df.insert(1,"week",wk)
    return df
    
def getWeekendDataByWeeks(start,end):
    if(os.path.exists("weeks.csv")):
        df=pd.read_csv("weeks.csv")
    else:
        df=getWeekendDataByWeek(start)
        start+=1
    for wk in range(start,end):
        df=df.append(getWeekendDataByWeek(wk))
    df.to_csv("weeks.csv",index=False)
    return df

def getWeekendDataByYearWeek(yr,wk):
    url=f"https://www.boxofficemojo.com/weekend/{yr}W{wk:02}/?ref_=bo_wey_table_1"
    req=requests.get(url)
    df=pd.read_html(req.text)[0]
    df=df.iloc[:,0:11]
#    df["week"]=wk
    df.insert(0,"year",yr)
    df.insert(1,"week",wk)
    return df

def getWeekendDataByYearWeeks(yr,start,end):
    if(os.path.exists("yearweeks.csv")):
        df=pd.read_csv("yearweeks.csv")
    else:
        df=getWeekendDataByYearWeek(yr,start)
        start+=1
    for wk in range(start,end):
        df=df.append(getWeekendDataByYearWeek(yr,wk))
        print(f"{yr}-{wk} done!")
    df.to_csv("yearweeks.csv",index=False)
    return df

def getWeekendDataByYear(yr):
    url="https://www.boxofficemojo.com/weekend/by-year/{}/".format(yr)
    req=requests.get(url)
    soup=BeautifulSoup(req.text,"html.parser")
    links=list(map(lambda x:x['href'],soup.select(".a-text-left a[href^='/weekend']")))
    df=pd.read_html(req.text)[0]
    cols=['Dates',  'Week' ,'Top 10 Gross', '%± LW', 'Overall Gross', '%± LW.1', 'Releases', '#1 Release' ]
    df=df.loc[:,cols]
    df['link']=links
#    df["week"]=wk
    df.insert(1,"year",yr)
    return df

#年份从近到远
def getWeekendDataByYears(start,end):
    if(os.path.exists("years.csv")):
        df=pd.read_csv("years.csv")
    else:
        df=getWeekendDataByYear(start)
        start-=1
    for yr in range(start,end,-1):
        df=df.append(getWeekendDataByYear(yr))
        print(f"{yr} done!")
    df.to_csv("years.csv",index=False)
    return df

df=getWeekendDataByYears(2019,2007)