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
from decimal import Decimal
from re import sub
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

def generateMovieWeekendDataByLink(yr,wk,url):
    if(os.path.exists(f"dataset/{yr}-{wk}.csv")):
#        df=pd.read_csv(f"dataset/{yr}-{wk}.csv")
        print(f"pass {yr}-{wk}.csv")
        return 0
    url="https://www.boxofficemojo.com"+url
    df=pd.read_html(url)[0]
    df=df.iloc[:,:11]
    df.insert(0,'year',yr)
    df.insert(1,'week',wk)
    df.to_csv(f"dataset/{yr}-{wk}.csv",index=False)
    print(f"generate {yr}-{wk}.csv")
    return 1

def read_csv(filepath):
     if os.path.splitext(filepath)[1] != '.csv':
          return  # or whatever
     seps = [',', ';', '\t']                    # ',' is default
     encodings = [None, 'utf-8', 'ISO-8859-1']  # None is default
     for sep in seps:
         for encoding in encodings:
              try:
                  return pd.read_csv(filepath, encoding=encoding, sep=sep)
              except Exception:  # should really be more specific 
                  pass
     raise ValueError("{!r} is has no encoding in {} or seperator in {}"
                      .format(filepath, encodings, seps))
#将一个形如$1,000的字符串变为整数1000
def moneyToNum(money):
    value = Decimal(sub(r'[^\d.]', '', money))
    return int(value)

def formatYears():
    if(not os.path.exists("years.csv")):
        return
    df=read_csv("years.csv")
    df["Top 10 Gross"]=df["Top 10 Gross"].apply(lambda x:moneyToNum(x))
    df["Overall Gross"]=df["Overall Gross"].apply(lambda x:moneyToNum(x))
    df.to_csv("yearsFormated.csv",index=False)
    return

def generateMovieWeekendFiles(limit=35):
    df=pd.read_csv("yearsFormated.csv")
    cfgs=list(zip(df["Year"],df["Week"],df["link"]))
    count=0
    for cfg in cfgs:
        count+=generateMovieWeekendDataByLink(cfg[0],cfg[1],cfg[2])
        if(count>limit):
            break
    return


def getYearDataByYear(yr):
    url=f"https://www.boxofficemojo.com/year/{yr}/"
    req=requests.get(url)
    df=pd.read_html(req.text)[0]
    cols=['Rank', 'Release',  'Distributor', 'Gross', 'Max Th', 'Opening', '% of Total', 'Open Th', 'Open', 'Close']
    df=df.loc[:,cols]
    soup=BeautifulSoup(req.text,"html.parser")
    links=list(map(lambda x:x['href'],soup.select(".a-text-left a[href^='/release']")))
    df['link']=links
    df.insert(0,'year',yr)
    return df
    
def getYearDataByYears():
    df=getYearDataByYear(2019)
    for i in range(2018,2007,-1):
        df=df.append(getYearDataByYear(i))
        print(f"{i}-done!")
    df.to_csv("allYearsMovies.csv",index=False)
    return df

path="https://www.boxofficemojo.com/release/rl3059975681/?ref_=bo_yld_table_1"

def getMovieDetail(url):
    req=requests.get(url)
    soup=BeautifulSoup(req.text,"html.parser")
    val=soup.select(".mojo-summary-values>div.a-section:nth-of-type(4)>span:nth-of-type(2)")[0].text.split()
    val1=soup.select(".a-box-inner>a[href*='/cast?']")[0]['href']
    df=pd.read_html(val1)
    return val,val1,df[1] if(len(df)>1) else df[0]

def getMoviesDetail(limit=10):
    years=[]
    ranks=[]
    g=[]
    links=[]
    count=0
    df=pd.read_csv("allYearsMovies.csv")
    rows=list(zip(df['year'],df['Rank'],df['link']))
    for year,Rank,link in rows:
        if(os.path.exists(f"cast/{year}-{Rank}.csv")):
            print(f"{year}-{Rank} passed")
        else:
            genres,url,df1=getMovieDetail(f"https://www.boxofficemojo.com{link}")
            df1.to_csv(f"cast/{year}-{Rank}.csv",index=False)
            count+=1
            print(f"{year}-{Rank} generated")
            years.append(year)
            ranks.append(Rank)
            g.append(genres)
            links.append(url)
            if(count>=limit):break
        
    df2=pd.DataFrame({'year':years,'rank':ranks,'genres':g,'link':links})
    if(not os.path.exists("movies.csv")):
        df2.to_csv("movies.csv",index=False)
    else:
        df3=pd.read_csv("movies.csv")
        df2=df3.append(df2)
        df2.to_csv("movies.csv",index=False)
    return df2

import time

#while True:
#    df=getMoviesDetail(15)
#    time.sleep(15)


def getMovieCastStats(file):
    df=pd.read_csv(file)
    if(df.shape[1]!=3):
        return (0,0,0,0)
    all=df.shape[0]
    mem=df[df.iloc[:,1]=="Members only"].shape[0]
    t5k=df[df.iloc[:,1]=="Top 5000"].shape[0]
    t500=df[df.iloc[:,1]=="Top 500"].shape[0]
    t100=all-mem-t5k-t500
    return (t100,t500,t5k,mem)

def getAllMovieCastStats():
    t100,t500,t5k,mem=[],[],[],[]
    df=pd.read_csv("allYearsMovies.csv")
    rows=list(zip(df['year'],df['Rank']))
    for year,Rank in rows:
        if(os.path.exists(f"cast/{year}-{Rank}.csv")):
            a,b,c,d=getMovieCastStats(f"cast/{year}-{Rank}.csv")
            t100.append(a)
            t500.append(b)
            t5k.append(c)
            mem.append(d)
            print(f"{year}-{Rank} passed")
    print("all files are don")
    time.sleep(10)
    df['t100']=t100
    df['t500']=t500
    df['t5k']=t5k
    df['mem']=mem
    df.to_csv('allYearsMoviesWithCast.csv',index=False)
    return df

def getWeekStats():
    df=pd.read_csv("weeks(2008-2019).csv")
    df["Top 10 Gross"]=df["Top 10 Gross"].apply(lambda x:moneyToNum(x))
    df["Overall Gross"]=df["Overall Gross"].apply(lambda x:moneyToNum(x))
    df=df.groupby('week',as_index=False).mean()
#    df["Releases"]=df["Releases"].apply(lambda x:moneyToNum(x))
    df=df.iloc[:,[0,2,3,4]]
    df.to_csv('weekStats',index=False)
    return df

import matplotlib.pyplot as plt
import seaborn as sns

df=getWeekStats()
#sns.lineplot(data=df,x="week",y=["Releases","Top 10 Gross"])
#plt.plot('week','Top 10 Gross',data=df)
plt.figure()
f, axes = plt.subplots(2, 1)
axes[0].plot('week', 'Release',data=df)
axes[0].set_ylabel('Release')

axes[1].plot(x, y2)
axes[1].set_ylabel('y2')

plt.plot('week','Releases',data=df)
plt.legend()

#df=getAllMovieCastStats()
#df=getMoviesDetail(25)
#
#df=getMoviesDetail(25)
#
#df=getMoviesDetail(25)