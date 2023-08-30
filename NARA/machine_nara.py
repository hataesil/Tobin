import requests

url = 'http://apis.data.go.kr/1230000/ScsbidInfoService/getScsbidListSttusThng'
params ={'serviceKey' : 'amqB+UIFid4xMglQUJtz4misDuSk6b6AVgG4AWQp842+rQyn8QPx4NarGI+ed4F9PTtZquFLfg0gv6y7ta+SCA==', 'numOfRows' : '10', 'pageNo' : '1', 'inqryDiv' : '1', 'inqryBgnDt' : '202305010000', 'inqryEndDt' : '202305051234', 'bidNtceNo' : '20230439522', 'type' : 'json' }
# params ={'serviceKey' : 'amqB+UIFid4xMglQUJtz4misDuSk6b6AVgG4AWQp842+rQyn8QPx4NarGI+ed4F9PTtZquFLfg0gv6y7ta+SCA==', 'numOfRows' : '10', 'pageNo' : '1', 'inqryDiv' : '1', 'inqryBgnDt' : '201605010000', 'inqryEndDt' : '201605052359', 'bidNtceNo' : '20160439522', 'type' : 'json' }

response = requests.get(url, params=params)
print(response.content)
