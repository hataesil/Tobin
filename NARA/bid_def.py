#python 나라장터 입찰정보수집_20220210(ver_01) 20220421(Renewal)
#import chromedriver_autoinstaller
#import chromedriver_autoinstaller
from soupsieve import select #20231013
#chromedriver_autoinstaller.install()
from selenium import webdriver
from selenium.webdriver.chrome.service import Service #20230725
from webdriver_manager.chrome import ChromeDriverManager #20230724
from selenium.webdriver.common.by import By     #새롭게 추가
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import pandas as pd
import time, os
start = time.time()  #시작시간

try:
    chrome_options = webdriver.ChromeOptions() #20230725
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options) #20230725
    #driver = webdriver.Chrome(service=Service(),options=chrome_options) #20230725
    driver.get('https://www.d2b.go.kr/psb/bid/serviceBidAnnounceList.do?key=32')

    date_divs = driver.find_element(By.NAME,'date_divs')
    selector = Select(date_divs)
    selector.select_by_value('0')

    xldown = driver.find_element(By.ID,'btn_excel_down')
    xldown.click()

    time.sleep(5)

    os.rename('C:/Users/USER/Downloads/입찰공고목록.xls','C:/Users/USER/Downloads/bid_def.xls')

    print("time :", time.time() - start) #현재시각 - 시작시간

except Exception as e:
    print(e) 
    print("time :", time.time() - start) #현재시각 - 시작시간   
finally:
    driver.close()
