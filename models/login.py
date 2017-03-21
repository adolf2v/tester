#!coding:utf-8
from Utils.connection import conn
from sqlobject import *
from datetime import datetime

# 登录状态的类
class LoginStatus(SQLObject):
    _connection = conn
    mobile = StringCol(length=11, notNone=True, unique=True)
    status = BoolCol(default=False)
    login_time = DateTimeCol(default=datetime.now())
    ip = StringCol(length=16, notNone=True)
