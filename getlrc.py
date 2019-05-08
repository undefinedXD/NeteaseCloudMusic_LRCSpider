# encoding : utf-8
import time
import re
import requests
import json
import pymysql
import random
from lrc_clean import lrc_clean_function

# lrc接口
# 反爬虫措施：封IP
# TODO 2019/06/06 代理IP池


def getsong_page(song_id):
    url = 'https://music.163.com/api/song/lyric?id=' + str(
        song_id) + '&lv=1&kv=1&tv=-1'

    USER_AGENT = random.choice([
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1"
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36"
    ])
    header = {'USER_AGENT': USER_AGENT}

    try:
        r = requests.get(url, headers=header)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
        time.sleep(3)
    except:
        print("获取歌词过程出错")


# json处理⭐️
def parse_lrc(page, song_id):
    try:
        jsonF = page
        j = json.loads(jsonF)
        lrc = j['lrc']['lyric']
        lrc = re.sub(r'\[.*\]', "", lrc)
        lrc = lrc.strip()
        return lrc
    except:
        print("解析歌词过程出错-->>该歌曲暂无歌词？/该歌曲有版权限制，歌曲ID为:", song_id)


def write_to_text(lrc):
    with open('lrc.txt', 'a') as f:
        f.write(lrc)


def main():
    '''
    with open('song.csv', 'r') as csvfile:
        #reader = csv.reader(csvfile)
        for row in reader:
            try:
                song_id = row[0]
                print(song_id)
                page = getsong_page(song_id)
                lrc = parse_lrc(page)
                write_to_text(lrc)
            except:
                continue
    '''
    #username,password是mysql用户名及密码，请自行填充，music163数据库名字 也可以自行改成别的库    
    db = pymysql.connect("localhost", "username", "password", "MUSIC163")
    cursor = db.cursor()
    sql = '''select * from SONG_INFO'''
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        db.close()
        i = 0
        for item in results:
            try:
                song_id = item[0]
                song_name = item[1]
                page = getsong_page(song_id)
                lrc = parse_lrc(page, song_id)
                write_to_text(lrc)
            except:
                continue
        lrc_clean_function()
    except:
        print("读取歌曲库过程异常")


main()