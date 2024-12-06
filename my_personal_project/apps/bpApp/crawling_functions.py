import pandas as pd # 표 형식의 데이터를 다룰 수 있는 pandas를 pd라고 줄여서 불림
from selenium import webdriver # 크롬 창을 조종하기 위한 모듈
from selenium.webdriver.common.by import By # 웹사이트의 구성요소를 선택하기 위해 By 모듈을 불림
from selenium.webdriver.support.ui import WebDriverWait # 웹페이지가 전부 로드될때까지 기다리는 (Explicitly wait) 기능을 하는 모듈
from webdriver_manager.chrome import ChromeDriverManager # 크롬에서 크롤링을 하기 위해, 웹 드라이버를 설치하는 모듈
from selenium.webdriver.support import expected_conditions as EC # 크롬의 어떤 부분의 상태를 확인하는 모듈
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time # 정해진 시간만큼 기다리게 하기 위한 패키지
from tqdm import tqdm
import requests # 페이지 요청
from bs4 import BeautifulSoup 
# from konlpy.tag import Okt

# ---------------------------------------------------------------------------------------------------------------------------------

# 스크롤 다운 함수화
def scroll_down(driver):
    position = 0

    while True:
        # 스크롤 다운
        driver.execute_script(f"window.scrollTo(0, {position});")
        
        # 페이지 로딩 대기 및 위치 증가
        position += 600
        time.sleep(0.2)

        # 새로운 높이 가져오고 비교하기 
        new_height = driver.execute_script("return document.body.scrollHeight")
      
        if position >= new_height:
            break

# ---------------------------------------------------------------------------------------------------------------------------------

def extract_content(driver,price_list, purchase_list, review_list, jjim_list): # 네이버 키워드 입력 후 각 소호몰 쇼핑몰 별 상세페이지 기본 정보 추출

    import re

    element_text=[]
    new = []
    link_element = driver.find_elements(By.CLASS_NAME, 'product_list_item__b84TO') # 구매건수, 리뷰, 찜 뽑기
    time.sleep(3)

    #평점 뽑기
    for idx in range(len(link_element)):
        element_text.append([link_element[idx].text]) 

    for e in element_text:
        e = "".join(e).replace('\n', ' ').split()
        result = any(re.search(r"(?=.*구매)(?=.*리뷰)(?=.*찜)", item) for item in e)
        if '배송비' in e and result:
            new.append(e)
    try:    
        for n in new:
            for i in range(len(n)):
                if n[i] == '배송비':
                    price_list.append(int(n[i-1].replace('원','').replace(',','')))
                elif ('구매' in n[i]) and ('리뷰' in n[i]) and ('찜' in n[i]):
                    init_ = n[i].replace('구매', '').replace('리뷰', ' ').replace('찜', ' ').split() # 구매건수, 리뷰, 찜 추출
                    purchase_list.append(int(init_[0].replace(',','')))
                    review_list.append(int(init_[1].replace(',','')))
                    jjim_list.append(int(init_[2].replace(',','')))
                else: pass
    except: pass

# ---------------------------------------------------------------------------------------------------------------------------------

# 도매꾹 홈 -> 키워드 입력 -> 인기상품순 정렬 -> 전체 가격(사입원가) 추출
def search_domaekook(keyword, driver, cost_list):

    driver.get('https://domeggook.com/main//')
    driver.implicitly_wait(10) # 정보가 모두 뜰때까지 최대 10초를 기다린다.
    time.sleep(3)

    driver.find_element(By.CSS_SELECTOR,'#searchWordForm').send_keys(f'{keyword}')
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, '#searchWordSubmit').click()
    time.sleep(3)

    # 인기상품순 클릭으로 인기순 정렬
    driver.find_element(By.CSS_SELECTOR, '#lSort > li:nth-child(5) > a').click()
    time.sleep(3)
  
    split_list = driver.find_elements(By.CLASS_NAME, 'amt')
    time.sleep(3)

    # 광고 없는 사입 상품들의 가격(사입원가)만 추출
    try:
        for s in split_list[1:]:
                cost_list.append(int(s.text.replace('원','').replace(',','')))
    except: pass

# ---------------------------------------------------------------------------------------------------------------------------------

def view_to_button(driver):
        rs = driver.execute_script("return document.getElementsByClassName('paginator_btn_next__3fcZx')[0].getBoundingClientRect().top;")
        now_y = driver.execute_script("return window.scrollY")
        driver.execute_script(f"window.scrollTo(0, {now_y + rs-200});")

# ---------------------------------------------------------------------------------------------------------------------------------

def get_Naver_page(keyword, driver): # 네이버 쇼핑 홈 -> '키워드 입력' -> 검색 -> [소호몰] 정렬순 클릭
#def get_Naver_page(keyword):
    driver.get('https://shopping.naver.com/home')
    driver.implicitly_wait(10)
    time.sleep(3)

    driver.find_element(By.CSS_SELECTOR, '#gnb-gnb > div > div._combineHeader_inner_2Uy4J > button > span').click()
    time.sleep(3)
    # 볼펜 입력
    driver.find_element(By.CSS_SELECTOR,'#input_text').send_keys(f'{keyword}')
    time.sleep(3)
    # 돋보기 버튼 클릭
    driver.find_element(By.CSS_SELECTOR, '#gnb-gnb > div > div._combineHeader_inner_2Uy4J > div._combineHeader_right_button_area_10E31 > button._combineHeader_button_2xfGa.N\=a\:scb\.search').click()
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, '#__next > div > div.style_container__IrlMV > div.basicFilter_filter_wrap__WgrCe > div.basicFilter_filter_button_area__A_l9Y > span:nth-child(4) > button > span').click()
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, '#__next > div > div.style_container__IrlMV > div.basicFilter_filter_wrap__WgrCe > div.basicFilterDetail_basic_filter_option__VVSCg.basic_filter.active > div.flick_area > div > div > ul:nth-child(1) > li:nth-child(6) > button > span').click()
    time.sleep(1)

    return driver

# ---------------------------------------------------------------------------------------------------------------------------------

# 네이버 메인 페이지 동적 크롤링
def search_Naver(keyword, driver, page_num=20):
    price_list = [] # 가격 리스트 지역변수
    purchase_list = [] # 구매 건수 리스트 지역변수
    review_list = [] # 리뷰 건수 리스트 지역변수
    jjim_list = [] # 찜 건수 리스트 지역변수
    driver = get_Naver_page(keyword, driver)

    scroll_down(driver)
    for _ in tqdm(range(page_num)):
        extract_content(driver,price_list, purchase_list, review_list, jjim_list)# 중요 피쳐 데이터 추출 후 각 리스트에 담아내는 함수       
        view_to_button(driver) # next 버튼의 좌표를 잡아주는 함수
        time.sleep(0.2)
                
        # 페이지 넘기는 버튼 클릭
        driver.find_element(By.CSS_SELECTOR, "button.paginator_btn_next__3fcZx").click()
        time.sleep(0.2)
        
        scroll_down(driver)
    return price_list, purchase_list, review_list, jjim_list

# ---------------------------------------------------------------------------------------------------------------------------------

def extract_adj_verb(keyword, driver,final_keywords):
    driver = get_Naver_page(keyword, driver)

    tag_list = []
    li_tag = driver.find_elements(By.TAG_NAME, 'li')
    time.sleep(3)
    
    related_keywords = []
    for l in li_tag:
        if not l.text.startswith('#') or len(l.text):
            tag_list.append(l.text.replace('#',''))
    filtered_list = list(filter(None, tag_list))
    related_keywords.extend(filtered_list)

    init_keywords = [] # 형용사 및 동사 추출용 리스트
    for k in related_keywords:
        if keyword in k:
            init_keywords.append(k)

    okt = Okt() # OKT 객체 생성
    for word in init_keywords:
        pos = okt.pos(word)
        for p in pos:
            if p[1] == 'Adjective' or p[1] == 'Verb':
                final_keywords.add(p[0]+keyword)
        # return driver

#--------------------------------------------------------------------------------------------------------------------------

def del_outlier_quantiles_columns(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1

    mask = (df[column] > Q1 - (IQR * 1.5)) & (df[column] < Q3 + (IQR * 1.5))
    return df[mask]

#--------------------------------------------------------------------------------------------------------------------------

