#!coding:utf-8
import tornado
from models.user import User
from tornado.log import app_log
import hashlib
import sys
from datetime import datetime
from models.login import LoginStatus
from libs.helper import handlerHelper

reload(sys)
sys.setdefaultencoding('utf-8')


class LoginHandler(tornado.web.RequestHandler, handlerHelper):
    # 返回登录的html页面
    def get(self):
        self.render('login.html')

    # 用户进行登录和退出的post接口
    def post(self):
        action = self.get_argument('action', None)
        action_mapping = {
            "login": self.login,
            "logout": self.logout,
        }
        func = action_mapping.get(action, None)
        app_log.error("action is %s" % action)
        if func:
            func()
            return
        else:
            self.reply_json_error(1000, u'参数错误')
            return

    def logout(self):
        mobile = self.get_secure_cookie('sign')
        if not mobile:
            self.reply_json_error(1, u'用户不存在')
            self.redirect('/login')
            return
        # 查询用户的登录状态
        ls = LoginStatus.select(LoginStatus.q.mobile == mobile)
        if not ls.count():
            self.reply_json_error(1, u'用户不存在')
            self.redirect('/login')
            return
        ls.getOne().set(status=0)
        self.clear_cookie('login')
        self.clear_cookie('sign')
        self.redirect('/login')
        return

    def login(self):
        mobile = self.get_argument('mobile', None).strip()
        password = self.get_argument('password', None).strip()
        if not mobile or not password:
            self.reply_json_error(1, u'用户名或者密码不能为空')
            self.redirect('/login')
            return
        try:
            u = User.select(User.q.mobile == mobile)
            if not u.count():
                self.reply_json_error(1, u"该手机号未注册")
                return
            user = u.getOne()
            salt = user.salt
            passwd = user.password
            m = hashlib.md5()
            m.update(password + salt)
            hashpassword = m.hexdigest()
            if not passwd == hashpassword:
                self.reply_json_error(1, u"手机号或者密码不正确")
                return
            ls = LoginStatus.select(LoginStatus.q.mobile == mobile)
            app_log.error(ls)
            if not ls.count():
                lls = LoginStatus(mobile=mobile, status=1, ip=self.request.remote_ip)
                if lls:
                    self.reply_json_data(0, u'登录成功')
            if ls.getOne().status == 1:
                self.reply_json_error(1, u'用户已经登录')
                self.redirect('/book')
                return
            else:
                ls.getOne().set(status=1, login_time=datetime.now(), ip=self.request.remote_ip)
            self.set_secure_cookie("sign", mobile, version=2, expires_days=1)
            self.set_secure_cookie("login", salt, version=2, expires_days=1)
            self.redirect('/book')
            return
        except Exception as e:
            app_log.error(str(e))
