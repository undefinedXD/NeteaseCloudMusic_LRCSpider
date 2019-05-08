# NeteaseCloudMusic_LRCSpider
网易云音乐歌手及其热门歌曲的歌词爬虫


## To Do List
-----

1. MySQL查询优化？
2. ~~添加已入库歌曲/歌手时的交互反馈~~
3. ~~通过民谣歌单 自动获取民谣歌手集合//标记歌曲类别~~
4. ~~增加获取评论功能 *基于puppeteer的NodeJS方法已实现，python 方法(getcomment.py)待完成~~
5. ~~添加requirements.txt~~
6. 增加爬取评论时显示当前进度功能
7. ~~某些页面评论无法正常爬取（但页面有响应） 原因待排查~~
-----

提取的民谣歌词高频词云图：


![](https://github.com/cheerway6/NeteaseCloudMusic_LRCSpider/blob/master/res6.png?raw=true)

---
## 执行步骤
### 方法1:
首先爬取网易云音乐所有华语歌手信息并入库，然后根据要爬取的歌手来获取其歌曲及歌词
先后在终端内依次执行getAllSinger.py、getSingersTop50.py、getlrc.py、lrccloud.py

### 方法2:
直接爬取歌单下的所有歌曲和歌词信息
先后在终端内依次执行getSongList.py、getlrc.py、lrccloud.py

---
