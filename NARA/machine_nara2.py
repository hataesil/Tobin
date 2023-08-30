import requests
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# 나라장터 API 키를 설정합니다.
API_KEY = "amqB+UIFid4xMglQUJtz4misDuSk6b6AVgG4AWQp842+rQyn8QPx4NarGI+ed4F9PTtZquFLfg0gv6y7ta+SCA=="

# 나라장터에서 입찰 결과를 수집합니다.
url = "https://api.g2b.go.kr/openapi/service/rest/289/getBiddingList"
params = {
    "serviceKey": API_KEY,
    "pageNo": 1,
    "numOfRows": 100,
    "biddingType": "2"
}
response = requests.get(url, params=params)
data = response.json()

# 수집된 데이터를 DataFrame에 저장합니다.
df = pd.DataFrame(data["data"]["row"])

# 투찰율을 계산합니다.
df["bidRate"] = df["bidAmount"] / df["estimatedAmount"]

# 투찰율을 예측하는 선형 회귀 모델을 학습합니다.
model = LinearRegression()
model.fit(df[["bidAmount", "estimatedAmount"]], df["bidRate"])

# 입찰 결과를 입력하면 투찰율을 예측합니다.
bid_amount = 1000000
estimated_amount = 2000000
bid_rate = model.predict([[bid_amount, estimated_amount]])

# 예측 결과를 출력합니다.
print("투찰율:", bid_rate)
