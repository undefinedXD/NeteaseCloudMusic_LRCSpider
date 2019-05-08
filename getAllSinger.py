# encoding : utf-8
import time
import os
import csv
import requests
import re
import pymysql
from bs4 import BeautifulSoup
from selenium import webdriver


def get_html_src(url):
    driver = webdriver.Chrome()
    driver.get(url)
    #切换frame
    driver.switch_to_frame("g_iframe")
    #waiting
    time.sleep(2)
    page_src = driver.page_source
    driver.close()
    return page_src


def parsebyre(page):
    lis = re.findall(
        r'href="\s?\/artist\?id=(\d*)"\sclass="nm\snm-icn\sf-thide\ss-fc0".*?>(.*?)<\/a>',
        page)
    return lis


def isSingerInDB(singer_id):
    try:
        #username,password是mysql用户名及密码，请自行填充，music163数据库名字 也可以自行改成别的库    
        db = pymysql.connect("localhost", "username", "password", "MUSIC163")    
        cursor = db.cursor()
        sql = """select * from SINGER_INFO"""
        cursor.execute(sql)
        results = cursor.fetchall()
        db.close()
        flag = 0
        for item in results:
            s_id = item[0]
            s_name = item[1]
            if (int(item[0]) == int(singer_id)):  #判断是否相等时候的条件最好变成同一类型
                print("该歌手信息已在库中")
                flag = 1
                return False
        if (not flag):
            print("该歌手信息入库成功")
            return True
    except:
        print("查询过程异常")
        return


def write_to_db(lis):
    #with open('singer.csv', 'a') as csvfile:
    #writer = csv.writer(csvfile)
    #for i in lis:
    #writer.writerow(i)
    #csvfile.close()
    for i in lis:
        #username,password是mysql用户名及密码，请自行填充，music163数据库名字 也可以自行改成别的库    
        db = pymysql.connect("localhost", "username", "password", "MUSIC163")
        cursor = db.cursor()
        try:
            sql = """INSERT INTO SINGER_INFO
                    values(%s,%s)"""
            isSingerInDB(i[0])
            if (not isSingerInDB(i[0])):
                continue
            cursor.execute(sql, (i[0], i[1]))
            db.commit()
            db.close()
        except:
            db.rollback()


def getkindsinger(root):
    for i in range(-1, 1):
        url = root + str(i)
        try:
            page = get_html_src(url)
            lis = parsebyre(page)
            write_to_db(lis)
        except:
            print("ERROR")
            continue
    for i in range(65, 91):
        url = root + str(i)
        try:
            page = get_html_src(url)
            lis = parsebyre(page)
            write_to_db(lis)
        except:
            continue


# https://music.163.com/#/discover/artist/cat?id=1002&initial=-1
# https://music.163.com/#/discover/artist/cat?id=1001&initial=1002&initial=-1
# 每遍循环没有初始化root导致的问题


def main():
    for i in range(1001, 1004):
        root = 'https://music.163.com/#/discover/artist/cat?id='
        root = root + str(i) + '&initial='
        getkindsinger(root)


main()