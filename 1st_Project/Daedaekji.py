# 서비스 "대댁지"의 핵심 기능들
# (Core Functions for the random-food-choice service: "Daedaekji")

# 1. 좋아하는 음식들 저장 후
# (1. save the foods you like)

# 2. 기존에 큐레이트 해놨던 모든 메뉴들을 무작위로 한가지 추천:
# (2. Randomly choose one of the menus the user has saved/curated)

# 3. 리스트 초기화를 통해 새로운 목록 생성
# (3. resetting the previous food list and making a new list)

# 4. 세가지의 키워드만 입력 : '배고파', '대댁지?', '배불러'
# (4. Three keywords to type : 'Im hungry', 'WhatDoIEat?', 'Im full' )


# 첫번째 기능) 좋아하는 메뉴 저장 =====================================================================================
# (First Function) Save your favorite menu =========================================================================)

# 좋아하는 메뉴를 저장할 수 있는 파일:
# (The file for saving the user's favorite menus)
filename= "C:\\Users\\KDP-23\Desktop\\python_Sean\\PROJECT\\food_list.txt"

# 기존에 먹었던 메뉴를 저장할 수 있는 파일:
# (The file for saving the user's previous menu chosen before)
same_count_list = 'C:\\Users\KDP-23\\Desktop\\python_Sean\\PROJECT\\same_count.txt'


# 좋아하는 메뉴 파일:
# (favorite menu file)
with open(filename, mode='a', encoding='utf-8') as fp:
    while True:      
        try:
            # 좋아하는 음식 원하는대로 저장 input:
            # The input function for saving the user's favorite food:
            menu = input('좋아하는 음식 저장(예: 짜장면) "배불러" 입력시 저장 종료) : ')
            
            # 배불러 입력시 메뉴 랜덤 추출하고 결정하는 단계로 진입:
            if menu  == '배불러':
                break
            # 미입력시 예외처리:
            if not len(menu): raise Exception("데이터 미입력")
            # 제대로 입력시 좋아하는 메뉴를 자체 큐레이트한 food_list에 저장:
            else: fp.write(f'{menu}\n')
        except Exception as e:
            print(f"ERROR : {e}")


# 두번째 기능) 메뉴 랜덤 출력 =====================================================================================


class FoodChoice:
    def __init__(self, _gacha):
        self.gacha =_gacha

    # Random 모듈 사용 않고 기능 추가
    def choice(self):
        with open(filename, mode='r', encoding='utf-8') as fp:
            #대댁지 입력시 기존에 저장해놨던 메뉴들을 랜덤으로 추출:
            if self.gacha == '대댁지':
                 # 중복-지양적 랜덤 추출을 위한 빈 세트 생성:
                choice = set()
                # 저장했던 food_list에서 중복없이 빈 세트에 생성:
                for f in set(fp.readlines()): choice.add(f.rstrip('\n'))
                
            while True:
                    # 비어 있는 세트가 아닐시:
                    if len(choice) != 0:
                        # 랜덤으로 추출:
                        random_food=choice.pop()
                        # 랜덤으로 뽑은 메뉴 출력:
                        print(f"오늘의 랜덤 메뉴는 {random_food}입니당")


                        # 다른 메뉴를 고르고 싶을 땐 '배고파' 입력, Enter 입력, 해당 메뉴로 정했을 시 Enter:
                        again = input('다시 고르려면 "배고파" 입력, 이 메뉴로 정했으면 엔터 입력 : ')
                        if again == "배고파": continue
                        else:
                            # 해당 메뉴 정했을 시 기존에 먹었던 음식으로 same_count_list 파일 저장:
                            with open(same_count_list, mode='a', encoding='utf-8') as fp2:
                                fp2.write(f'{random_food}\n')
                            # 메뉴를 정했기 때문에 프로그램 종료:    
                            return "오늘도 대댁지 내일도 대댁지"
                    else:
                        # choice set 가 set(food_list)보다 큰 길이면 중복으로 추출될 수 있기 때문에 길이가 똑같을 시 안내문
                        return "저장하신 메뉴들을 모두 고르셨습니다. 추가로 더 저장하시거나 다시 선택해주세요."
                   
    # 세번째 기능) 중복 메뉴 먹은 횟수 ============================================================================
    def food_count(self, _food):
        self.food = _food
        with open(same_count_list, mode='r', encoding='utf-8') as fp3:
            lines = fp3.readlines()
            # 지금까지 해당 메뉴를 먹었던 횟수를 표시하기 위한 기능: 이를 통해 유저는 새로운 메뉴를 생성하거나 다른 메뉴를 고를 수 있는 선택지를 가질 수도 있음.
            count = lines.count(f'{self.food}\n')
            print(f"{self.food}을/를 지금까지 {count}번 드셨습니다.")


    # 네번째 기능) 리스트 초기화 ============================================================================

    # 지금의 리스트가 마음에 안들시, 모아놓은 메뉴들의 food_list를 초기화.
    def delete_list(self):
        with open(filename, mode='w', encoding='utf-8') as fp:
            fp.write('')
        with open(same_count_list, mode='w', encoding='utf-8') as fp2:
            fp2.write('')


# 메뉴 결정 기능:
daedaek = input("대댁지 입력: ")
Menu = FoodChoice(daedaek)
print(Menu.choice())


# 메뉴 선택 횟수 표시 기능:
count_check = input("지금까지 몇번 먹었는지 확인 : ")
Menu.food_count(count_check)


# (선택) 모아놓은 메뉴 리스트 초기화:
refresh = input("지금까지 저장한 메뉴들, 먹은 리스트를 초기화 하려면 y 아니면 아무 키 입력 : ")
if refresh in ['y', 'ㅛ']:
    Menu.delete_list()
else:
    pass