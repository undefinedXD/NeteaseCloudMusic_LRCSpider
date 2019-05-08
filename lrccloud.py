# coding: utf-8
import jieba
import imageio
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

back_color = imageio.imread('001.jpg')

text = open('lrc_clean.txt').read()


# 该函数的作用就是把屏蔽词去掉，使用这个函数就不用在WordCloud参数中添加stopwords参数了
# 把你需要屏蔽的词全部放入一个stopwords文本文件里即可
def stop_words(texts):
    words_list = []
    word_generator = jieba.cut(texts, cut_all=False)  # 返回的是一个迭代器
    with open('stopwords.txt') as f:
        str_text = f.read()
        unicode_text = str(str_text)
        f.close()  # stopwords文本中词的格式是'一词一行'
    for word in word_generator:
        if word.strip() not in unicode_text:
            words_list.append(word)
    return ' '.join(words_list)  # 注意是空格


text = stop_words(text)

wc = WordCloud(
    background_color='white',  # 背景颜色
    max_words=3500,  # 最大词数
    mask=back_color,  # 以该参数值作图绘制词云，这个参数不为空时，width和height会被忽略
    max_font_size=320,  # 显示字体的最大值
    min_font_size=30,
    collocations=False,     #默认为True 这里打开避免词语重复
    font_path="STHeiti Medium.ttc",  # 解决显示字体乱码问题
    random_state=42,  # 为每个词返回一个PIL颜色
    # width=1000,  # 图片的宽
    # height=860  #图片的长
)

wc.generate(text)
# 基于彩色图像生成相应彩色
image_colors = ImageColorGenerator(back_color)
# 显示图片
plt.imshow(wc)
# 关闭坐标轴
plt.axis('off')
# 绘制词云
plt.figure()
plt.imshow(wc.recolor(color_func=image_colors))
plt.axis('off')
# 保存图片
wc.to_file('res6.png')