from crawling_functions import *
DEBUG = True
if DEBUG: keyword = input('키워드 입력: ')
else: keyword ='볼펜'
cost_list = [] # 사입원가 리스트 전역변수
final_keywords = set() # 최종 반환용 연관키워드 리스트 전역변수 (형용사 및 동사를 조합한 키워드 추출)
# 함수 호출 및 크롤링 통합적 실행
driver = webdriver.Chrome(ChromeDriverManager().install())
driver_2 = webdriver.Chrome(ChromeDriverManager().install())

price_list = [] # 가격 리스트 전역변수
purchase_list = [] # 구매 건수 리스트 전역변수
review_list = [] # 리뷰 건수 리스트 전역변수
jjim_list = [] # 찜 건수 리스트 전역변수

while True:
    search_domaekook(keyword, driver, cost_list)
    price_list_2, purchase_list_2, review_list_2, jjim_list_2 = search_Naver(keyword, driver)
    price_list += price_list_2
    purchase_list += purchase_list_2
    review_list += review_list_2
    jjim_list += jjim_list_2
    extract_adj_verb(keyword, driver, final_keywords) # final_keywords 빈 리스트 연관 키워드 추가
    
    print(final_keywords)

    for kword_ in final_keywords: # 추출된 연관 키워드 (형용사 or 동사) 크롤링
        driver_2 = get_Naver_page(kword_, driver_2)

        scroll_down(driver_2)
        # 네이버 페이지별 추출
        for _ in tqdm(range(20)):
            extract_content(driver_2, price_list, purchase_list, review_list, jjim_list)# 중요 피쳐 데이터 추출 후 각 리스트에 담아내는 함수       
            view_to_button(driver_2) # next 버튼의 좌표를 잡아주는 함수
            time.sleep(0.3)
                    
            # 페이지 넘기는 버튼 클릭
            driver_2.find_element(By.CSS_SELECTOR, "button.paginator_btn_next__3fcZx").click()
            time.sleep(0.3)
            
            scroll_down(driver_2)
    break
driver_2.close()
final_keywords # 데이터 수집에 쓰여진 "제품군 keyword"의 연관 키워드들
import statistics
purchase_cost = statistics.median(cost_list) # 사입 원가들의 중앙값
purchase_cost
len(price_list),len(purchase_list) ,len(review_list) ,len(jjim_list)
import numpy as np

final_data = [price_list, purchase_list, review_list, jjim_list]
df = pd.DataFrame(np.array(final_data).T, columns=['가격', '구매건수', '리뷰 건수', '찜 건수']).dropna()
df
df[['구매건수','가격','리뷰 건수', '찜 건수']] = df[['구매건수','가격','리뷰 건수', '찜 건수']].astype(int)
new_df = del_outlier_quantiles_columns(df, '가격') # 사분위수를 활용한 가격 컬럼 이상치 제거
new_df = new_df.drop_duplicates().reset_index(drop=True)

# 도매꾹의 사입원가들의 중앙값으로 원가 기준을 정했지만 그 숫자가 원가 50%보다 더 클 가능성이 있기 때문 원가조정 실행
new_cost = (new_df.가격) * 0.5

# 개당 원가 파생변수 추출 (0.1 은 10%의 부가세)
new_df['개당 원가'] = np.where(purchase_cost > new_cost, 
                               new_cost + ((new_df.가격)*0.1), 
                               purchase_cost + ((new_df.가격)*0.1)) 
new_df
from googletrans import Translator

translator = Translator()
text = keyword
translated = translator.translate(text, src='ko', dest='en')

print(translated.origin, '->', translated.text)

new_df.to_csv(f'naver_{translated.text}_data.csv')
