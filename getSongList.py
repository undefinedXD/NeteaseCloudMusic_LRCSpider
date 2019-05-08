# encoding : utf-8
import requests
import re
import pymysql
from bs4 import BeautifulSoup
import traceback

# 从歌单直接导入歌曲并标记歌曲种类的方法
def get_html_src(url):
    header = {
    'Host':'music.163.com',
    'Referer':'https://music.163.com/',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'
}
    try:
        r = requests.get(url, headers=header)
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'lxml')
        song_list = soup.ul.contents
        return song_list
    except Exception as e:
            print("Error: ", e)
            traceback.print_exc()


def parselist(songlist,song_tag):
    pat = re.compile('[0-9]\d*')
    #username,password是mysql用户名及密码，请自行填充，music163数据库名字 也可以自行改成别的库    
    db = pymysql.connect("localhost", "username", "password", "MUSIC163")
    cursor = db.cursor()
    for item in songlist:
        song_name = item.a.text
        song_id = re.findall(pat,item.a.get('href'))
        try:
            sql = """INSERT INTO SONG_INFO
                    values(%s,%s,%s)"""
            cursor.execute(sql, (song_id, song_name, song_tag))
            db.commit()
        except:
            db.rollback()
    db.close()

def main():
    root = 'https://music.163.com/playlist?id='
    playlist_ID = input("请输入歌单数字ID:")
    song_tag = input("请指定你希望保存的该歌单种类名称（如民谣/小语种/轻音乐等）：")
    url = root + playlist_ID
    song_list = get_html_src(url)
    parselist(song_list,song_tag)

if __name__ == "__main__":
    main()