#-*- encoding: utf-8 -*-
import requests, json, os, csv, math
import pandas as pd
import numpy as np
from urllib.parse import urlencode, unquote

indstry_Cd = ['1162','1164','1260']
prtcptLmtRgn_Cd = ['00','30']               #전국00 대전30

url = 'http://apis.data.go.kr/1230000/ad/BidPublicInfoService/getBidPblancListInfoServcPPSSrch'   #용역개찰결과 2025

#전체 데이터를 저장할 객체 선언
df = pd.DataFrame()

indstry_Cd =['1162','1164','1260']
prtcptLmtRgn_Cd = ['00','30']
inqryBgn_Dt = '202502010000'  
inqryEnd_Dt = '202502282359'

#오픈 API 호출을 총 오픈 API 호출 회수 만큼 반복 실행
for i in indstry_Cd:
        for j in prtcptLmtRgn_Cd:
                queryString = "?" + urlencode(
                        {'serviceKey' : 'CYbbRD03Ax46XrHUnk1RvZfXcxTbGrYVxSGxVWZ97Zobcwo1VVp4exGI4kb8Z9HHtKajWbwnXnTCXwHeDGZe4Q==',
                        'pageNo' : '1',
                        'numOfRows' : '100',       
                        'inqryDiv' : '1', 
                        'inqryBgnDt' : inqryBgn_Dt, 
                        'inqryEndDt' : inqryEnd_Dt,
                        'indstrytyCd' : i,
                        'prtcptLmtRgnCd' : j,
                        'bidClseExcpYn' : 'Y',
                        'type' : 'json'
                        }  
                )

                queryURL = url + queryString
                response = requests.get(queryURL)
                r_dic = json.loads(response.text)
                doc = r_dic['response']['body']['items']
                df = pd.concat([df, pd.DataFrame(doc)], axis=0, ignore_index=True)
                # df_2=df_1.assign(indstry_Cd=i,prtcptLmtRgn_Cd=j)

        queryURL = url + queryString
        response = requests.get(queryURL)
        r_dic = json.loads(response.text)
        doc = r_dic['response']['body']['items']
        df = pd.concat([df, pd.DataFrame(doc)], axis=0, ignore_index=True)
        # df_2 = df_1.assign(indstry_Cd=i,prtcptLmtRgn_Cd=j)

#CSV화일로 저장
# df.to_csv('D:/BID/bidlist_00.csv')
# df.drop_duplicates()
# df.to_csv('bidlistsort00.csv')
# df = pd.DataFrame(result,columns=['업무','공고번호','분류','공고명','수요기관','공고기관','계약방법','입력일시','입찰마감일시','공동도급','업종구분','지역제한'])
# df.to_excel(excel_writer = "D:/BID/bidlist/bidlist_nara.xlsx")
# print("Bid_nara_time :", time.time() - start) #현재시각 - 시작시간
# results.clear()
# result.clear()
# http://apis.data.go.kr/1230000/ad/BidPublicInfoService/getBidPblancListInfoServcPPSSrch?serviceKey=CYbbRD03Ax46XrHUnk1RvZfXcxTbGrYVxSGxVWZ97Zobcwo1VVp4exGI4kb8Z9HHtKajWbwnXnTCXwHeDGZe4Q==&pageNo=1&numOfRows=100&inqryDiv=1&inqryBgnDt=202502010000&inqryEndDt=202502282359&indstrytyCd=1162&prtcptLmtRgnCd=00&bidClseExcpYn=N&type=json
# df.to_csv(output_path, mode='a', header=not os.path.exists(output_path))

# 특정 컬럼 추출
df = df[['bidNtceNo','bidNtceOrd','bidNtceNm','bidBeginDt','bidClseDt','sucsfbidLwltRate']]

# 중복행 삭제
df.drop_duplicates(subset=None, keep='first', inplace=True, ignore_index=True)

df = df.set_index('bidNtceNo')

# 화일에 데이터를 추가하도록 함
output_path = 'bidlist202502.csv'
# df.to_csv ('bidlist202502.csv', index='False' )
df.to_csv(output_path, mode='a', header=not os.path.exists(output_path))

# df_1.to_excel(excel_writer='bidlist202502.xlsx')
df.to_excel(excel_writer='bidlist202502.xlsx',sheet_name='DATA_sheet')

#del [df_2]]
del [df]
