#!coding:utf-8
import tornado
from models.user import User
from libs.helper import handlerHelper


class UserHandler(tornado.web.RequestHandler, handlerHelper):
    def get(self):
        uid = self.get_argument('id', None)
        if not uid:
            self.reply_json_error(1, u'参数错误')
            return
        try:
            u = User.get('uid')
            if not u:
                self.reply_json_error(1, u'用户不存在')
                return
            self.write(u)
        except Exception as e:
            print str(e)

    # 暂时没有完成的修改用户类,和密码重置
    def post(self):
        action = self.get_argument("action", None)
        action_func = {
            "update": self.update_profile,
            "resetpasswd": self.resetpasswd,
        }
        func = action_func.get(action, None)
        if func:
            func()
        else:
            self.reply_json_error(1, u"参数错误")

    def update_profile(self):
        pass

    def resetpasswd(self):
        pass
