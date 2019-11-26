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
import matplotlib.pyplot as plt

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
#前面的函数已失效，从这个函数开始正式起作用
    
#输入：wk-第几周
#输出：有记录的所有年份中wk所指定的周中的票房统计信息，其中每条数据包括某一年在wk这一周中总体票房情况，包括发片数和票房总计
def getWeekendDataByWeek(wk):
    url="https://www.boxofficemojo.com/weekend/by-week/{}/".format(wk)
    req=requests.get(url)
    df=pd.read_html(req.text)[0]
    df=df.iloc[:,0:8]
#    df["week"]=wk
    df.insert(1,"week",wk)
    return df
#输入：start-起始周，end-终点周
#输出：利用上述函数批量获取近年来在特定周的票房统计情况，保存在weeks.csv文件中
#文件：weeks.csv中得每条数据包含了某一年在某一周中的票房表现，weeks(2008-2019).csv由这个文件筛选得来    
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



#输入：yr-年份，wk-周
#输出：对应某一年某一周的周末所有上映影片票房信息及票房排行
def getWeekendDataByYearWeek(yr,wk):
    url=f"https://www.boxofficemojo.com/weekend/{yr}W{wk:02}/?ref_=bo_wey_table_1"
    req=requests.get(url)
    df=pd.read_html(req.text)[0]
    df=df.iloc[:,0:11]
    df.insert(0,"year",yr)
    df.insert(1,"week",wk)
    return df

#输入：yr-年份，start-开始周，end-结束周
#输出：利用上一个函数分别抓取某一年从某开始周到某结束周的某周票房信息，并且累计存储在yearweeks.csv文件中
#文件：yearweeks.csv包含了近十年每一周所有影片的票房信息，总共900条左右数据
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

#读代码入口，从下面的函数开始读！！
#输入：yr-年份
#输出：某一年份中所有周次的每周票房大概统计以及该周详情页面的链接地址，通过链接地址可进一步获取每周票房详情
def getWeekendDataByYear(yr):
    url="https://www.boxofficemojo.com/weekend/by-year/{}/".format(yr)
    req=requests.get(url)
    soup=BeautifulSoup(req.text,"html.parser")
    links=list(map(lambda x:x['href'],soup.select(".a-text-left a[href^='/weekend']")))
    df=pd.read_html(req.text)[0]
    cols=['Dates',  'Week' ,'Top 10 Gross', '%± LW', 'Overall Gross', '%± LW.1', 'Releases', '#1 Release' ]
    df=df.loc[:,cols]
    df['link']=links
    df.insert(1,"year",yr)
    return df

#输入：start-开始年份，end-终点年份
#输出：利用上面的函数把从开始年份到终点年份所包含的所有周次的票房大概统计整合在一起，保存在years.csv文件中
#文件：years.csv包含了近十年每一周的票房大概统计以及每一周票房详情页面的链接，一共600条左右数据
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
#输入：yr-年份，wk-周，url-周票房详情链接地址
#输出：首先会查看对应的周票房详情文件是否存在，如果存在直接返回0，如果不存在，把url对应周票房详情页面中的数据下载并保存在dataset文件夹的文件中，并输出1
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
#输入：filepath-csv文件路径
#输出：将csv文件读取成pandas的dataframe，这个函数的作用是用来读取无法直接使用pd.read_csv函数读取的csv文件
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
#输入：money-表示为“$10,000”形式的字符串
#输出：money字符串对应的整数值，“$10,000”变为10000
def moneyToNum(money):
    value = Decimal(sub(r'[^\d.]', '', money))
    return int(value)
#输出：将years.csv文件中代表金额的列中的字符串转换为整数值后，以"yearsFormated.csv"文件输出
#文件：yearsFormated.csv是对years.csv文件的格式转换
def formatYears():
    if(not os.path.exists("years.csv")):
        return
    df=read_csv("years.csv")
    df["Top 10 Gross"]=df["Top 10 Gross"].apply(lambda x:moneyToNum(x))
    df["Overall Gross"]=df["Overall Gross"].apply(lambda x:moneyToNum(x))
    df.to_csv("yearsFormated.csv",index=False)
    return
#输入：limit-连续抓取文件数
#输出：根据yearsFormated.csv文件中记载的周详情链接去抓取周票房详情数据，并用函数generateMovieWeekendDataByLink保存到dataset文件夹下
def generateMovieWeekendFiles(limit=35):
    df=pd.read_csv("yearsFormated.csv")
    cfgs=list(zip(df["Year"],df["Week"],df["link"]))
    count=0
    for cfg in cfgs:
        count+=generateMovieWeekendDataByLink(cfg[0],cfg[1],cfg[2])
        if(count>limit):
            break
    return
#输入：yr-年份
#输出：年度票房详情数据，包括某一年中出了哪些影片，票房排行如何等，每条数据中包含了影片详情页面的链接地址
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
#输出：使用上述函数对近十年所有电影进行汇总，保存到allYearsMovies.csv文件中
#文件：allYearsMovies.csv中的每一条数据代表了一部影片，共包含8000多条数据
def getYearDataByYears():
    df=getYearDataByYear(2019)
    for i in range(2018,2007,-1):
        df=df.append(getYearDataByYear(i))
        print(f"{i}-done!")
    df.to_csv("allYearsMovies.csv",index=False)
    return df

path="https://www.boxofficemojo.com/release/rl3059975681/?ref_=bo_yld_table_1"
#输入：url-电影详情页链接地址，注意：这里的电影详情页不包括演员信息，但包括指向演员详情页（imdb网站）的链接地址
#输出：val-影片类型，val1-演员详情页网址，df-演员详情数据
def getMovieDetail(url):
    req=requests.get(url)
    soup=BeautifulSoup(req.text,"html.parser")
    val=soup.select(".mojo-summary-values>div.a-section:nth-of-type(4)>span:nth-of-type(2)")[0].text.split()
    val1=soup.select(".a-box-inner>a[href*='/cast?']")[0]['href']
    df=pd.read_html(val1)
    return val,val1,df[1] if(len(df)>1) else df[0]
#输入：limit-批量获取电影详情数据时连续访问次数
#输出：根据allYearsMovies.csv文件获取所有影片的详情页数据，再每次连续抓取若干条电影详情数据，把演员详细信息存入cast文件夹下，把影片的类型等信息存入movies.csv文件中
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

#输入：file-某影片演员详情文件路径
#输出：某影片各类等级演员数量统计值（t100,t500,t5k,mem）-前一百位演员数量，前500位。。。
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
#输出：将上述函数计算得到的某影片不同等级演员数量的统计与allYearsMovies.csv文件整合，得到新的allYearsMoviesWithCast.csv文件
#文件：allYearsMoviesWithCast.csv中的每条数据包含了某一部影片的总体票房信息以及其参演演员在不同的演员等级中所占的数量
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
#输出：根据weeks(2009-2019).csv文件中的数据统计近年来每一周的票房和出片数的平均值，并保存在weekStats.csv文件中
#文件：weekStats.csv共包含53条数据，每条数据包含了对近十年来某一周统计得出得平均出片数和平均票房
def getWeekStats():
    df=pd.read_csv("weeks(2008-2019).csv")
    df["Top 10 Gross"]=df["Top 10 Gross"].apply(lambda x:moneyToNum(x))
    df["Overall Gross"]=df["Overall Gross"].apply(lambda x:moneyToNum(x))
    df=df.groupby('week',as_index=False).mean()
#    df["Releases"]=df["Releases"].apply(lambda x:moneyToNum(x))
    df=df.iloc[:,[0,2,3,4]]
    df.to_csv('weekStats',index=False)
    return df
#输出：Year-某年，Week-某周，lYear-某年某周的上一周是哪年，lWeek-某年某周的上一周是哪周，比如2019年第一周的上一周是2018年53周或52周，此时lYear是2018，lWeek是53，lWeeks-上周票房冠军连映周数
#文件：frame1.csv，这个文件记录的是某年某周的上一周的票房冠军是哪部影片，该影片的周票房如何，总票房如何，连映周数如何，以及某年某周的周次上历史平均的发片数和票房值是什么
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
#输入：yr-年份，wk-哪一周
#输出：从dataset文件夹对应的文件中找出某年某周首次上映的影片及其在那周的票房情况
def getNewMovies(yr,wk):
    df=pd.read_csv(f"dataset/{yr}-{wk}.csv")
    df=df.loc[(df["LW"]=="-") & ((df["Weeks"]==1)|(df["Weeks"]=="1"))]
    return df
#输出：首先利用上述函数获得所有影片首映时的票房状况，包括上映影院数，票房统计等，再将得出的每条数据与allYearsMoviesWithCast.csv文件中的每条数据相关联
#由此用于预测首周票房成绩的特征变量以及目标变量
#文件：frame2.csv
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
#输出：分别读取前后两周影片票房详情表，将两表中相同影片所对应的数据做关联，就可得出同一部影片在前后两周的票房表现
#然后我们就可以根据前一周的票房信息去预测后一周的票房数据
#文件：frame3.csv，每一条数据包含前后同一影片在某连续两周里的票房表现，共包含51774条数据
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

#def generateCat(x):
#    if(x<4000):
#        return 0
#    elif(x>4000) and (x<8000):
#        return 1
#    elif(x>8000) and (x<16000):
#        return 2
#    elif(x>16000) and (x<40000):
#        return 3
#    elif(x>40000) and (x<120000):
#        return 4
#    elif(x>120000) and (x<1000000):
#        return 5
#    elif(x>1000000) and (x<15000000):
#        return 6
#    else:
#        return 7
    
def generateCat(x):
    if(x<100000):
        return 0
    elif(x>100000) and (x<1000000):
        return 1
    elif(x>1000000) and (x<10000000):
        return 2
    else:
        return 3
#输出：frame1.csv记录的是某年某周相关的票房统计信息，上周票房冠军信息等，frame2.csv记录的是某影片在某年某周首映时已知的信息，包括放映影院数，包括演员情况
#将这两个表的数据链接，并对首周票房字段进行分类，得出frame4.csv
#文件：frame4.csv其中每一条数据对应了某影片在首周上映时所知的信息以及首周票房分类信息，因此frame4.csv用于首周票房预测
def getOpeningMovieStats():
    df1=pd.read_csv("frame1.csv")
    df2=pd.read_csv("frame2.csv")
    df1=df1.loc[:,["Year","Week","Releases","wT10Gross","wRelease","lGross","lTGross","lWeeks","lTop 10 Gross","lOverall"]]
    df2=df2.loc[:,["year_x","week","Release","Distributor","Theaters","t100","t500","t5k","mem","Gross_x"]]
    df=pd.merge(df1,df2,left_on=["Year","Week"],right_on=["year_x","week"])
    df=df.loc[df["Theaters"]!="-"]
    df["Gross_x"]=df["Gross_x"].apply(lambda x:moneyToNum(x))
    df["Cat"]=df["Gross_x"].apply(lambda x:generateCat(x))
    df.to_csv("frame4.csv",index=False)
    return df

#生成一年52周平均票房与影片数的波动图
def generateWeekstatFig():
    df=pd.read_csv("weekStats.csv",index_col=0)
    fig,(ax1,ax2)=plt.subplots(2,1)
    ax1.plot(df.iloc[:,[0,1]])
    ax1.set_ylabel("Average Gross")
    ax1.legend(["Top 10","Overall"],loc="upper right")
    ax2.plot(df.iloc[:,[2]])
    ax2.set_ylabel("Releases")
    ax2.set_xlabel("Week#")
    fig.suptitle("Average Gross and Releases Number for Each week within a Year")

#生成直方图，用于表示首周末票房的分布    
def generateOpeningGrossHist():
    df=pd.read_csv("frame4.csv")
    fig,(ax1,ax2)=plt.subplots(2,1)
    ax1.hist(df["Gross_x"])
    ax2.hist(df["Cat"])

generateOpeningGrossHist()
#df=getOpeningMovieStats()


#df=getAllMovieCastStats()
#df=getMoviesDetail(25)
#
#df=getMoviesDetail(25)
#
#df=getMoviesDetail(25)