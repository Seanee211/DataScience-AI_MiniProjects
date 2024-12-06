from crawling_functions import *
from data_collection_2 import *
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV, KFold
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score


def data_predict(keyword, user_purchase=None, user_review=None, user_jjim=None, user_cost=None): 

    # DEBUG = True
    # if DEBUG: keyword = input('키워드 입력: ')
    # else: keyword ='볼펜'

    cost_list = [] # 사입원가 리스트 전역변수

    # 데이터 수집에 쓰여진 "제품군 keyword"의 연관 키워드들
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
    purchase_cost = statistics.median(cost_list) # 사입 원가들의 중앙값


    final_data = [price_list, purchase_list, review_list, jjim_list]
    df = pd.DataFrame(np.array(final_data).T, columns=['가격', '구매건수', '리뷰 건수', '찜 건수']).dropna()
    df[['구매건수','가격','리뷰 건수', '찜 건수']] = df[['구매건수','가격','리뷰 건수', '찜 건수']].astype(int)
    new_df = del_outlier_quantiles_columns(df, '가격') # 사분위수를 활용한 가격 컬럼 이상치 제거
    new_df = new_df.drop_duplicates().reset_index(drop=True)

    # 도매꾹의 사입원가들의 중앙값으로 원가 기준을 정했지만 그 숫자가 원가 50%보다 더 클 가능성이 있기 때문 원가조정 실행
    new_cost = (new_df.가격) * 0.5

    # 개당 원가 파생변수 추출 (0.1 은 10%의 부가세)
    new_df['개당 원가'] = np.where(purchase_cost > new_cost, 
                                new_cost + ((new_df.가격)*0.1), 
                                purchase_cost + ((new_df.가격)*0.1)) 

    # translator = Translator()
    # text = keyword
    # translated = translator.translate(text, src='ko', dest='en')

    # new_df.to_csv(f'naver_{translated.text}_data.csv')




    # -------------------------------------------------------------------------------------------------------------------------
    # 모델링
    # -------------------------------------------------------------------------------------------------------------------------



    # data = pd.read_csv('./naver_pen_data.csv').drop('Unnamed: 0', axis=1)
    # data = pd.read_csv('./naver_shoes_data.csv').drop('Unnamed: 0', axis=1)
    data = new_df

    # 피쳐와 타겟 데이터 분할
    X = data.drop('가격', axis=1) # 피쳐데이터
    y = data['가격'] # 타겟 데이터

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    # 다중 회귀 모델 생성 및 학습
    model = LinearRegression()
    model.fit(X_train, y_train)

    # 테스트 데이터에 대한 예측 수행
    y_pred = model.predict(X_test)

    # 평균 제곱 오차 계산 (모델의 성능 평가)
    mse = mean_squared_error(y_test,y_pred)
    print('Mean Squared Error:', mse)

    rmse = np.sqrt(mse)
    print(f'평균 오차: {round(rmse):,}원')

    r2 = r2_score(y_test, y_pred)
    print('R-squared:', round(r2,4))
    # k-fold 교차 검증 및 그리드 서치로 최적의 하이퍼파라미터 탐색

    param_grid = {'fit_intercept':[True,False], 'copy_X':[True,False]}
    kfold_cv=KFold(n_splits=5) # k-fold 교차 검증 설정
    grid_search=GridSearchCV(LinearRegression(), param_grid, cv=kfold_cv) # 그리드 서치 객체 생성
    grid_search.fit(X,y)


    best_params = grid_search.best_params_
    print('Best Parameters:', best_params)
    print('Best Score:', grid_search.best_score_)

    best_model = LinearRegression(**best_params)
    best_model.fit(X, y)


    # 새로운 데이터 생성
    new_data = pd.DataFrame({
        '구매건수': [user_purchase],
        '리뷰 건수': [user_review],
        '찜 건수': [user_jjim],
        '개당 원가': [user_cost]
    })

    # 모델에 새로운 데이터 넣어서 예측 수행
    predicted_price = best_model.predict(new_data)

    return f"예측 가격: {round(predicted_price[0]):,}원"
