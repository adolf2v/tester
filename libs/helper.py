#!-*- coding:utf-8 -*-
"""
    __author__='Created by xiaoqiang'
    Date:2017/4/6
    Name:helper
"""
import hashlib
import sys
import json

reload(sys)
sys.setdefaultencoding('utf-8')


# handler的helper类
class handlerHelper(object):
    def reply_json_data(self, code=0, detail=None, hashcode=None):
        if hashcode is None:
            hashcode = self.get_argument('hashcode', '0')
        self.reply_json(code, detail, hashcode)

    def reply_json_error(self, errcode=1, errmsg=None):
        self.reply_json(errcode, errmsg)

    def reply_json(self, code=0, detail=None, hashcode=None):
        self.set_header('Content-Type', 'application/json')
        if detail is None:
            detail = {}
        if hashcode:
            new_hashcode = hashlib.md5(
                str(detail).encode('utf-8')).hexdigest()
            if new_hashcode == hashcode:
                self.set_status(304)
                return
            else:
                hashcode = new_hashcode
        else:
            hashcode = '0'

        respone_data = {}
        respone_data['code'] = code
        respone_data['detail'] = detail
        respone_data['hashcode'] = hashcode
        data = json.dumps(respone_data, encoding='utf-8', ensure_ascii=True)
        self.write(data)
        self.finish()
