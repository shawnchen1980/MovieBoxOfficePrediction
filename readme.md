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
<p>数据框架一</p>
<ul>
<li>year-年份</li>
<li>week-周次</li>
<li>weekTop12GrossHistory-近n年当周票房榜前12票房总和平均</li>
<li>weekOverallGrossHistory-近n年当周票房总和平均</li>
<li>weekTotalMoviesHistory-近n年当周电影总数平均</li>
<li>lastWeekTop12Gross-上周票房榜前12票房总和</li>
<li>lastWeekOverallGross-上周票房总和</li>
<li>lastWeekMovies-上周电影总数</li>
<li>lastWeekTop1Gross-上周票房冠军票房</li>
<li>lastWeekTop1WeekSpan-上周票房冠军已放映周数</li>
</ul>
相关链接：
https://www.boxofficemojo.com/weekend/by-year/2018/（最新链接）
https://www.boxofficemojo.com/weekend/?yr=2018&p=.htm（已过期）
https://www.boxofficemojo.com/weekend/?view=wknd&wknd=1&sort=year&order=DESC&p=.htm（已过期）
<p>
思路：根据最新链接可以获取某一年每一周的票房概况，还可以获得某一年每一周票房具体情况页面的链接，先用最新链接抓取2008-2019
近十年的所有周末票房概况数据，同时抓取每一周具体票房的链接，结果保存到years.csv文件中，然后对节假日周次的数据进行人肉清洗，
（数据中对于假日周末会计算两次，需要把重复的票房数据去除）,然后针对csv文件中留下的每周详情链接进一步抓取数据，获得每周票房冠军
相关的数据，至此我们可以获得数据包括（年份，周次，本周前十票房总和，本周票房总和，本周上映数，本周票房冠军票房，本周票房冠军已放映周数）
接下来用pandas.DataFrame.shift和join即可
</p>



<p>数据框架二</p>
<ul>
<li>year-年份</li>
<li>week-周次</li>
<li>title-片名</li>
<li>starNum-明星数</li>
<li>director-是否名导演（0或1）</li>
<li>theater-上映影院数</li>
<li>weekendGross-本周末票房（目标变量）</li>
</ul>
有效链接：
https://www.boxofficemojo.com/year/2019/?ref_=bo_yl_table_1

相关链接：(以下链接已经全部失效)
https://www.boxofficemojo.com/people/?view=Actor&pagenum=1&sort=sumgross&order=DESC&&p=.htm
https://www.boxofficemojo.com/people/chart/?view=Actor&id=samuelljackson.htm
https://www.boxofficemojo.com/people/?view=Director&sort=sumgross&order=DESC&p=.htm
https://www.boxofficemojo.com/people/?view=Director&sort=sumgross&order=DESC&p=.htm

思路：对于名演员，先把前n位名演员对应链接抓下来，然后进入每个链接进一步抓取影片列表，抓下来的每部影片都要和一个演员组合成新的行
一部影片可以有多个名演员参演，对于名导演，同样先抓取前n位名导演对应的链接，然后进入链接抓取片名列表，此时片名列表无需与导演名绑定
因为我们只需要知道某部影片是不是名导演执导（0或1），但需要知道有几个名演员参演
新思路：从目前有效链接入手把每一年所有影片的链接先抓下来，然后从每一个链接入手进一步抓取imdb链接，再进入imdb页面抓取该影片卡司阵容
可参考scrape.py文件中的getWeekendDataByYear和getWeekendDataByYears两个函数
<p>数据框架三</p>
<ul>
<li>year-年份</li>
<li>week-周次</li>
<li>title-片名</li>
<li>LW-上周排名</li>
<li>LWGross-上周票房</li>
<li>GrossTotal-到上周为止的票房总计</li>
<li>weekNum-上映周数</li>
<li>theater-上映影院数（本周）</li>
<li>weekendGross-本周末票房（目标变量）</li>
</ul>
相关链接：
https://www.boxofficemojo.com/weekend/chart/?yr=2019&wknd=42&p=.htm

2 画图
a 画一年当中每周的票房平均与影片数平均分布图

3 对论文中上面用到的特征数据进行描述

4 完成查新报告

email:chenxiao@sincereedu.com

