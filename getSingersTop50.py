# encoding : utf-8
import time
import re
import pymysql
from bs4 import BeautifulSoup
from selenium import webdriver

def getsingerID(singer_name):
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
            if (item[1] == singer_name):
                return item[0]
                flag = 1
        if (not flag):
            print("库中查无此人")
            return "NULL_rsa"
    except:
        print("查询过程异常")


def getsinger_profile(singer_ID):
    root = 'https://music.163.com/#/artist?id='
    purl = root + str(singer_ID)
    driver = webdriver.Chrome()
    driver.get(purl)
    #切换frame
    driver.switch_to_frame("g_iframe")
    #waiting
    time.sleep(3)
    page_src = driver.page_source
    driver.close()
    return page_src


def parsesinger_song(page, singer_name):
    soup = BeautifulSoup(page, 'lxml')
    lis = soup.select('.txt')
    dist = []
    for i in lis:
        distp = [0, 0, 0]
        passli = re.findall(r'<a href="\/song\?id=(\d*)"><b title="(.*?)">',
                            str(i))
        distp[0] = passli[0][0]
        distp[1] = passli[0][1]
        distp[2] = singer_name
        dist.append(distp)
    return dist


def write_to_db(lis):
    #with open('song.csv', 'a') as csvfile:
    #writer = csv.writer(csvfile)
    #for i in lis:
    #writer.writerow(i)
    #csvfile.close()
    for i in lis:
        #username,password是mysql用户名及密码，请自行填充，music163数据库名字 也可以自行改成别的库    
        db = pymysql.connect("localhost", "username", "password", "MUSIC163")        
        cursor = db.cursor()
        try:
            sql = """INSERT INTO SONG_INFO
                    values(%s,%s,%s)"""
            cursor.execute(sql, (i[0], i[1], i[2]))
            db.commit()
            db.close()
        except:
            db.rollback()


def main():
    singer_name = input("请输入歌手名字：")
    singer_id = getsingerID(singer_name)
    if (singer_id != "NULL_rsa"):
        page = getsinger_profile(singer_id)
        dist = parsesinger_song(page, singer_name)
        write_to_db(dist)
        print("该歌手热门歌曲已入库成功")
    else:
        pass


while (1):
    main()