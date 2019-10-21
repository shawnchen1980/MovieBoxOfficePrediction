# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 22:28:23 2019

@author: shawn
"""

Windows users, please open the anaconda prompt, which you can find this way:
Windows Button in the lower left corner -> List of programs -> anaconda -> anaconda prompt
Then inside the anaconda prompt, copy-paste and enter the following line command:

conda install -c conda-forge keras

email:chenxiao@sincereedu.com

10.21 任务计划


1 生成训练数据集，要求包含以下字段：
数据框架一
year-年份
week-周次
weekTop12GrossHistory-近n年当周票房榜前12票房总和平均
weekOverallGrossHistory-近n年当周票房总和平均
weekTotalMoviesHistory-近n年当周电影总数平均
lastWeekTop12Gross-上周票房榜前12票房总和
lastWeekOverallGross-上周票房总和
lastWeekMovies-上周电影总数
lastWeekTop1Gross-上周票房冠军票房
lastWeekTop1WeekSpan-上周票房冠军已放映周数
相关链接：
https://www.boxofficemojo.com/weekend/?yr=2018&p=.htm
https://www.boxofficemojo.com/weekend/?view=wknd&wknd=1&sort=year&order=DESC&p=.htm



数据框架二
year-年份
week-周次
title-片名
starNum-明星数
director-是否名导演（0或1）
theater-上映影院数
weekendGross-本周末票房（目标变量）
相关链接：
https://www.boxofficemojo.com/people/?view=Actor&pagenum=1&sort=sumgross&order=DESC&&p=.htm
https://www.boxofficemojo.com/people/chart/?view=Actor&id=samuelljackson.htm
https://www.boxofficemojo.com/people/?view=Director&sort=sumgross&order=DESC&p=.htm
https://www.boxofficemojo.com/people/?view=Director&sort=sumgross&order=DESC&p=.htm
思路：对于名演员，先把前n位名演员对应链接抓下来，然后进入每个链接进一步抓取影片列表，抓下来的每部影片都要和一个演员组合成新的行
一部影片可以有多个名演员参演，对于名导演，同样先抓取前n位名导演对应的链接，然后进入链接抓取片名列表，此时片名列表无需与导演名绑定
因为我们只需要知道某部影片是不是名导演执导（0或1），但需要知道有几个名演员参演

数据框架三
year-年份
week-周次
title-片名
LW-上周排名
LWGross-上周票房
GrossTotal-到上周为止的票房总计
weekNum-上映周数
theater-上映影院数（本周）
weekendGross-本周末票房（目标变量）
相关链接：
https://www.boxofficemojo.com/weekend/chart/?yr=2019&wknd=42&p=.htm

2 