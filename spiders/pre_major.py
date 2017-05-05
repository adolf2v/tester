#!-*- coding:utf-8 -*-
"""
    __author__='Created by xiaoqiang'
    Date:2017/3/13
    Name:
"""
from sqlobject import SQLObject, StringCol, DateTimeCol, DecimalCol, IntCol
import datetime

from Utils.connection import conn


# 书的类
class PreMajor(SQLObject):
    _connection = conn
    # debug
    # _connection.debug = True
    city = StringCol(notNone=True)
    cityCode = IntCol(notNone=True)
    schoolName = StringCol(length=50, notNone=True)
    schoolCode = IntCol(notNone=True)
    newUrl = StringCol(notNone=True)
    pageNum=IntCol(notNone=True)
