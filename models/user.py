#!coding:utf-8
from Utils.connection import conn
from sqlobject import *
import datetime

#  用户类
class User(SQLObject):
    _connection = conn
    username = StringCol(length=30, notNone=True)
    mobile = StringCol(length=11, unique=True, notNone=True)
    password = StringCol(length=100, notNone=True)
    sex = IntCol(default=1)
    salt = StringCol(length=6, notNone=True)
    created_at = DateTimeCol(default=datetime.datetime.now())
    ip = StringCol(length=16, default=None)
    updated_at = DateTimeCol(default=datetime.datetime.now())


if __name__ == '__main__':
    u = User.get(1)
    print u
