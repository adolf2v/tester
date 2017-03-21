#!-*- coding:utf-8 -*-
"""
    __author__='Created by xiaoqiang'
    Date:2017/3/20
    Name:bookcontent
"""
import sys
from Utils.connection import conn
from sqlobject import SQLObject, IntCol, StringCol, DateTimeCol
from datetime import datetime

reload(sys)
sys.setdefaultencoding('utf-8')


# 书的章节内容类
class BookContent(SQLObject):
    _connection = conn
    bookId = IntCol(default=0)
    chapterId = IntCol(default=0)
    chapterName = StringCol(length=100)
    content = StringCol()
    created_at = DateTimeCol(default=datetime.now())
    updated_at = DateTimeCol(default=datetime.now())
