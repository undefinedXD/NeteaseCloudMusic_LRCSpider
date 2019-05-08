# encoding : utf-8
import os
import re

# 该函数为生成词云图，清理歌词文本信息中的多余项
# 后来发现实际上在stopwords.txt里添加要过滤的词就可以

def lrc_clean_function():
    with open('lrc.txt') as f:
        lines = f.readlines()
        nums = len(lines)
        pattern = re.compile(r':|：')
        for i in range(nums):
            if (not re.search(pattern, lines[i])):
                lines[i].replace(lines[i], "")
                if (lines[i]):
                    with open('lrc_clean.txt', 'a') as f2:
                        f2.write(lines[i])