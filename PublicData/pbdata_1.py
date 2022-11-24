# 조달청 입찰공고정보 #
import requests
from bs4 import BeautifulSoup
import urllib
from urllib import parse
from datetime import datetime, timedelta, date
import re
import math
import pandas as pd
import json


today = date.today()
start = re.sub('-','',str(today - timedelta(days=60)))
end = re.sub('-','',str(today))

priceUp = 2000000
priceDown = 20000000000
key = 'eyfwZsSUETBvnMtwKmZkUSLwBI5mOnNAc5pu9XxCAkdbfqAhY5JlGtTA7ysGMiyz%2BawYWdxcSiSwf1uOc9wIUQ%3D%3D'

link='http://apis.data.go.kr/1230000/BidPublicInfoService/getBidPblancListInfoServcPPSSrch?type=json&inqryDiv=1&dminsttNm='+parse.quote('해양수산부')+'&inqryBgnDt='+start+'&inqryEndDt='+end+'&pageNo=1&numOfRows=1&ServiceKey='+key
url = parse.urlparse(link) 
query = parse.parse_qs(url.query)
base='http://apis.data.go.kr/1230000/BidPublicInfoService/getBidPblancListInfoServcPPSSrch?'
link=base+parse.urlencode(query, doseq=True)

request=urllib.request.urlopen(link).read().decode('utf-8')
n=math.ceil(json.loads(request)['response']['body']['totalCount']*.1)
n

page=1
link='http://apis.data.go.kr/1230000/BidPublicInfoService/getBidPblancListInfoServcPPSSrch?type=json&inqryDiv=1&dminsttNm='+parse.quote('해양수산부')+'&inqryBgnDt='+start+'&inqryEndDt='+end+'&pageNo='+str(page)+'&numOfRows=10&ServiceKey='+key
url = parse.urlparse(link) 
query = parse.parse_qs(url.query)
link=base+parse.urlencode(query, doseq=True)
request=urllib.request.urlopen(link).read().decode('utf-8')
df = pd.DataFrame(json.loads(request)['response']['body']['items'])
df2=df[['bidNtceNm','asignBdgtAmt','bidBeginDt','bidClseDt','opengDt','bidMethdNm','cntrctCnclsMthdNm','dminsttNm','dminsttCd','bidNtceNo','reNtceYn','ntceKindNm','bidNtceDtlUrl']]
df2.rename(columns = {'asignBdgtAmt' : '배정예산','bidNtceNm':'공고명','bidBeginDt':'입찰개시일','bidClseDt':'입찰마감일'
                  ,'opengDt':'개찰일시','bidMethdNm':'입찰방식','cntrctCnclsMthdNm':'계약체결방법','dminsttCd':'수요기관코드'
                 ,'dminsttNm':'수요기관명','bidNtceNo':'입찰공고번호','reNtceYn':'재공고여부','ntceKindNm':'공고종류','bidNtceDtlUrl':'링크'}, inplace = True)
data=df2



