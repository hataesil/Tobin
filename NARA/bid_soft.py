#python 소포트웨어 수집
from msilib.schema import CheckBox
import chromedriver_autoinstaller
from soupsieve import select
chromedriver_autoinstaller.install()
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import pandas as pd
import time
start = time.time()  #시작시간

try:
    driver = webdriver.Chrome()
    #driver.get('https://www.g2b.go.kr:8101/ep/tbid/tbidFwd.do')
    driver.get('https://www.g2b.go.kr:8402/gtob/all/pr/estimate/fwdReqEstimateOpenCond.do')

    # 견적요청선택
    # side_list = driver.find_element_by_name('00084')
    # side_list.click()

    #업무종류체크
    task_dict = {'물품': 'bsnsDivCdSch1', '민간': 'bsnsDivCdSch4'}
    for task in task_dict.values():
        CheckBox = driver.find_element_by_id(task)
        CheckBox.click()

    #검색어 입력   
    # query1 = ""   #소프트웨어 검색시 사용
    # bidNm = driver.find_element_by_id('bidNm')
    # bidNm.click()
    # bidNm.send_keys(query1)
    # bidNm.send_keys(Keys.ENTER)

    #검색조건체크
    # option_dict = {'검색기간 1달':'setMonth1_1','입찰마감건 제외':'exceptEnd','검색건수 표시': 'useTotalCount'}
    # for option in option_dict.values():
    #     CheckBox = driver.find_element_by_id(option)
    #     CheckBox.click()

    # 출력목록수 50건 선택 (드롭다운)
    recordcountperpage = driver.find_element_by_name('recordCountPerPage')
    selector = Select(recordcountperpage)
    selector.select_by_value('100')
    
    results = []  # 결과값을 저장할 리스트를 미리 만든다

#     query2_list = ['1162','1164','1260']
# #    query2_list = ['1426','1468']  #소프트웨어  
#     for query2 in query2_list:
#         #업종선택
#         search_button = driver.find_element_by_xpath('//*[@id="search"]/table/tbody/tr[7]/td[1]/div/button[1]')
#         search_button.click()
#         #팝업창 제어
#         main_window, sub_window = driver.window_handles
#         #제어권을 서브로 이전
#         driver.switch_to.window(sub_window)
#         #업종검색
#         industrialCd = driver.find_element_by_id('industrialCd')
#         industrialCd.send_keys(query2)
#         search_button = driver.find_element_by_xpath('//*[@id="bt_search"]')
#         search_button.click()
#         rs_link = driver.find_element_by_css_selector('#ebid > div.results > table > tbody > tr > td:nth-child(4)')
#         rs_link.click()
#         #제어권을 메인으로 이전
#         driver.switch_to.window(main_window)

#         #참가지역제한 선택(드롭다운) 전국 00  대전 30 
#         area_list = {'전국(제한없음)':'00','대전':'30'}
#         for area in area_list:
#             select = Select(driver.find_element_by_id('area'))
#             select.select_by_visible_text(area)

            # 검색 버튼 클릭
    search_button = driver.find_element_by_class_name('btn_search')
    search_button.click()

            # 검색 결과 확인
    elem = driver.find_element_by_class_name('results')
    td_list = elem.find_elements_by_tag_name('td')

            #검색결과 리스트로 저장
    for td in td_list:
        results.append(td.text)
        a_tags = td.find_elements_by_tag_name('a')
        # if a_tags:
        #     for a_tag in a_tags:
        #         link = a_tag.get_attribute('href')
        #         results.append(link)          

            # 검색화면으로 이동
            # search_button = driver.find_element_by_class_name('btn_mdl')
            # search_button.click()

    #검색결과 모음 리스트를 12개씩 분할 새로운 리스트 생성
    result = [results[i * 8:(i + 1) * 8] for i in range((len(results) + 7) // 8)]            

    #pandas를 이용하여 결과 excel에 출력
    df = pd.DataFrame(result,columns=['구분','견적요청번호','분류','견적요청건명','제출마감일시','견적서제출','발주기관','대표품목'])
    df.to_excel(excel_writer = "D:\BID/bidlist_software.xlsx")
    print("time :", time.time() - start) #현재시각 - 시작시간 

except Exception as e:
    print(e)  
    print("time :", time.time() - start) #현재시각 - 시작시간   
finally:
    driver.close()
