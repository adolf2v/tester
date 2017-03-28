#!-*- coding:utf-8 -*-
"""
    __author__='Created by xiaoqiang'
    Date:2017/3/20
    Name:spider
    three ways to parse html and get the content what you want .
    以http://www.54qa.cn/forum.php?gid=1为例子,抓取本站最新的10个主题
    需要自己安装requests,BeautifulSoup和lxml的库
"""
import sys
import requests
import time
from lxml import etree
import re
# from models.bookcontent import BookContent
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')
# 要抓取内容的网址
url = 'http://www.54qa.cn/forum.php?gid=1'
res = requests.get(url)
# 通过BeautifulSoup来获取想要的元素
bs = BeautifulSoup(res.text, 'lxml')
# .通过类名查找,#通过id查找,>查找子元素
# 根据给定的条件返回了相应元素的集合,本处是一个list,查找出了最新主题的10个帖子
soup = bs.select('.category_l2 > div > ul > li > a')
# 遍历返回的结果
print u"通过BeaufitulSoup来获取想要的元素"
for item in soup:
    print "title is :" + item.text
    # attrs是该元素属相的集合,一个字典类型
    print "url is :http://www.54qa.cn/" + item.attrs['href']
    print "\n" * 2

# 通过lxml的xpath来获取
# 将返回的结果通过etree转为html
selector = etree.HTML(res.text)
# 通过xpath来获取元素
# xpath://td[@class="category_l2"]/div/ul/li/a
# //从任意位置开始查找,/从dom的根元素开始查找
links = selector.xpath('//td[@class="category_l2"]/div/ul/li/a')
print u"通过xpath查找元素"
for link in links:
    print "title is :" + link.text
    # 该次返回的link的属性为attrib,也是一个字典类型
    print "url is :http://www.54qa.cn/" + link.attrib['href']
    print "\n" * 2

# 通过正则表达式来获取想要的元素
# 构建正则表达式,获取一个分组,然后对分组进行处理
# 预编译,使用已编译表达式的另一个好处是，通过在加载模块时预编译所有表达式，可以把编译工作转到应用开始时，而不是当程序响应一个用户动作时才进行编译。
patern = re.compile(r'<li><a href=(.*)target')
links = patern.findall(res.text)
print u"通过正则表达式来获取需要的内容"
for link in links:
    # 此处排除掉最新回复的内容,但是里边还包含热帖的数据,可以通过分割link来过滤,是list是有顺序,读者可自行实现此处不再实现
    if not "lastpost" in link:
        # 一下的re正则表达式没有进行预编译
        print 'title is :' + re.findall(r'<strong>(.*)</strong>', link)[0]
        print 'url is :http://www.54qa.cn/' + re.findall(r'"(.*);extra', link)[0]

