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
<p>frame1.csv</p>
<ul>
<li>Year-年份</li>
<li>Week-周次</li>
<li>Releases-本周上映片数</li>
<li>wT10Gross-历史本周前十票房平均</li>
<li>wRelease-历史本周影片数平均</li>
<li>lGross-上周票房冠军票房</li>
<li>lTGross-上周票房冠军累计票房</li>
<li>lWeeks-上周票房冠军累计放映周数</li>
<li>lTop 10 Gross-上周票房前十票房</li>
<li>lOverall-上周总票房</li>
<li>lastWeekTop1WeekSpan-上周票房冠军已放映周数</li>
<li>["Year","Week","Releases","wT10Gross","wRelease","lGross","lTGross","lWeeks","lTop 10 Gross","lOverall"]</li>
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
关于groupby:https://pandas.pydata.org/pandas-docs/stable/user_guide/groupby.html
</p>



<p>数据框架二</p>
<p>frame2.csv</p>
<ul>
<li>year_x-上映年份</li>
<li>week-上映周次</li>
<li>Release-片名</li>
<li>Distributor-发行商</li>
<li>Theaters-上映影院数</li>
<li>t100-排名100内演员数</li>
<li>t500-排名500内演员数</li>
<li>t5k-排名5k内演员数</li>
<li>mem-其他演员数</li>
<li>Gross_x-本周末票房（目标变量）</li>
<li>["year_x","week","Release","Distributor","Theaters","t100","t500","t5k","mem","Gross_x"]</li>
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
<p>frame3.csv</p>
<ul>
<li>year_y-影片上映年份</li>
<li>week_y-影片上映周次</li>
<li>Release-片名</li>
<li>Distributor-发行商</li>
<li>Rank_x-上周排名</li>
<li>Theaters_x-上周上映影院数</li>
<li>Theaters_y-本周上映影院数</li>
<li>Gross_x-上周票房</li>
<li>Total Gross_x-到上周为止的票房总计</li>
<li>Weeks_y-本周上映周数（>1）</li>
<li>Gross_y-本周票房（目标变量）</li>

</ul>
相关链接：
https://www.boxofficemojo.com/weekend/chart/?yr=2019&wknd=42&p=.htm

2 画图
a 画一年当中每周的票房平均与影片数平均分布图

3 对论文中上面用到的特征数据进行描述

4 完成查新报告

email:chenxiao@sincereedu.com

