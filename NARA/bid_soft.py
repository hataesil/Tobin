#python 소포트웨어 수집  20230725(ver_02)
#from msilib.schema import CheckBox #20231013 python 3.13이후에는 사용안함
#import chromedriver_autoinstaller
#from soupsieve import select #20231013
#chromedriver_autoinstaller.install()
from selenium import webdriver
from selenium.webdriver.chrome.service import Service #20230725
from webdriver_manager.chrome import ChromeDriverManager #20230724
from selenium.webdriver.common.by import By     #새롭게 추가
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import pandas as pd
import time
start = time.time()  #시작시간


try:
    chrome_options = webdriver.ChromeOptions() #20230725
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options) #20230725
    #driver = webdriver.Chrome(service=Service(),options=chrome_options) #20230725
    driver.get('https://www.g2b.go.kr:8402/gtob/all/pr/estimate/fwdReqEstimateOpenCond.do')

    #업무종류체크
    task_dict = {'물품': 'bsnsDivCdSch1', '민간': 'bsnsDivCdSch4'}
    for task in task_dict.values():
        CheckBox = driver.find_element(By.ID,task)
        CheckBox.click()


    # 출력목록수 50건 선택 (드롭다운)
    recordcountperpage = driver.find_element(By.NAME,'recordCountPerPage')
    selector = Select(recordcountperpage)
    selector.select_by_value('100')
    
    results = []  # 결과값을 저장할 리스트를 미리 만든다


    # 검색 버튼 클릭
    search_button = driver.find_element(By.CLASS_NAME,'btn_search')
    search_button.click()

            # 검색 결과 확인
    elem = driver.find_element(By.CLASS_NAME,'results')
    td_list = elem.find_elements(By.TAG_NAME,'td')

            #검색결과 리스트로 저장
    for td in td_list:
        results.append(td.text)
        a_tags = td.find_elements(By.TAG_NAME,'a')


    #검색결과 모음 리스트를 12개씩 분할 새로운 리스트 생성
    result = [results[i * 8:(i + 1) * 8] for i in range((len(results) + 7) // 8)]            

    #pandas를 이용하여 결과 excel에 출력
    df = pd.DataFrame(result,columns=['구분','견적요청번호','분류','견적요청건명','제출마감일시','견적서제출','발주기관','대표품목'])
    df.to_excel(excel_writer = "D:/BID/bidlist_software.xlsx")
    print("time :", time.time() - start) #현재시각 - 시작시간 

except Exception as e:
    print(e)  
    print("time :", time.time() - start) #현재시각 - 시작시간   
finally:
    driver.close()
