from msilib.schema import CheckBox
import chromedriver_autoinstaller
from soupsieve import select
chromedriver_autoinstaller.install()

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
#from openpyxl import load_workbook
#import time
#import datetime
#import openpyxl
import pandas as pd

#엑셀파일 활성화
#workbook_name = 'bid_list.xlsx'
#wb = load_workbook(workbook_name)
#page = wb.active


try:
    driver = webdriver.Chrome()
    driver.get('https://www.g2b.go.kr:8101/ep/tbid/tbidFwd.do')


    #업무종류체크
    task_dict = {'용역': 'taskClCds5', '민간': 'taskClCds20', '기타': 'taskClCds4'}

    for task in task_dict.values():
        CheckBox = driver.find_element_by_id(task)
        CheckBox.click()

    #검색어 입력    
    query1 = ""
    bidNm = driver.find_element_by_id('bidNm')
    bidNm.click()
    bidNm.send_keys(query1)
    bidNm.send_keys(Keys.ENTER)

    #검색조건체크
    option_dict = {'검색기간 1달':'setMonth1_1','입찰마감건 제외':'exceptEnd','검색건수 표시': 'useTotalCount'}
    for option in option_dict.values():
        CheckBox = driver.find_element_by_id(option)
        CheckBox.click()

    # 목록수 100건 선택 (드롭다운)
    recordcountperpage = driver.find_element_by_name('recordCountPerPage')
    selector = Select(recordcountperpage)
    selector.select_by_value('100')
    
    #업종선택
    search_button = driver.find_element_by_xpath('//*[@id="search"]/table/tbody/tr[7]/td[1]/div/button[1]')
    search_button.click()

    #팝업창 제어
    main_window, sub_window = driver.window_handles

    #제어권을 서브로 이전
    driver.switch_to.window(sub_window)

    #업종검색
    query2 = '1162'
    industrialCd = driver.find_element_by_id('industrialCd')
    industrialCd.send_keys(query2)
    search_button = driver.find_element_by_xpath('//*[@id="bt_search"]')
    search_button.click()
    rs_link = driver.find_element_by_css_selector('#ebid > div.results > table > tbody > tr > td:nth-child(4)')
    rs_link.click()

    #제어권을 메인으로 이전
    driver.switch_to.window(main_window)

    #참가지역제한 선택(드롭다운) 전국 00  대전 30
    area_list = '00'
    for area in area_list:
        area = driver.find_element_by_name('area')
        selector = Select(area)
        selector.select_by_value('00')

    # 검색 버튼 클릭
    search_button = driver.find_element_by_class_name('btn_mdl')
    search_button.click()

    # 검색 결과 확인
    elem = driver.find_element_by_class_name('results')
    div_list = elem.find_elements_by_tag_name('div')
    
    #검색결과 리스트로 저장
    results = []
    for div in div_list:
        results.append(div.text)
        a_tags = div.find_elements_by_tag_name('a')

        if a_tags:
            for a_tag in a_tags:
                link = a_tag.get_attribute('href')
                results.append(link)          

    #검색결과 모음 리스트를 12개씩 분할 새로운 리스트 생성
    result = [results[i * 12:(i + 1) * 12] for i in range((len(results) + 11) // 12)]            
    #print(result)

    #pandas를 이용하여 결과 excel에 출력
    df = pd.DataFrame(result,columns=['업무','공고번호','공고번호링크','분류','공고명','공고명링크','수요기관','공고기관','계약방법','입력일시','입찰마감일시','공동수급'])
    #print(df)
    df.to_excel(excel_writer="bid_list.xlsx")

    #openpyxl 를 이용한 자료저장
    #page.append(result)
    #wb.save(filename=workbook_name)

except Exception as e:
    print(e)    

finally:
    driver.close()
    

