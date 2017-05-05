#!coding:utf-8
import xlrd
import sys
import xlsxwriter
import requests
from bs4 import BeautifulSoup
import re
import csv
import codecs
import lxml
import MySQLdb

reload(sys)
sys.setdefaultencoding('utf8')
workbook = xlrd.open_workbook('demo.xlsx')
sheet = workbook.sheet_by_index(0)
row = sheet.nrows

queryurl = 'http://yz.chsi.com.cn/zsml/querySchAction.do'
reqdata = {"mldm": "", "mlmc": u"--选择门类--", "yjxkdm": "", "zymc": ""}
parrten = re.compile(r"\('(.*)',")
# count = 0
with open('major2.csv', 'wb') as csvfile:
    csvfile.write(codecs.BOM_UTF8)
    csvwriter = csv.writer(csvfile, dialect='excel')
    for item in range(0, row + 1):
        print "this is the %s" % item
        url = sheet.cell(item, 4).value
        city = sheet.cell(item, 0).value
        citycode = sheet.cell(item, 1).value
        schoolname = sheet.cell(item, 2).value
        schoolcode = sheet.cell(item, 3).value
        reqdata['ssdm'] = citycode
        reqdata['dwmc'] = schoolname
        print 'http://yz.chsi.com.cn' + url
        res = requests.get('http://yz.chsi.com.cn' + url, timeout=50)

        pagebs = BeautifulSoup(res.text, "lxml")
        total = pagebs.select('#page_total')
        if total:
            num = total[0].text.split('/')[1]
            print num
        for item2 in range(1, int(num) + 1):

            reqdata['pageno'] = item2
            # print reqdata
            res2 = requests.post(queryurl, data=reqdata, timeout=50)
            soup = BeautifulSoup(res2.text, 'lxml')
            res3 = soup.select('#sch_list table tbody tr')
            for item3 in res3:
                college = item3.contents[1].text
                major = item3.contents[3].text
                direction = item3.contents[5].text
                people = item3.contents[9].text
                peoplenum = parrten.findall(people)[0]
                newurl = item3.contents[11].a['href']
                rowcontent = []
                rowcontent.append(city)
                rowcontent.append(citycode)
                rowcontent.append(schoolname)
                rowcontent.append(schoolcode)
                rowcontent.append(college[5:])
                rowcontent.append(college[1:3])
                rowcontent.append(major[8:])
                rowcontent.append(major[1:6])
                rowcontent.append(direction[4:])
                rowcontent.append(direction[1:3])
                rowcontent.append(peoplenum)
                res4 = requests.get('http://yz.chsi.com.cn' + newurl, timeout=50)
                soup4 = BeautifulSoup(res4.text, 'html.parser')
                res5 = soup4.select('#result_list table tbody tr')
                fanwei = ""

                rowcontent.append(fanwei)
                csvwriter.writerow(rowcontent)
