# -*- coding: UTF-8 -*-
u'''用来把所有的测试的class装载到suite，并执行测试'''
import sys
import unittest
import os
import re
from testLogin import testLogin
from testXuetuan import testXuetuan
from testCourse import testCourse
from testChannel import testChannel
from testxuetuanPull import testXuetuanPull
from testSms import testSms
from testP2P import testP2P
from testOpenChannel import testOpenChannel
from Utils import HTMLTestRunner
from testForum import testForum
import platform
import time
from testOpenChannelPull import testOpenChannelPull

reload(sys)
sys.setdefaultencoding("utf-8")
import SendMail

if __name__ == "__main__":
    # 获取操作系统的类型,windows or linux
    osType = platform.system()
    # 声明测试套
    suite1 = unittest.TestLoader().loadTestsFromTestCase(testLogin)
    suite2 = unittest.TestLoader().loadTestsFromTestCase(testXuetuan)
    # 组装测试套件
    suite = unittest.TestSuite([suite1, suite2])
    # 命名一个文件
    filename = time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time()))
    print filename
    if (osType == 'Windows'):
        file1 = r"E:\\xiaoqiang.html"
        fp = file(file1, 'wb')
    else:
        os.getcwd()
        resultFile = os.getcwd() + '/results/%s.html' % filename
        print resultFile
        fp = file(resultFile, 'wb')
    # 利用HTMLTestRunner来声明一个runner
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u'Auto Report', description=u'用例执行情况：')
    # 运行测试
    runner.run(suite)
    fp.close()
    # 下边发送邮件给人,将测试报告当做附件进行发送
    with open(resultFile, 'rb') as fb:
        text2 = fb.read()
    server = {'name': 'smtp.163.com', 'user': 'liuweiqiang3v@163.com', 'passwd': '521426'}
    sm = SendMail
    sm.send_mail(server, 'liuweiqiang3v@163.com', ['liuwq@tupo.com'], 'nihao', u'测试报告来了，敬请关注', text2, [resultFile])
    # sendhtml(server,'liuweiqiang3v@163.com',['liuwq@tupo.com'],'nihao','测试报告来了，关注')
