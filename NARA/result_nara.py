#python 나라장터 입찰정보수집_20220210(ver_01) 20220421(Renewal) 20220915(result) 20231016(py 3.13)
#from msilib.schema import CheckBox(3.13이후사용안함)
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

    #검색유형(개찰결과)
    bidSearchType2 = driver.find_element(By .ID, 'bidSearchType2')
    bidSearchType2.click()

    #업무종류체크
    task_dict = {'용역': 'taskClCds5'} #,'민간': 'taskClCds20'
    for task in task_dict.values():
        CheckBox = driver.find_element(By.ID, task)
        CheckBox.click()

    #검색어 입력   
    #query1 = ""   #소프트웨어 검색시 사용
    #bidNm = driver.find_element(By.ID,'bidNm')
    #bidNm.click()
    #bidNm.send_keys(query1)
    #bidNm.send_keys(Keys.ENTER)

    #검색조건체크
    option_dict = {'검색기간 1달':'setMonth2_4','검색건수 표시': 'useTotalCount'}
    for option in option_dict.values():
        CheckBox = driver.find_element(By.ID, option)
        CheckBox.click()

    # 목록수 100건 선택 (드롭다운)
    recordcountperpage = driver.find_element(By.NAME, 'recordCountPerPage')
    selector = Select(recordcountperpage)
    selector.select_by_value('100')

    results = []  # 결과값을 저장할 리스트를 미리 만든다

    #query2_list = ['1162','1164','1260','1426','1468']
    query2_list = ['1162','1164','1260','9999']
    for query2 in query2_list:
        #업종선택
        search_button = driver.find_element(By.XPATH, '//*[@id="search"]/table/tbody/tr[7]/td[1]/div/button[1]')
        search_button.click()           #   //*[@id="resultForm"]/div[3]/div/a/span
        #팝업창 제어
        main_window, sub_window = driver.window_handles
        #제어권을 서브로 이전
        driver.switch_to.window(sub_window)
        #업종검색
        industrialCd = driver.find_element(By.ID, 'industrialCd')
        industrialCd.send_keys(query2)
        search_button = driver.find_element(By.XPATH, '//*[@id="bt_search"]')
        search_button.click()
        rs_link = driver.find_element(By.CSS_SELECTOR, '#ebid > div.results > table > tbody > tr > td:nth-child(4)')
        rs_link.click()
        #제어권을 메인으로 이전
        driver.switch_to.window(main_window)

        #참가지역제한 선택(드롭다운) 전국 00  대전 30 
        area_list = {'전국(제한없음)':'00','대전':'30'} 
        for area in area_list:
            select = Select(driver.find_element(By.ID,'area'))
            select.select_by_visible_text(area)

            # 검색 버튼 클릭
            search_button = driver.find_element(By.CLASS_NAME, 'btn_mdl')
            search_button.click()

            # 검색 결과 확인(변수지정)
            elem = driver.find_element(By.CLASS_NAME, 'results')
            div_list = elem.find_elements(By.TAG_NAME, 'div')

            #검색결과 리스트로 저장

            for div in div_list:
                results.append(div.text)
                # 용역구분과 지역구분 삽입
                #kk = len(results) + 2
                #if kk % 12 == 0 :
                #    results.append(query2)
                #    results.append(area) 
                #    kk += 1    

            # 검색건수가 100건초과시 클릭
            inforight = driver.find_element(By.CLASS_NAME, 'inforight')
            str_page = inforight.text
            var_page = str_page.replace("[검색건수 :","")
            num_page = var_page.replace("건]","")
            page = int(num_page)//100

            # 검색건수에 따른 조건문 실행
            if page >= 1 : 
                for i in range(2,page+2):  
                    #페이지 맨 아래로 스크롤
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
                    driver.find_element(By.LINK_TEXT, str(i)).click()  #다음페이지 선택
                    
                    # 검색 결과 확인(변수지정)
                    elem = driver.find_element(By.CLASS_NAME, 'results')
                    div_list = elem.find_elements(By.TAG_NAME, 'div')
                    #검색결과 리스트로 저장 
                    for div in div_list:
                        results.append(div.text)
                        # 용역구분과 지역구분 삽입
                        #jj = len(results) + 2    
                        #if jj % 12 == 0:
                        #    results.append(query2)
                        #    results.append(area)                     
                        #    jj += 1

            # 검색화면으로 이동
            search_button = driver.find_element(By.CLASS_NAME,'button4') #'btn_mdl'
            search_button.click()

    #검색결과 모음 리스트를 11개씩 분할 새로운 리스트 생성
    result = [results[i * 11:(i + 1) * 11] for i in range((len(results) + 10) // 11)]            
    # print(results, end=" " )

    #pandas를 이용하여 결과 excel에 출력
    df = pd.DataFrame(result,columns=['업무','공고번호','재입찰','공고명','수요기관','개찰일시','참가수','낙찰예정자','투찰금액','투찰율','진행상황'])
    df.to_excel(excel_writer = "D:/BID/resultlist_nara.xlsx")
    print("time :", time.time() - start) #현재시각 - 시작시간

except Exception as e:
    print(e) 
    print("time :", time.time() - start) #현재시각 - 시작시간   
finally:
    driver.close()
