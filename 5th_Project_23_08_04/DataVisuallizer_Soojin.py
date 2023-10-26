import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
import time
import random as rd
from wordcloud import WordCloud
from collections import Counter
from konlpy.tag import Okt
from ASiteCralwer import ASiteCralwer
from Logger import Logger
from WebDriver import WebDriver
import pandas as pd
import re
import matplotlib.pyplot as plt

# def returnTypes():
#     return [(f"워드 클라우드 보기",process)]

# 네이버 블로그 크롤링 (딥 페이크에 대한 네이버 블로그 인식 분석)
# Crawling Data from Naver Blogs (Analysis for the recognition of "Deep Fake" in Naver blogs)

# 데이터 프레임 안에 데이터 입력
# Inserting datas into dataframe
def process(df):
    print("안녕 데이터 프레임 : ", df)
    data=[]
    a=0
    for x in df.iloc:
        a+=1
        okt = Okt()
        okt_tags = okt.pos(str(x["CONTENT"]), norm=True, stem=True)
        for word, tag in okt_tags:
            if (tag == "Noun"):
                data.append(word)
        print(a,df["CONTENT"].count())

    print(data)
    ct = Counter(data)
    items = ct.most_common(70)
    print(items)


    # 워드클라우드를 이용하여 단어들의 최빈값 추출
    # Extracting the most used words using Word Cloud
    wc = WordCloud(font_path="D:/NanumGothic.ttf",background_color="white", max_font_size=60)
    cloud = wc.generate_from_frequencies(dict(items))

    plt.figure(figsize=(1.2,1.2),dpi=1000)
    plt.axis("off")
    plt.imshow(cloud)
    plt.show()

# process(pd.read_csv("naver_blog_citation_test_2005.csv", header=0, index_col=0, encoding="UTF-8", sep="|"))
# process(pd.read_csv("naver_blog_citation_test_2015.csv", header=0, index_col=0, encoding="UTF-8", sep="|"))
process(pd.read_csv("naver_blog_citation_test_2023.csv", header=0, index_col=0, encoding="UTF-8", sep="|"))