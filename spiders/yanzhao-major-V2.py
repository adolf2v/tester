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
from pre_major import PreMajor
from major import Major

reload(sys)
sys.setdefaultencoding('utf8')

queryurl = 'http://yz.chsi.com.cn/zsml/querySchAction.do'
reqdata = {"mldm": "", "mlmc": u"--选择门类--", "yjxkdm": "", "zymc": ""}
parrten = re.compile(r"\('(.*)',")


def get_page():
    for item in PreMajor.select():
        print item.id
        print item.newUrl
        res = requests.get('http://yz.chsi.com.cn' + item.newUrl, timeout=50)
        pagebs = BeautifulSoup(res.text, "lxml")
        total = pagebs.select('#page_total')
        if total:
            num = total[0].text.split('/')[1]
            print num
            item.set(pageNum=int(num))


def get_content():
    for item in PreMajor.select(PreMajor.q.id >= 785):
        print item.id
        reqdata['ssdm'] = item.cityCode
        reqdata['dwmc'] = item.schoolName
        for pageno in xrange(1, item.pageNum + 1):
            reqdata['pageno'] = pageno
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
                u = Major.select(Major.q.url == newurl)
                if not u.count():
                    o = Major(city=item.city, cityCode=item.cityCode, schoolName=item.schoolName,
                              schoolCode=item.schoolCode, college=college[5:], collegeCode=college[1:4],
                              major=major[8:],
                              majorCode=major[1:7], direction=direction[4:], directionCode=direction[1:3],
                              peopleNum=peoplenum, fanwei="", url=newurl)
                    if o:
                        print("ok")
                    else:
                        print("failed")
    print("it's over")


def get_scope():
    url = 'http://yz.chsi.com.cn'
    try:
        con = MySQLdb.connect(host='localhost', passwd='123456', db='kaoyan', charset='utf8', user='root')
        cursor = con.cursor()
        cursor.execute('select startid from tableid where id =1')
        startid = cursor.fetchone()[0]
        print("start id is %s" % startid)
        for item in Major.select(Major.q.id >= startid):
            aa = ""
            print "item id is ", item.id
            if not item.fanwei:
                res = requests.get(url + item.url, timeout=50)
                soup = BeautifulSoup(res.text, 'html.parser')
                res2 = soup.select('#result_list table tbody tr')
                for item2 in res2:
                    bb = ""
                    for item3 in item2.select('td')[1:]:
                        bb = bb + item3.text + "|"
                    aa = aa + bb + "|"
                print aa
            item.set(fanwei=aa)
            cursor.execute('update tableid set startid = %d where id =1 ' % item.id)
            con.commit()
    except requests.exceptions.Timeout as e:
        # print str(e)
        get_scope()
    finally:
        cursor.close()
        con.close()

if __name__ == "__main__":
    get_scope()
