#!-*- coding:utf-8 -*-
"""
    __author__='Created by xiaoqiang'
    Date:2017/3/20
    Name:spider
"""
import sys
import requests
import time
from lxml import etree
# from models.bookcontent import BookContent
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

url = 'http://www.doupocangqiong1.com/1/'
res = requests.get(url)

# bs = BeautifulSoup(res.text, 'lxml')
# # .通过类名查找,#通过id查找,>查找子元素
# soup = bs.select('.body ' )
# for item in soup:
#     print item
#     exit(111)
selector = etree.HTML(res.text)
# /html/body/section/div[3]/div[2]/ul/li[1]/a
# 通过xpath来获取元素
links = selector.xpath('/html/body/section/div[3]/div[2]/ul/li/a')
bookid=1
i=0
for link in links:
    churl= link.attrib['href']
    name=link.text
    print name
    chapterId=churl.split('/')[2].split('.')[0]
    print chapterId
    res2=requests.get('http://www.doupocangqiong1.com'+churl)
    time.sleep(5)
    soup=BeautifulSoup(res2.text,'lxml')
    content=soup.select('#chaptercontent')
    for item in content:
        print item
    i+=1
    if i>10:
        exit(111)

