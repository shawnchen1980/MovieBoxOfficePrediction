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

def getOpeningStats():
    df=pd.read_csv("yearsFormated.csv")
    df1=df.shift(periods=-1,fill_value=0)
    df1=df1.loc[:,['Year','Week','Top 10 Gross','Overall Gross']]
    df1.columns=['lYear','lWeek','lTop 10 Gross','lOverall']
    df=df.join(df1)
    df=df.iloc[:-1,:]
    lTop,lGross,lTGross,lWeeks=[],[],[],[]
    for yr,wk in list(zip(df['lYear'],df['lWeek'])):
        df1=pd.read_csv(f"dataset/{yr}-{wk}.csv")
        lTop.append(df1.loc[0,'Release'])
        lGross.append(moneyToNum(df1.loc[0,'Gross']))
        lTGross.append(moneyToNum(df1.loc[0,'Total Gross']))
        lWeeks.append(df1.loc[0,'Weeks'] if(df1.loc[0,'Weeks']!="-") else 1)
        print(f"{yr}-{wk} done")
    df['lTop']=lTop
    df['lGross']=lGross
    df['lTGross']=lTGross
    df['lWeeks']=lWeeks
    df1=pd.read_csv("weekStats.csv")
    wT10g,wOverallg,wRelease=[],[],[]
    
    for wk in list(df['Week']):
        print(f"{wk} is comming")
        if(wk<=52):
            wT10g.append(df1.iloc[wk-1,1])
            wOverallg.append(df1.iloc[wk-1,2])
            wRelease.append(df1.iloc[wk-1,3])
        else:
            wT10g.append(0)
            wOverallg.append(0)
            wRelease.append(0)
    df['wT10Gross']=wT10g
    df['wOverallGross']=wOverallg
    df['wRelease']=wRelease
    df.to_csv("frame1.csv",index=False)
    return df

def getNewMovies(yr,wk):
    df=pd.read_csv(f"dataset/{yr}-{wk}.csv")
    df=df.loc[(df["LW"]=="-") & ((df["Weeks"]==1)|(df["Weeks"]=="1"))]
    return df

def getAllNewMovies():
    df=pd.read_csv("yearsFormated.csv")
    df1=getNewMovies(2008,1)
    df1=df1.iloc[0:0]
    for yr,wk in list(zip(df["Year"],df["Week"])):
        df2=getNewMovies(yr,wk)
        df1=df1.append(df2)
        print(f"{yr}-{wk} done!")
    df2=pd.read_csv("allYearsMoviesWithCast.csv")
    df1=df1.groupby(["Release","Distributor"],as_index=False).last()
    df3=pd.merge(df1,df2,left_on=["Release","Distributor"],right_on=["Release","Distributor"])
    df3=df3.sort_values(["year_x","week","Rank_x"],ascending=[False,False,True])
    df3.to_csv("frame2.csv",index=False)
    return df1,df2,df3

def findDuplicates(arr):
    seen = {}
    dupes = []
    for x in arr:
        if x not in seen:
            seen[x] = 1
        else:
            if seen[x] == 1:
                dupes.append(x)
            seen[x] += 1
    return seen,dupes

def getThisAndNextWeekDataset():
    df=pd.read_csv("frame1.csv")
    dfs=[]
    for yr1,wk1,yr2,wk2 in list(zip(df["lYear"],df["lWeek"],df["Year"],df["Week"])):
        df1=pd.read_csv(f"dataset/{yr1}-{wk1}.csv")
        df2=pd.read_csv(f"dataset/{yr2}-{wk2}.csv")
        dff=pd.merge(df1,df2,on=["Release","Distributor"])
        dfs.append(dff)
        dff["Gross_x"]=dff["Gross_x"].apply(lambda x:moneyToNum(x))
        dff["Total Gross_x"]=dff["Total Gross_x"].apply(lambda x:moneyToNum(x))
        dff["Gross_y"]=dff["Gross_y"].apply(lambda x:moneyToNum(x))
        dff["Total Gross_y"]=dff["Total Gross_y"].apply(lambda x:moneyToNum(x))
        print(f"{yr1}-{wk1}-{yr2}-{wk2} done")
    df=pd.concat(dfs)
    df=df.loc[(df["Weeks_x"]!="-")|(df["Weeks_y"]!="-")]
    df=df.loc[(df["Weeks_x"]!="-")|(df["Weeks_y"]!=1)]
    df=df.loc[(df["Weeks_x"]!="-")|(df["Weeks_y"]!="1")]
    Weeks_y=[]
    for wks1,wks2 in list(zip(df["Weeks_x"],df["Weeks_y"])):
        print(f"{wks1}-{wks2}")
        if (wks2==1 or wks2=="1" or wks2=="-"):
            
            Weeks_y.append(int(wks1)+1)
        else:
            Weeks_y.append(int(wks2))
        
    df["Weeks_y"]=Weeks_y
    df.to_csv("frame3.csv",index=False)
    return df

def getOpeningMovieStats():
    df1=pd.read_csv("frame1.csv")
    df2=pd.read_csv("frame2.csv")
    df1=df1.loc[:,["Year","Week","Releases","wT10Gross","wRelease","lGross","lTGross","lWeeks","lTop 10 Gross","lOverall"]]
    df2=df2.loc[:,["year_x","week","Release","Distributor","Theaters","t100","t500","t5k","mem","Gross_x"]]
    df=pd.merge(df1,df2,left_on=["Year","Week"],right_on=["year_x","week"])
    df["Gross_x"]=df["Gross_x"].apply(lambda x:moneyToNum(x))
    df=df.loc[df["Theaters"]!="-"]
    df.to_csv("frame4.csv",index=False)
    return df

df=getOpeningMovieStats()


#df=getAllMovieCastStats()
#df=getMoviesDetail(25)
#
#df=getMoviesDetail(25)
#
#df=getMoviesDetail(25)