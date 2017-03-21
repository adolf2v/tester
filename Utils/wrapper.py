#!-*- coding:utf-8 -*-
"""
    __author__='Created by xiaoqiang'
    Date:2017/3/13
    Usage:用来判断用户是否登录
"""
import sys
from models.login import LoginStatus

reload(sys)
sys.setdefaultencoding('utf-8')


def login(func):
    def wrapper(self, *args, **kwargs):
        mobile = self.get_secure_cookie('sign')
        salt = self.get_secure_cookie('login')
        if not mobile or not salt:
            self.redirect('/login')
            return
        ls = LoginStatus.select(LoginStatus.q.mobile == mobile).getOne()
        if ls.status != 1:
            self.redirect('/login')
            return
        return func(self, *args, **kwargs)

    return wrapper
