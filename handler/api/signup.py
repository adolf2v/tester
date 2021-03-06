#!coding:utf-8
from handler.api.user import User
import datetime
import hashlib
import tornado
import random
import string
from libs.helper import handlerHelper
from tornado.log import app_log

# 注册的handler类
class SignUpHandler(tornado.web.RequestHandler, handlerHelper):
    def get(self):
        # 向日志中添加info级别的log
        app_log.info("xxxxxxx")
        self.render('signup.html')

    # 注册的接口
    def post(self):
        mobile = self.get_argument('mobile', None).strip()
        exists = User.select(User.q.mobile == mobile).count()
        if exists:
            self.reply_json_error(1, u'用户已存在')
            return
        name = self.get_argument('username', None)
        password1 = self.get_argument('password1', None)
        password2 = self.get_argument('password2', None)
        if len(password1) < 6 or len(password1) > 20:
            self.reply_json_error(1, u'密码长度不符合规范')
            return
        sex = int(self.get_argument('sex', 1))
        ip = self.request.remote_ip
        if not mobile or not name or not password1 or not password2:
            self.reply_json_error(1, u'必填参数不全')
            return
        if password1 != password2:
            self.reply_json_error(1, u'两次密码不一致')
            return
        # random.sample(sequence,k) 从指定序列中随机获取指定长度的片断。sample函数不会修改原有序列
        g = lambda a: "".join(random.sample(string.letters, a))
        # 获取一个6位大写字母的salt,用来和密码一起进行md5
        salt = g(6).upper()
        m = hashlib.md5()
        m.update(password2 + salt)
        passwd = m.hexdigest()
        created_at = datetime.datetime.now()
        try:
            u = User(mobile=mobile, username=name, password=passwd, salt=salt, sex=sex, created_at=created_at, ip=ip)
            if u:
                self.reply_json_data(0, u"注册成功")
                self.redirect('/login')
                return
        except Exception as e:
            print str(e)
