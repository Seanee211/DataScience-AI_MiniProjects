import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

# 2023년 4월 30일 발생한 "순살 아파트, 건축아파트 붕괴사건" 이후 대구 부동산 시장의 분석
# Analysis of Daegu's real estate market after the 'Apartment Colapse Incident' in the year 2023, April 30th 

def rent(filename):
    file=filename
    data=pd.read_excel(file, header=16)
    data = data.dropna(subset=['건축년도'])
    data['건축년도'] = data['건축년도'].astype('int64')
    
    
    data['계약년월'] = pd.to_datetime(data['계약년월'], format='%Y%m')
    monthly = data[data['전월세구분']=='월세']  
    
# 월세 : month_df 에 컬럼 추가 후 시군구 컬럼에서 동구만 추출
# monthly payment : add a column to month_df and extract '동구' only from '시군군' column

    month_df = monthly[['시군구', '전용면적(㎡)', '계약년월','전월세구분','월세(만원)', '건축년도' ]]
    month_df['시군구']=month_df['시군구'].apply(lambda v : v.split()[1])

# 전세 : annually_df 에 컬럼 추가 후 시군구 컬럼에서 동구만 추출    
# lease deposit : After adding a column to the annually_df, extract only the 'Dong-gu' from the '시군구' column.
    annually = data[data['전월세구분']=='전세']
    annually_df = annually[['시군구','전용면적(㎡)', '계약년월','전월세구분','보증금(만원)', '건축년도' ]]
    annually_df['시군구']=annually['시군구'].apply(lambda v : v.split()[1])
    annually_df = annually_df[annually_df['시군구']!='군위군']
    annually_df['보증금(만원)'] = annually_df['보증금(만원)'].apply(lambda x:int(x.replace(',', '')))
    
    return month_df, annually_df
def trading(filename):
    file=filename
    data=pd.read_excel(file, header=16)
    data= data.dropna(subset=['건축년도'])
    data['건축년도'] = data['건축년도'].astype('int64')
    
    
    data['계약년월'] = pd.to_datetime(data['계약년월'], format='%Y%m')
    
# 매매 :
# Purchase data :
    trading_df = data[['시군구','전용면적(㎡)', '계약년월','거래금액(만원)', '건축년도' ]]
    trading_df['시군구']=data['시군구'].apply(lambda v : v.split()[1])
    trading_df = trading_df[trading_df['시군구']!='군위군']
    trading_df['거래금액(만원)'] = trading_df['거래금액(만원)'].apply(lambda x:int(x.replace(',', '')))

    return trading_df

def EightMonth_before(area_list, df1):
    Before_first_four_month = []
    Before_second_four_month = []

    for a in area_list:
        mask1 = df1[df1['시군구']==a]
        construct_df_1999 = mask1[mask1['건축년도'] < 2020]
        # 1월부터 4월의 데이터
        # Data between January and April
        df_first1 = construct_df_1999[(construct_df_1999['계약년월'].dt.month >= 1) & (construct_df_1999['계약년월'].dt.month <= 4)] 

        # 5월부터 7월말의 데이터
        # Data between May and the end of July
        df_second1 = construct_df_1999[(construct_df_1999['계약년월'].dt.month > 4) & (construct_df_1999['계약년월'].dt.month <= 7)] 
        
        # 1월~4월의 계약건수, 5월~7월의 계약건수
        # number of contracts January~April, May~July
        Before_first_four_month.append(df_first1.shape[0])
        Before_second_four_month.append(df_second1.shape[0])

    return Before_first_four_month, Before_second_four_month
def EightMonth_after(area_list, df2):
    After_first_four_month = []
    After_second_four_month = []

    for a in area_list:
        mask2 = df2[df2['시군구']==a]
        construct_df_2020 = mask2[mask2['건축년도'] >= 2020]
        # 1월부터 4월의 데이터
        # Data between January and April
        df_first2 = construct_df_2020[(construct_df_2020['계약년월'].dt.month >= 1) & (construct_df_2020['계약년월'].dt.month <= 4)]

        # 5월부터 7월말의 데이터
        # Data between May and the end of July
        df_second2 = construct_df_2020[(construct_df_2020['계약년월'].dt.month > 4) & (construct_df_2020['계약년월'].dt.month <= 7)]

        After_first_four_month.append(df_first2.shape[0])
        After_second_four_month.append(df_second2.shape[0])
        
    return After_first_four_month, After_second_four_month # 1월~4월의 계약건수, 5월~7월의 계약건수 (number of contracts January~April, May~July)

# 확인용 (for verification) ---------------------------------------------------------------------------------------
# area_set = ['중구','동구','서구','남구','북구','수성구','달서구','달성군']

# trading_before1, trading_before2 = EightMonth_before(office_trade_df)
# trading_after1, trading_after2 = EightMonth_after(office_trade_df)

# def Get_before_fourMonth_list(tup1):
#     area_set = ['중구','동구','서구','남구','북구','수성구','달서구','달성군']
    
#     for idx in range(len(area_set)):
#         print(f"2020년 이전, 대구 광역시 {area_set[idx]} 지역의 1월부터 4월까지의 계약건수는 {tup1[0][idx]}이고\n5월부터 7월말까지의 계약건수는 {tup1[1][idx]}.")
#         print()

# def Get_after_fourMonth_list(tup2):
#     area_set = ['중구','동구','서구','남구','북구','수성구','달서구','달성군']

#     for idx in range(len(area_set)):
#         print(f"2020년 이후, 대구 광역시 {area_set[idx]} 지역의 1월부터 4월까지의 계약건수는 {tup2[0][idx]}이고\n5월부터 7월말까지의 계약건수는 {tup2[1][idx]}.")
#         print()

# Get_before_fourMonth_list(trading_before_first_four_month)
# print('-'*100)
# Get_after_fourMonth_list(trading_after_first_four_month)
# ----------------------------------------------------------------------------------------------

def visualize(title, area, list1, list2):
    font_location = r'c:/Windows/Fonts/malgun.ttf'
    font_name = fm.FontProperties(fname=font_location).get_name()
    plt.rc('font', family=font_name, size=12)

    plt.figure(figsize=(12, 6)) 
    bar_width = 0.35
    index = np.arange(len(area))

    plt.bar(index, list1, bar_width, label='1월~4월', color='b', alpha=0.7)
    plt.bar(index + bar_width, list2, bar_width, label='5월~7월', color='r', alpha=0.7)

    plt.xlabel('지역')
    plt.ylabel('계약건수')
    plt.title(title)
    plt.xticks(index + bar_width / 2, area) 
    plt.legend()

    plt.tight_layout()
    plt.show()

def visualize_compare(title, list1, list2):
    font_location = r'c:/Windows/Fonts/malgun.ttf'
    font_name = fm.FontProperties(fname=font_location).get_name()
    plt.rc('font', family=font_name, size=12)

    total_list1 = sum(list1)
    total_list2 = sum(list2)

    plt.figure(figsize=(8, 6))

    labels = ['1월~4월\n총 계약 건수', '5월~7월\n총 계약 건수']
    comparison = [total_list1, total_list2]

    plt.bar(labels, comparison, color=['purple', 'orange'])

    plt.xlabel('기간별 비교')
    plt.ylabel('총 계약건수')
    plt.title(title)
    plt.show()

office_trade_df = trading('.\오피스텔(매매)_실거래가_20230810 (1).xlsx')
office_rent_df = rent('.\오피스텔(전월세)_실거래가_20230810.xlsx')
apt_trade_df = trading('.\아파트(매매)_실거래가_20230811092808.xlsx')
apt_rent_df = rent('.\아파트(전월세)_실거래가_20230811094129.xlsx')

area_set = ['중구','동구','서구','남구','북구','수성구','달서구','달성군']

# ====================================================================================================================================
FLAG1 = False
if FLAG1:
    # 오피스텔 매매 : 2020년 이전 구별 계약건수
    # The number of office-tel sales by district prior to 2020.
    office_trading_before1, office_trading_before2 = EightMonth_before(area_set, office_trade_df)
    visualize('오피스텔(매매) 건축년도 2020년 이전 각 지역 계약 건수', area_set, office_trading_before1, office_trading_before2)

    # 오피스텔 매매 : 2020년 이후 구별 계약건수
    # The number of office-tel sales by district since 2020.
    office_trading_after1, office_trading_after2 = EightMonth_after(area_set, office_trade_df)
    visualize('오피스텔(매매) 건축년도 2020년 이후 각 지역 계약 건수', area_set, office_trading_after1, office_trading_after2)

    # 오피스텔 전월세 : 2020년 이전 구별 계약건수
    # The number of office-tel rentals by district prior to 2020.
    office_renting_before1, office_renting_before2 = EightMonth_before(area_set, office_rent_df[0])# tuple로 데이터프레임 두개가 담겼기 때문
    visualize('오피스텔(전월세) 건축년도 2020년 이전 각 지역 계약 건수', area_set, office_renting_before1, office_renting_before2)

    # 오피스텔 전월세 : 2020년 이후 구별 계약건수
    # The number of office-tel rentals by district since 2020
    office_renting_after1, office_renting_after2 = EightMonth_after(area_set, office_rent_df[0])
    visualize('오피스텔(전월세) 건축년도 2020년 이후 각 지역 계약 건수', area_set, office_renting_after1, office_renting_after2)

    # 아파트 매매 : 2020년 이전 구별 계약건수
    # The number of apartment sales by district prior to 2020.
    apt_trading_before1, apt_trading_before2 = EightMonth_before(area_set, apt_trade_df)
    visualize('아파트(매매) 건축년도 2020년 이전 각 지역 계약 건수', area_set, apt_trading_before1, apt_trading_before2)

    # 아파트 매매 : 2020년 이후 구별 계약건수
    # The number of apartment sales by district since 2020.
    apt_trading_after1, apt_trading_after2 = EightMonth_after(area_set, apt_trade_df)
    visualize('아파트(매매) 건축년도 2020년 이후 각 지역 계약 건수', area_set, apt_trading_after1, apt_trading_after2)

    # 아파트 전월세 : 2020년 이전 구별 계약건수
    # The number of apartment rentals by district prior to 2020.
    apt_renting_before1, apt_renting_before2 = EightMonth_before(area_set, apt_rent_df[0])
    visualize('아파트(전월세) 건축년도 2020년 이전 각 지역 계약 건수', area_set, apt_renting_before1, apt_renting_before2)
    
    # 아파트 전월세 : 2020년 이후 구별 계약건수
    # The number of apartment rentals by district since 2020.
    apt_renting_after1, apt_renting_after2 = EightMonth_after(area_set, apt_rent_df[0])
    visualize('아파트(전월세) 건축년도 2020년 이후 각 지역 계약 건수', area_set, apt_renting_after1, apt_renting_after2)

# ====================================================================================================================================

FLAG2 = False
if FLAG2:
    # 오피스텔 매매 : 2020년 이전 총 계약건수
    # office-tel sales : Total number of contract prior to 2020.
    visualize_compare('오피스텔(매매) 건축년도 2020년 이전 4개월 단위 총 계약건수 비교', office_trading_before1, office_trading_before2)
    
    # 오피스텔 매매 : 2020년 이후 총 계약건수
    # office-tel sales : Total number of contract since 2020.
    visualize_compare('오피스텔(매매) 건축년도 2020년 이후 4개월 단위 총 계약건수 비교', office_trading_after1, office_trading_after2)
    
    # 오피스텔 전월세 : 2020년 이전 총 계약건수
    # office-tel rentals : Total number of contract prior to 2020.
    visualize_compare('오피스텔(전월세) 건축년도 2020년 이전 4개월 단위 총 계약건수 비교', office_renting_before1, office_renting_before2)
    
    # 오피스텔 전월세 : 2020년 이후 총 계약건수
    # office-tel rentals : Total number of contract since 2020.
    visualize_compare('오피스텔(전월세) 건축년도 2020년 이후 4개월 단위 총 계약건수 비교', office_renting_after1, office_renting_after2)
    
    # 아파트 매매 : 2020년 이전 총 계약건수
    # apartment sales : Total number of contract prior to 2020.
    visualize_compare('아파트(매매) 건축년도 2020년 이전 4개월 단위 총 계약건수 비교', apt_trading_before1, apt_trading_before2)
    
    # 아파트 매매 : 2020년 이후 총 계약건수
    # apartment sales : Total number of contract since 2020.
    visualize_compare('아파트(매매) 건축년도 2020년 이후 4개월 단위 총 계약건수 비교', apt_trading_after1, apt_trading_after2)
    
    # 아파트 전월세 : 2020년 이전 총 계약건수
    # apartment rentals : Total number of contract prior to 2020.
    visualize_compare('아파트(전월세) 건축년도 2020년 이전 4개월 단위 총 계약건수 비교', apt_renting_before1, apt_renting_before2)
    
    # 아파트 전월세 : 2020년 이후 총 계약건수
    # apartment rentals : Total number of contract since 2020.
    visualize_compare('아파트(전월세) 건축년도 2020년 이후 4개월 단위 총 계약건수 비교', apt_renting_after1, apt_renting_after2)