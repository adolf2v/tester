#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
import os
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


# server['name'], server['user'], server['passwd']
def send_mail(server, fro, to, subject, content, files=[]):
    """
    server:字典类型,发件人的邮件服务相关信息
    fro:发件人的邮件地址
    to:list类型,收件人列表
    subject:邮件标题
    content:html的内容,做成正文,可以快速预览一把
    files:list类型,邮件附件
    """
    # 判断server是否是字典类型
    assert type(server) == dict
    # 判断收件人是不是一个列表
    assert type(to) == list

    # 实例化一个多媒体的类
    msg = MIMEMultipart()
    # 设置编码
    msg.set_charset('UTF-8')
    # 设置发件人
    msg['From'] = fro
    # 设置主题
    msg['Subject'] = subject
    # 设置收件人
    msg['To'] = COMMASPACE.join(to)
    # 设置时间
    msg['Date'] = formatdate(localtime=True)
    # MIMEText('中文', _charset='UTF-8')
    # 正文的内容
    msgtext = MIMEText("""%s""" % content, 'html', 'UTF-8')
    # 添加正文内容
    msg.attach(msgtext)
    # 遍历附件,并进行添加
    for file in files:
        part = MIMEBase('application', 'multipart/mixed')  # 'octet-stream': binary data
        part.set_payload(content)
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
    msg.attach(part)
    import smtplib
    smtp = smtplib.SMTP(server['name'])
    smtp.login(server['user'], server['passwd'])
    smtp.sendmail(fro, to, msg.as_string())
    smtp.close()
    print 'the email has been send'


if __name__ == "__main__":
    server = {'name': 'smtp.163.com', 'user': 'liuweiqiang3v@163.com', 'passwd': 'xxxxxxx'}
    with open("result.html", "rb") as fb:
        content = fb.read()
        send_mail(server, 'liuweiqiang3v@163.com', ['xxxxx@xxxxx.com'], u'测试报告,详情请见附件', content, files=["result.html"])
