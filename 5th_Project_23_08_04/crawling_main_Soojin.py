import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
import time
import random as rd
from konlpy.tag import Okt
from ASiteCralwer import ASiteCralwer
from Logger import Logger
from WebDriver import WebDriver
import pandas as pd
import re
webDriver = WebDriver()
webDriver.initCrawling()


# 네이버 블로그 크롤링 함수
# Crawling data function for Naver blogs
def naver_blog(url):
    try:
        driver = webdriver.Edge()
        url = "https://" + str(re.match("https{0,1}://(m.){0,1}(.*)",url).groups()[1])

        print("URL 주소 : ", url)
        driver.get(url)
        driver.implicitly_wait(3 + rd.randint(1,4))

        driver.switch_to.frame('mainFrame')
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        whole_border = soup.select_one('div#whole-border')
        results = whole_border.select('div.se-module')
        naver_content_list = []
        if(len(results)==0):
            results1=whole_border.select_one("#postViewArea")
            naver_content_list.append(results1.text)
            pass
        else:
            for result in results:
                naver_content_list.append(result.text)
                print(result.text)
        print(naver_content_list)
        driver.quit()
        return naver_content_list
    except Exception as e: 
        print("오류 발생 : " , e)
        pass

def wordpress(url):
    agent_option = webdriver.ChromeOptions()
    user_agent_string = 'Mozilla/5.0'
    agent_option.add_argument('user-agent=' + user_agent_string)
    driver = webdriver.Chrome('D:/chromedriver_win32/chromedriver',
    options=agent_option)

    driver.get(url)
    driver.implicitly_wait(3 + rd.randint(1,4))

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    whole_border = soup.select_one('#content')
    results = whole_border.select('article')

    wordpress_url_list = []
    for result in results:
        wordpress_url_list.append(result.text)
    driver.quit()
    df = pd.DataFrame(wordpress_url_list)
    return df

#print(wordpress('https://awesomedisplay.wordpress.com/2017/08/01/%EB%84%88%EB%AC%B4-%EB%98%91%EB%98%91%ED%95%B4%EC%A7%84-ai%EC%9E%90%EC%8B%A0%EB%A7%8C%EC%9D%98-%EC%9D%80%EC%96%B4%EB%A1%9C-%EB%8C%80%ED%99%94-%EC%B6%A9%EA%B2%A9/'))
#print(wordpress('https://popntalk.wordpress.com/2018/03/07/ai-saves-lives/'))

# def get_Noun_Adj(file_contents):
#     okt = Okt()
#     txt_list_tag = okt.pos(file_contents)
#     noun_adj_list = []
#     for word, tag in txt_list_tag:
#         if tag in ["Noun", 'Adjective']:
#             noun_adj_list.append(word)
#     return noun_adj_list

# print(get_Noun_Adj(naver_blog('https://blog.naver.com/knowledge_worker/223170703171')))


# 검색 후 사이트들의 링크를 담아내는 함수===============================
# Function for extracting links and citation
asiteCralwer = ASiteCralwer(webDriver)

def getLinks(year,maxPage, progress):
    query = 'site:blog.naver.com AI 딥페이크'
    maxPage = int(maxPage)
    link_all=[]

    _max = maxPage
    _nowValue = 0

    query2 = f'&tbs=cdr%3A1%2Ccd_min%3A%2Ccd_max%3A{year}&tbm='
    for page in range(maxPage):
        links = asiteCralwer.getItemsFromG(f"https://www.google.com/search?q={query}&start={(page)*10}"+ query2)
        link_all.extend(links)
        _nowValue+=1

        progress(_nowValue,_max)

    link_alls=[]
    for x in link_all:
        title = x[0]
        link = x[1]
        print(x)
        if("blog.naver.com" in link):
            link_alls.append((title,link))
    return link_alls

def process(fileName,link_all,progress):
    contents_list = []
    _max = len (link_all)
    nowValue=0
    links=[]
    titles=[]
    for link in link_all:
        links.append(link[1])
        titles.append(link[0])
        contents_list.append(naver_blog(link[1]))
        nowValue+=1
        progress(nowValue,_max)


    df = pd.DataFrame({'TITLE':titles, 
                    'URL':links, 
                    'CONTENT':contents_list})
    df.to_csv(fileName, index=False, sep='|')


def progress(value,max):
    print(value,"/",max)


# links_2005 = getLinks("2005",3,progress)
# process('naver_blog_citation_test_2005.csv',links_2005,progress)

# links_2015 = getLinks("2015",3,progress)
# process('naver_blog_citation_test_2015.csv',links_2015,progress)

links_2023 = getLinks("2023",3,progress)
process('naver_blog_citation_test_2023.csv',links_2023,progress)
# ===================================================================