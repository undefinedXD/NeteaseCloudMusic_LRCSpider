import execjs
import os
import pymysql
import traceback

with open('get_comment.js', 'r', errors='ignore') as f:
    jscode = f.read()

def readinDB():
    ctx = execjs.compile(jscode)
    db = pymysql.connect("localhost", "username", "password", "MUSIC163")    
    cursor = db.cursor()
    sql = """select * from SONG_INFO"""
    sql2 = """DELETE FROM `MUSIC163`.`SONG_INFO`  WHERE `SONG_ID` = %s; """
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for items in results:
            song_id = items[0]
            song_name = items[1]
            encrypt_data = ctx.call('get_comment',song_id,song_name)
            cursor.execute(sql2,(song_id))
            db.commit()
        db.close()
    except Exception as e:
        print("Error: ", e)
        traceback.print_exc()
readinDB()