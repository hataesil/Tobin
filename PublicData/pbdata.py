# 조달청 입찰공고정보 #
import requests

url = 'http://apis.data.go.kr/1230000/BidPublicInfoService02'
params ={'serviceKey' : 'eyfwZsSUETBvnMtwKmZkUSLwBI5mOnNAc5pu9XxCAkdbfqAhY5JlGtTA7ysGMiyz%2BawYWdxcSiSwf1uOc9wIUQ%3D%3D', 'numOfRows' : '10', 'pageNo' : '1', 'inqryDiv' : '1', 'inqryBgnDt' : '20220101001', 'inqryEndDt' : '20220131900', 'bidNtceNo' : '20220131900', 'type' : 'json' }

response = requests.get(url, params=params)
print(response.content)

