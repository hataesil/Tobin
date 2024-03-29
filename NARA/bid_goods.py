#python 나라장터 입찰정보수집_20220710(ver_01) 20230725(ver_02)
#from msilib.schema import CheckBox
#import chromedriver_autoinstaller
from soupsieve import select
#chromedriver_autoinstaller.install()
from selenium import webdriver
from selenium.webdriver.chrome.service import Service #20230725
from webdriver_manager.chrome import ChromeDriverManager #20230724
from selenium.webdriver.common.by import By     #새롭게 추가
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import pandas as pd
import time
start = time.time()  #시작시간

try:
    chrome_options = webdriver.ChromeOptions() #20230725
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options) #20230725
    #driver = webdriver.Chrome(service=Service(),options=chrome_options) #20230725
    driver.get('https://www.g2b.go.kr:8101/ep/tbid/tbidFwd.do')

    #업무종류체크
    task_dict = {'물품': 'taskClCds1', '민간': 'taskClCds20', '기타': 'taskClCds4'}
    for task in task_dict.values():
        CheckBox = driver.find_element(By.ID,task)
        CheckBox.click()

    #검색조건체크
    option_dict = {'검색기간 1달':'setMonth1_1','입찰마감건 제외':'exceptEnd','검색건수 표시': 'useTotalCount'}
    for option in option_dict.values():
        CheckBox = driver.find_element(By.ID,option)
        CheckBox.click()

    # 목록수 100건 선택 (드롭다운)
    recordcountperpage = driver.find_element(By.NAME,'recordCountPerPage')
    selector = Select(recordcountperpage)
    selector.select_by_value('100')

    results = []  # 결과값을 저장할 리스트를 미리 만든다

    #검색어 입력   
    query1_list = ['ZOOM','windows server','windows os','운영체제','윈도우서버','업무용s/w']
    for query1 in query1_list:
        bidNm = driver.find_element(By.ID,'bidNm')
        bidNm.clear()
        bidNm.click()
        bidNm.send_keys(query1)
        bidNm.send_keys(Keys.ENTER)
        
        #참가지역제한 선택(드롭다운) 전국 00  대전 30 
        area_list = {'전국(제한없음)':'00','대전':'30'}
        for area in area_list:
            select = Select(driver.find_element(By.ID,'area'))
            select.select_by_visible_text(area)

            # 검색 버튼 클릭
            search_button = driver.find_element(By.CLASS_NAME,'btn_mdl')
            search_button.click()

            # 검색 결과 확인(변수지정)
            elem = driver.find_element(By.CLASS_NAME,'results')
            div_list = elem.find_elements(By.TAG_NAME,'div')

            #검색결과 리스트로 저장
            for div in div_list:
                results.append(div.text)

                kk = len(results) + 2
                if kk % 12 == 0 :
                    results.append(query1)
                    results.append(area) 
                    kk += 1    

            # 검색건수가 100건초과시 클릭
            inforight = driver.find_element(By.CLASS_NAME,'inforight')
            str_page = inforight.text
            var_page = str_page.replace("[검색건수 :","")
            num_page = var_page.replace("건]","")
            page = int(num_page)//100

            # 검색건수에 따른 조건문 실행
            if page >= 1 : 
                for i in range(2,page+2):  
                    #페이지 맨 아래로 스크롤
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
                    #다음페이지 클릭
                    xpath = '//*[@id="pagination"]/a['
                    xpath += str(i)
                    xpath += ']'
                    page_link = driver.find_element(By.XPATH,xpath).click() 

                    # 검색 결과 확인(변수지정)
                    elem = driver.find_element(By.CLASS_NAME,'results')
                    div_list = elem.find_elements(By.TAG_NAME,'div')
                    #검색결과 리스트로 저장 
                    for div in div_list:
                        results.append(div.text)
   
                        jj = len(results) + 2
                        if jj % 12 == 0:
                            results.append(query1)
                            results.append(area)                     
                            jj += 1

            # 검색화면으로 이동
            search_button = driver.find_element(By.CLASS_NAME,'btn_mdl')
            search_button.click()           

    #검색결과 모음 리스트를 12개씩 분할 새로운 리스트 생성
    result = [results[i * 12:(i + 1) * 12] for i in range((len(results) + 11) // 12)]            

    #pandas를 이용하여 결과 excel에 출력
    df = pd.DataFrame(result,columns=['업무','공고번호','분류','공고명','수요기관','공고기관','계약방법','입력일시','입찰마감일시','공동도급','업종구분','지역제한'])
    df.to_excel(excel_writer = "D:/BID/bidlist_goods.xlsx")
    print("time :", time.time() - start) #현재시각 - 시작시간

except Exception as e:
    print(e) 
    print("time :", time.time() - start) #현재시각 - 시작시간   
finally:
    driver.close()
