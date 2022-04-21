import os
import django

from selenium import webdriver
from django.conf import settings
from datetime import datetime
from bs4 import BeautifulSoup
from django.utils.timezone import make_aware

def text_strip(text):
    return ' '.join(text.split())

if __name__ == "__main__":

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MarketPlace.settings')
    django.setup()

    from bids.models import RequestInfo

    # Chrome의 경우 | 아까 받은 chromedriver의 위치를 지정해준다.
    if settings.DEBUG == True:
        driver = webdriver.Chrome('chrome/chromedriver_mac')
    else:
        driver = webdriver.Chrome('chrome/chromedriver_linux')

    driver.implicitly_wait(2)

    # URL 읽어 오기
    driver.get('http://www.g2b.go.kr:8401/gtob/all/pr/estimate/fwdReqEstimateOpenCond.do')

    # 물품을 선택하고, 목록을 100개로 늘림
    driver.find_element_by_id('bsnsDivCdSch1').click()
    select = driver.find_element_by_id('recordCountPerPage')
    allOptions = select.find_elements_by_tag_name("option")
    for option in allOptions:
        if option.get_attribute("value") == '100':
            option.click()
    driver.execute_script("return toSearch('main');")
    driver.implicitly_wait(5)

    # Html 을 읽어 들이고 분석을 함
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    trs = soup.find_all('tr')

    for tr in trs:
        td_list = tr.find_all('td')

        try:
            orderno = td_list[0].text
            orderno = int(orderno)

            try:
                req = RequestInfo.objects.get(reqno=orderno)
            except Exception as ex:

                # 해당 콘텐츠가 DB에 없는 경우 저장을 함
                print("Searching : ", orderno)
                link_href = "javascript:toEstimateDetail('{}','Y');".format(orderno)
                driver.execute_script(link_href)

                driver.implicitly_wait(5)

                page = driver.page_source
                soup = BeautifulSoup(page, 'html.parser')

                props = {
                    text_strip(tag1.text): text_strip(tag2.text) for tag1, tag2 in zip(soup.select('table th'), soup.select('table td'))
                }
                print(props)

                docno = props['문서번호']
                name = props['견적건명']
                org = props['기관명']
                contact = props['담당자']
                end_at = props['견적마감일']
                end_at = make_aware(datetime.strptime(end_at, "%Y/%m/%d %H:%M"))

                req_at = props['요청일자']
                req_at = make_aware(datetime.strptime(req_at, "%Y/%m/%d %H:%M"))

                phone = props['전화/팩스']
                ptype = props['업무구분']


                category = props['1']
                catno = props['물품분류명']
                product = props['물품식별명']
                prdno = props['물품식별번호']

                qty = props['물품식별번호']
                delivery_at = props['수량'][:10]
                delivery_at = datetime.strptime(delivery_at, "%Y/%m/%d")

                delivery_cond = props['납품기한(일수)']
                delivery_place = props['인도조건']

                try:
                    reqinfo = RequestInfo.objects.create(reqno=orderno, docno=docno, name=name,
                            org=org, end_at=end_at, req_at=req_at, contact=contact,
                            phone=phone)

                    print(reqinfo)

                    reqinfo.product.category = category
                    reqinfo.product.catno = catno
                    reqinfo.product.product = product
                    reqinfo.product.prdno = prdno
                    reqinfo.product.qty = qty
                    reqinfo.product.delivery_at = delivery_at
                    reqinfo.product.delivery_cond = delivery_cond
                    reqinfo.product.delivery_place = delivery_place

                    reqinfo.product.save()
                    print(reqinfo.product)

                except Exception as ex:
                    print("ex : ", ex)

        except Exception as ex:
            print("Error : ", ex)


    driver.quit()
