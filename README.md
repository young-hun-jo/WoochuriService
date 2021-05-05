# 🐮 우추리 축산 일일 매출 예측 프로젝트 🐷

## 🎯 프로젝트 목적
- 대전광역시 서구 도화공원길 21에 위치한 우추리 축산
- 2020년 2월 이후로 세계적으로 확산된 코로나 신종 바이러스로 인해 매출의 타격에 큰 영향을 입게 된 상태
- 머신 러닝을 활용하여 **일일 매출을 실시간으로 예측**해 정육 재고 관리를 최적화하고 최종적으로 **운영 비용 최소화 목적**

## 📋 데이터 명세서
- *우추리 축산 일 매출 데이터*
  * 영업 오픈일 2009-01-01 ~ 현재 까지의 일 매출 데이터
  * Excel 활용해 수기로 직접 수집
 
- *지상(종관, ASOS) 일자료 조회 서비스*
  * 공공 데이터 [Open API](https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15059093)
  * 평균기온
  * 최저기온
  * 최고기온
  * 1시간 최다강수량
  * 일 강수량
  * 평균풍속
  * 최대풍속
  * 평균상대습도
  * 최소상대습도
  * 1시간 최다일사량
  * 일사량
 
- *축산물등급판정 서비스*
  * 공공 데이터 [Open API](https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15058822)
  * 한우와 육우 도매 가격
    - 2009-01-01~2011-03-02 까지는 전국 도매 가격 
    - 2011-03-03~현재 까지는 중부권 도매 가격(대전이 중부권에 속함)
  * 돼지 탕박 도매 가격
    - 돼지 박피 도매 가격도 있었으나 현재 돼지고기의 약 97%가 돼지 탕박을 사용하기 때문에 박피 데이터는 제외
    - [돼지 탕박과 돼지 박피의 차이점](https://m.blog.naver.com/PostView.nhn?blogId=dsf-mall&logNo=221503684858&proxyReferer=https:%2F%2Fwww.google.com%2F)

## 🛠 데이터 전처리
- 결측치
  * 지상(종관, ASOS) 일자료 데이터
    - 해당 데이터 변수들은 서로 상관성이 높기 때문에 Pearson Correlation을 기반으로 하여 [KNN(K-Nearest-Neighbors) Imputer](https://scikit-learn.org/stable/modules/generated/sklearn.impute.KNNImputer.html) 사용
    
- 이상치
  * 한우와 육우 도매 가격
    - [한우 가격은 육우 가격의 약 1.8배](https://www.google.com/search?q=%EC%9C%A1%EC%9A%B0+%ED%95%9C%EC%9A%B0+%EA%B0%80%EA%B2%A9%EC%B0%A8%EC%9D%B4&oq=%ED%95%9C%EC%9A%B0+%EC%9C%A1%EC%9A%B0&aqs=chrome.4.69i57j69i59j35i39j0i8i30l4j69i61.3516j0j4&sourceid=chrome&ie=UTF-8)로 책정. 이를 이용해 로직 구현
    - 한우 가격이 잘못 책정된 날짜일 경우 ➡️ 해당 날짜의 육우가격을 이용해 이상치 대체
    - 육우 가격이 잘못 책정된 날짜일 경우 ➡️ 해당 날짜의 한우가격을 이용해 이상치 대체
 
 - 명절, 공휴일 파생변수 생성
  * 설, 추석 명절
    - 우추리 축산은 항상 명절 당일 직전날까지 영업 게시
    - EDA 결과, 명절 이벤트로 인해 명절 당일 직전날로부터 과거 6일간 매출이 평소와 다르게 매우 높은 것으로 관찰
    - [holidays](https://pypi.org/project/holidays/) 오픈소스를 이용해 대한민국의 명절 데이터를 미리 로드하고 해당 날짜로부터 미래 6일 이내에 명절 당일 직전날이 존재하면 가중치를 1부터 6까지 차등적으로 부여
      - 위와 같은 로직을 사용해 실시간 날짜에 명절 연휴 가중치를 부여할 수 있음
  
  * 일반 공휴일
    - 어린이날, 석가탄신일 등과 같이 일반 공휴일에도 평소와 다르게 높은 매출이 집계
    - 명절과 마찬가지로 동일한 로직 구현

## 🦾 예측 모델 성능 비교
- ``Train`` : 2009-01-01 ~ 2019-12-31
- ``Validation`` : 2020-01-01 ~ 2020-12-31(1일씩 교차검증 수행)
- ``Accuracy``: 오차(MAE)가 10만원 이하로 예측했으면 성공(1), 아니면 실패(0)로 계산하여 예측 정확도 성능 계산

|Model|Train MAPE|Test MAPE|
|---|---|---|
|[Prophet](https://facebook.github.io/prophet/)|51.80%|41.75%|
|ARIMA|63.25%|67.43%|
|Linear Regression|43.51%|52.20%|
|Polynomial Linear Regression(2 degree)|41.02%|49.41%|
|PLS Regression|44.68%|62.21%|
|Random Forest|11.10%|34.32%|
|XGBoost|28.41%|33.51%|
|LightGBM|22.19%|34.22%|
|LightGBM(PCA로 차원축소 )|25.50%|37.70%|
|Hybrid Voting(Random Forest+XGBoost+LightGBM)|20.20%|33.35%|
|LSTM(with Convolution)|37.31%|42.95%|

💡 최종 모델 : **Random Forest Regressor**<br>
💡 Optimal Hyper-parameter : ``n_estimators=100``, ``min_samples_split=2``<br>
💡 앞으로 일일 데이터를 계속 수집 후 학습할 것이므로 Train MAE가 가장 낮은 Random Forest 선정<br><br>
🧷 최종 모델 예측 그래프(**2009-01-01 ~ 2021-04-18**)<br>
<img width="745" alt="eval_res" src="https://user-images.githubusercontent.com/54783194/115231708-d3ee5680-a150-11eb-852c-f6f54aec7903.png">

## 📊 분석결과 보고서 작성
- [Notion](https://www.notion.so/4f3cf41bc515438095b3a79be8bc5f9d)

## 📟 자동화
- 예측하기 전 전일 우추리 축산 매출과 휴무 여부를 ``today_sale`` 변수와 ``remark_str``에 입력
- 예측하려는 날 오전 8시, 오전 11시에 2차례 ``main.py`` 수행
- 유닉스 계열 Mac OS 시간 기반 잡 스케줄러 [cron](https://www.letmecompile.com/scheduler-cron-tutorial/) 이용
- 예측값을 SMS로 전달하기 위해 소정의 유료 SMS 발송 플랫폼 [twiliow](https://www.twilio.com/) 활용
```python
from model import WoochuriPredModel
from twilio.rest import Client
import pandas as pd
print('예측하려는 날짜:', pd.Timestamp.now())

# Load updated crawling dataset and modeling to predict tomorrow's sale
# Setting parameters using local MySQL id, password
user, password = 'root', 'your password'
end_time = (pd.Timestamp.now() - pd.Timedelta(days=1)).strftime("%Y-%m-%d")

# run crawling, preprocess datasets, and finally prediction at one time
PredModel = WoochuriPredModel(user=user, password=password, end_time=end_time,
                              today_sale=682100, remark='평일')
FinalDataset = PredModel.execute()
result = PredModel.run(FinalDataset)

# Sending message
account_sid = 'AC8f9d9f4c8983ee648153f5347ee027a9'
auth_token = 'your_auth_token'  # customize your_auth_token
client = Client(account_sid, auth_token)

woochuri_master = '+821094125854'
message = client.messages.create(from_='+13132543287', body=result, to=woochuri_master)
print(message.sid)
```

## ⚙️ Stack
<img width="639" alt="스크린샷 2021-03-29 오후 5 09 47" src="https://user-images.githubusercontent.com/54783194/112806291-95193380-90b1-11eb-9e6a-2b4934ea0080.png"><br>
- Python 3.7.7
- BeautifulSoup 4.6.0
- MySQL 8.0.21(pymysql 1.0.2)
- Pandas
- Numpy
- Scikit-learn 0.24.1
- Tensorflow 2.x
- PowerPoint
- IDE: PyCharm, Jupyter notebook

## 📌 [twiliow 사용법](https://pypi.org/project/twilio/)
- 다음 명령어를 터미널에서 입력 후 다운로드
<br>```pip install twilio```<br>
- twilio 가입 후 twilio 웹 브라우저 console로 이동해 ``account_sid``와 ``auth_token`` 확인 후 ``main.py`` 파일과 동일한 코드로 메세지 전송
