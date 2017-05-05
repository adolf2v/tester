#!coding:utf-8
import pickle
import requests
from bs4 import BeautifulSoup
import os
import xlsxwriter
import xlwt
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# 各地区的code和名称
zone = ["11:北京市", "12:天津市", "13:河北省", "14:陕西省", "15:内蒙古自治区", "21:辽宁省", "22:吉林省", "23:黑龙江省", "31:上海市", "32:江苏省",
        "33:浙江省", "34:安徽省", "35:福建省", "36:江西省", "37:山东省", "41:河南省", "42:湖北省", "43:湖南省", "44:广东省", "45:广西壮族自治区",
        "46:海南省", "50:重庆市", "51:四川省", "52:贵州省", "53:云南省", "54:西藏自治区", "61:陕西省", "62:甘肃省", "63:青海省", "64:宁夏回族自治区",
        "65:新疆维吾尔自治区"]
# 请求的url
url = "http://yz.chsi.com.cn/zsml/queryAction.do"
# 请求的数据
reqdata = {}
workbook = xlsxwriter.Workbook('demo.xlsx')
worksheet = workbook.add_worksheet()
count = 0
for item in zone:
    city = item.split(':')[1]
    ssdm = item.split(':')[0]
    reqdata['ssdm'] = ssdm
    res = requests.post(url, data=reqdata)
    pagebs = BeautifulSoup(res.text, "html.parser")
    total = pagebs.select('#page_total')
    if total:
        num = total[0].text.split('/')[1]

    for item2 in range(1, int(num) + 1):
        reqdata['pageno'] = item2
        print(reqdata)
        res2 = requests.post(url, data=reqdata)
        soup = BeautifulSoup(res2.text, 'html.parser')
        res3 = soup.select('#sch_list table tbody tr td form a')
        if not res3:
            continue
        for item3 in res3:
            newurl = item3['href']
            name = item3.text
            schoolcode = name[1:6]
            schoolname = name[7:]
            worksheet.write(count, 0, city)
            worksheet.write(count, 1, ssdm)
            worksheet.write(count, 2, schoolname)
            worksheet.write(count, 3, schoolcode)
            worksheet.write(count, 4, newurl)
            count += 1
workbook.close()
