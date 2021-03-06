#!-*- coding:utf-8 -*-
"""
    __author__='Created by xiaoqiang'
    Date:2017/3/20
    Name:book
"""
from tornado.log import app_log
import sys
import tornado
from models.book import Book
from Utils.wrapper import login
from libs.helper import handlerHelper
from tornado.log import app_log

class BookHandler(tornado.web.RequestHandler, handlerHelper):
    # 获取书籍
    @login
    def get(self):
        self.render('book.html')
        # bid = self.get_argument('bookid', None)
        # if not bid:
        #     self.write(u'此书不存在')
        #     return
        # else:
        #     pass

    def post(self):
        action = self.get_argument("action", None)
        action_func = {
            "add": self.add,
        }
        func = action_func.get(action, None)
        if func:
            func()
        else:
            self.reply_json_error(1, u"参数错误")

    # 添加书籍
    @login
    def add(self):
        name = self.get_argument('bookname', None)
        source = self.get_argument('source', None)
        author = self.get_argument('author', None)
        price = float(self.get_argument('price', 0))
        upload = int(self.get_secure_cookie('sign'))
        breif = self.get_argument('breif', None)
        if not name or not source or not author:
            self.reply_json_error(1, u'请填写书名,来源或者作者')
            return
        b = Book.select(Book.q.bookName == name).count()
        if b:
            self.reply_json_error(1, u'本书已经存在,请勿重复添加')
            return
        try:
            book = Book(bookName=name, source=source, author=author, uploadUser=upload, price=price, bookDesc=breif)
            if book:
                self.reply_json_data(0, u'书籍添加成功')
                return
            else:
                self.reply_json_error(1, u'书籍添加失败!')
                return
        except Exception as e:
            app_log.error(str(e))
