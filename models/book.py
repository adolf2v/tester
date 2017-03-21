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
class Book(SQLObject):
    _connection = conn
    # debug
    # _connection.debug = True
    bookDesc = StringCol(notNone=False)
    bookName = StringCol(length=100, unique=True, notNone=True)
    source = StringCol(length=50, notNone=True)
    author = StringCol(length=50, notNone=True)
    uploadUser = IntCol(length=10)
    created_by = DateTimeCol(notNone=False, default=datetime.datetime.now())
    update_by = DateTimeCol(notNone=False, default=datetime.datetime.now())
    price = DecimalCol(size=5, precision=2)
