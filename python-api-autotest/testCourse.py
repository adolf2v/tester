# -*- coding: UTF-8 -*-

import unittest
import requests


class testCourse(unittest.TestCase):
    # 测试前的准备工作
    def setUp(self):
        pass

    # 测试用例
    def test_a_Add(self):
        # 进行操作,并对返回的结果进行验证
        pass

    # 上传多媒体图片
    def uploadPic(self):
        # 以下是示例
        multiple_part = [('file1', ('gitflow.jpg', open('img/gitflow.jpg', 'rb'), 'application/octet-stream'))]
        return requests.post(Url, files=multiple_part, timeout=10)

    # 上传多媒体的声音
    def uploadVoice(self):
        multiple_part = [('file1', ('voice.mp3', open('voice/voice.mp3', 'rb'), 'application/octet-stream'))]
        return requests.post(Url, files=multiple_part, timeout=10)

    # 收尾工作
    def tearDown(self):
        pass


# 单独运行本文件的用例
if __name__ == '__main__':
    unittest.main()
