#!coding:utf-8
from sqlobject import connectionForURI, sqlhub
from sqlobject.mysql import builder
from tornado.options import options

# 初始化一个数据的连接,用来在models中传递连接,加上编码,要不可能会报未知的错误
conn = builder()(user='root', password='123456', host='localhost', db='kaoyan', charset='utf8')
