# ๐ฎ ์ฐ์ถ๋ฆฌ ์ถ์ฐ ์ผ์ผ ๋งค์ถ ์์ธก ํ๋ก์ ํธ ๐ท

## ๐ฏ ํ๋ก์ ํธ ๋ชฉ์ 
- ๋์ ๊ด์ญ์ ์๊ตฌ ๋ํ๊ณต์๊ธธ 21์ ์์นํ ์ฐ์ถ๋ฆฌ ์ถ์ฐ
- 2020๋ 2์ ์ดํ๋ก ์ธ๊ณ์ ์ผ๋ก ํ์ฐ๋ ์ฝ๋ก๋ ์ ์ข ๋ฐ์ด๋ฌ์ค๋ก ์ธํด ๋งค์ถ์ ํ๊ฒฉ์ ํฐ ์ํฅ์ ์๊ฒ ๋ ์ํ
- ๋จธ์  ๋ฌ๋์ ํ์ฉํ์ฌ **์ผ์ผ ๋งค์ถ์ ์ค์๊ฐ์ผ๋ก ์์ธก**ํด ์ ์ก ์ฌ๊ณ  ๊ด๋ฆฌ๋ฅผ ์ต์ ํํ๊ณ  ์ต์ข์ ์ผ๋ก **์ด์ ๋น์ฉ ์ต์ํ ๋ชฉ์ **

## ๐ ๋ฐ์ดํฐ ๋ช์ธ์
- *์ฐ์ถ๋ฆฌ ์ถ์ฐ ์ผ ๋งค์ถ ๋ฐ์ดํฐ*
  * ์์ ์คํ์ผ 2009-01-01 ~ ํ์ฌ ๊น์ง์ ์ผ ๋งค์ถ ๋ฐ์ดํฐ
  * Excel ํ์ฉํด ์๊ธฐ๋ก ์ง์  ์์ง
 
- *์ง์(์ข๊ด, ASOS) ์ผ์๋ฃ ์กฐํ ์๋น์ค*
  * ๊ณต๊ณต ๋ฐ์ดํฐ [Open API](https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15059093)
  * ํ๊ท ๊ธฐ์จ
  * ์ต์ ๊ธฐ์จ
  * ์ต๊ณ ๊ธฐ์จ
  * 1์๊ฐ ์ต๋ค๊ฐ์๋
  * ์ผ ๊ฐ์๋
  * ํ๊ท ํ์
  * ์ต๋ํ์
  * ํ๊ท ์๋์ต๋
  * ์ต์์๋์ต๋
  * 1์๊ฐ ์ต๋ค์ผ์ฌ๋
  * ์ผ์ฌ๋
 
- *์ถ์ฐ๋ฌผ๋ฑ๊ธํ์  ์๋น์ค*
  * ๊ณต๊ณต ๋ฐ์ดํฐ [Open API](https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15058822)
  * ํ์ฐ์ ์ก์ฐ ๋๋งค ๊ฐ๊ฒฉ
    - 2009-01-01~2011-03-02 ๊น์ง๋ ์ ๊ตญ ๋๋งค ๊ฐ๊ฒฉ 
    - 2011-03-03~ํ์ฌ ๊น์ง๋ ์ค๋ถ๊ถ ๋๋งค ๊ฐ๊ฒฉ(๋์ ์ด ์ค๋ถ๊ถ์ ์ํจ)
  * ๋ผ์ง ํ๋ฐ ๋๋งค ๊ฐ๊ฒฉ
    - ๋ผ์ง ๋ฐํผ ๋๋งค ๊ฐ๊ฒฉ๋ ์์์ผ๋ ํ์ฌ ๋ผ์ง๊ณ ๊ธฐ์ ์ฝ 97%๊ฐ ๋ผ์ง ํ๋ฐ์ ์ฌ์ฉํ๊ธฐ ๋๋ฌธ์ ๋ฐํผ ๋ฐ์ดํฐ๋ ์ ์ธ
    - [๋ผ์ง ํ๋ฐ๊ณผ ๋ผ์ง ๋ฐํผ์ ์ฐจ์ด์ ](https://m.blog.naver.com/PostView.nhn?blogId=dsf-mall&logNo=221503684858&proxyReferer=https:%2F%2Fwww.google.com%2F)

## ๐  ๋ฐ์ดํฐ ์ ์ฒ๋ฆฌ
- ๊ฒฐ์ธก์น
  * ์ง์(์ข๊ด, ASOS) ์ผ์๋ฃ ๋ฐ์ดํฐ
    - ํด๋น ๋ฐ์ดํฐ ๋ณ์๋ค์ ์๋ก ์๊ด์ฑ์ด ๋๊ธฐ ๋๋ฌธ์ Pearson Correlation์ ๊ธฐ๋ฐ์ผ๋ก ํ์ฌ [KNN(K-Nearest-Neighbors) Imputer](https://scikit-learn.org/stable/modules/generated/sklearn.impute.KNNImputer.html) ์ฌ์ฉ
    
- ์ด์์น
  * ํ์ฐ์ ์ก์ฐ ๋๋งค ๊ฐ๊ฒฉ
    - [ํ์ฐ ๊ฐ๊ฒฉ์ ์ก์ฐ ๊ฐ๊ฒฉ์ ์ฝ 1.8๋ฐฐ](https://www.google.com/search?q=%EC%9C%A1%EC%9A%B0+%ED%95%9C%EC%9A%B0+%EA%B0%80%EA%B2%A9%EC%B0%A8%EC%9D%B4&oq=%ED%95%9C%EC%9A%B0+%EC%9C%A1%EC%9A%B0&aqs=chrome.4.69i57j69i59j35i39j0i8i30l4j69i61.3516j0j4&sourceid=chrome&ie=UTF-8)๋ก ์ฑ์ . ์ด๋ฅผ ์ด์ฉํด ๋ก์ง ๊ตฌํ
    - ํ์ฐ ๊ฐ๊ฒฉ์ด ์๋ชป ์ฑ์ ๋ ๋ ์ง์ผ ๊ฒฝ์ฐ โก๏ธ ํด๋น ๋ ์ง์ ์ก์ฐ๊ฐ๊ฒฉ์ ์ด์ฉํด ์ด์์น ๋์ฒด
    - ์ก์ฐ ๊ฐ๊ฒฉ์ด ์๋ชป ์ฑ์ ๋ ๋ ์ง์ผ ๊ฒฝ์ฐ โก๏ธ ํด๋น ๋ ์ง์ ํ์ฐ๊ฐ๊ฒฉ์ ์ด์ฉํด ์ด์์น ๋์ฒด
 
 - ๋ช์ , ๊ณตํด์ผ ํ์๋ณ์ ์์ฑ
  * ์ค, ์ถ์ ๋ช์ 
    - ์ฐ์ถ๋ฆฌ ์ถ์ฐ์ ํญ์ ๋ช์  ๋น์ผ ์ง์ ๋ ๊น์ง ์์ ๊ฒ์
    - EDA ๊ฒฐ๊ณผ, ๋ช์  ์ด๋ฒคํธ๋ก ์ธํด ๋ช์  ๋น์ผ ์ง์ ๋ ๋ก๋ถํฐ ๊ณผ๊ฑฐ 6์ผ๊ฐ ๋งค์ถ์ด ํ์์ ๋ค๋ฅด๊ฒ ๋งค์ฐ ๋์ ๊ฒ์ผ๋ก ๊ด์ฐฐ
    - [holidays](https://pypi.org/project/holidays/) ์คํ์์ค๋ฅผ ์ด์ฉํด ๋ํ๋ฏผ๊ตญ์ ๋ช์  ๋ฐ์ดํฐ๋ฅผ ๋ฏธ๋ฆฌ ๋ก๋ํ๊ณ  ํด๋น ๋ ์ง๋ก๋ถํฐ ๋ฏธ๋ 6์ผ ์ด๋ด์ ๋ช์  ๋น์ผ ์ง์ ๋ ์ด ์กด์ฌํ๋ฉด ๊ฐ์ค์น๋ฅผ 1๋ถํฐ 6๊น์ง ์ฐจ๋ฑ์ ์ผ๋ก ๋ถ์ฌ
      - ์์ ๊ฐ์ ๋ก์ง์ ์ฌ์ฉํด ์ค์๊ฐ ๋ ์ง์ ๋ช์  ์ฐํด ๊ฐ์ค์น๋ฅผ ๋ถ์ฌํ  ์ ์์
  
  * ์ผ๋ฐ ๊ณตํด์ผ
    - ์ด๋ฆฐ์ด๋ , ์๊ฐํ์ ์ผ ๋ฑ๊ณผ ๊ฐ์ด ์ผ๋ฐ ๊ณตํด์ผ์๋ ํ์์ ๋ค๋ฅด๊ฒ ๋์ ๋งค์ถ์ด ์ง๊ณ
    - ๋ช์ ๊ณผ ๋ง์ฐฌ๊ฐ์ง๋ก ๋์ผํ ๋ก์ง ๊ตฌํ

## ๐ฆพ ์์ธก ๋ชจ๋ธ ์ฑ๋ฅ ๋น๊ต
- ``Train`` : 2009-01-01 ~ 2020-05-03
- ``Validation`` : 2020-05-04 ~ 2021-05-04(1์ผ์ฉ ๊ต์ฐจ๊ฒ์ฆ ์ํ)
- ``MAPE``: ์์ธก๊ฐ์ด ์ค์ ๊ฐ๊ณผ์ ์ฐจ์ด๊ฐ ์ผ๋ง๋ ์ฐจ์ด๋๋์ง์ ๋ํ ๋น์จ

|Model|Train MAPE|Test MAPE|
|---|---|---|
|[Prophet](https://facebook.github.io/prophet/)|51.80%|41.75%|
|ARIMA|63.25%|67.43%|
|Linear Regression|43.51%|52.20%|
|Polynomial Linear Regression(2 degree)|41.02%|49.41%|
|PLS Regression|44.68%|62.21%|
|<b>Random Forest</b>|<b>11.10%</b>|<b>34.32%</b>|
|XGBoost|28.41%|33.51%|
|LightGBM|22.19%|34.22%|
|LightGBM(PCA๋ก ์ฐจ์์ถ์ )|25.50%|37.70%|
|Hybrid Voting(Random Forest+XGBoost+LightGBM)|20.20%|33.35%|
|LSTM(with Convolution)|37.31%|42.95%|

๐ก ์ต์ข ๋ชจ๋ธ : **Random Forest Regressor**<br>
๐ก Optimal Hyper-parameter : ``n_estimators=100``, ``min_samples_split=2``<br>
๐ก ์์ผ๋ก ์ผ์ผ ๋ฐ์ดํฐ๋ฅผ ๊ณ์ ์์ง ํ ํ์ตํ  ๊ฒ์ด๋ฏ๋ก Train MAE๊ฐ ๊ฐ์ฅ ๋ฎ์ Random Forest ์ ์ <br><br>
๐งท ์ต์ข ๋ชจ๋ธ ์์ธก ๊ทธ๋ํ(**2009-01-01 ~ 2021-05-04**)<br>
<img width="719" alt="graph" src="https://user-images.githubusercontent.com/54783194/117105567-47cb6880-adb9-11eb-9b79-47c4b1b14572.png">

## ๐ ๋ถ์๊ฒฐ๊ณผ ๋ณด๊ณ ์ ์์ฑ
- [Notion](https://www.notion.so/4f3cf41bc515438095b3a79be8bc5f9d)

## ๐ ์๋ํ
- ์์ธกํ๊ธฐ ์  ์ ์ผ ์ฐ์ถ๋ฆฌ ์ถ์ฐ ๋งค์ถ๊ณผ ํด๋ฌด ์ฌ๋ถ๋ฅผ ``today_sale`` ๋ณ์์ ``remark``์ ์๋ ฅ
- ์์ธกํ๋ ค๋ ๋  ์ค์  8์, ์ค์  11์์ 2์ฐจ๋ก ``main.py`` ์ํ
- ์ ๋์ค ๊ณ์ด Mac OS ์๊ฐ ๊ธฐ๋ฐ ์ก ์ค์ผ์ค๋ฌ [cron](https://www.letmecompile.com/scheduler-cron-tutorial/) ์ด์ฉ
- ์์ธก๊ฐ์ SMS๋ก ์ ๋ฌํ๊ธฐ ์ํด ์์ ์ ์ ๋ฃ SMS ๋ฐ์ก ํ๋ซํผ [twiliow](https://www.twilio.com/) ํ์ฉ
```python
from model import WoochuriPredModel
from twilio.rest import Client
import pandas as pd
print('์์ธกํ๋ ค๋ ๋ ์ง:', pd.Timestamp.now())

# Load updated crawling dataset and modeling to predict tomorrow's sale
# Setting parameters using local MySQL id, password
user, password = 'root', 'your password'
end_time = (pd.Timestamp.now() - pd.Timedelta(days=1)).strftime("%Y-%m-%d")

# run crawling, preprocess datasets, and finally prediction at one time
PredModel = WoochuriPredModel(user=user, password=password, end_time=end_time,
                              today_sale='must be integer', remark='ํ์ผ')
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

## โ๏ธ Stack
<img width="639" alt="แแณแแณแแตแซแแฃแบ 2021-03-29 แแฉแแฎ 5 09 47" src="https://user-images.githubusercontent.com/54783194/112806291-95193380-90b1-11eb-9e6a-2b4934ea0080.png"><br>
- Python 3.7.7
- BeautifulSoup 4.6.0
- MySQL 8.0.21(pymysql 1.0.2)
- Pandas
- Numpy
- Scikit-learn 0.24.1
- Tensorflow 2.x
- PowerPoint
- IDE: PyCharm, Jupyter notebook

## ๐ [twiliow ์ฌ์ฉ๋ฒ](https://pypi.org/project/twilio/)
- ๋ค์ ๋ช๋ น์ด๋ฅผ ํฐ๋ฏธ๋์์ ์๋ ฅ ํ ๋ค์ด๋ก๋
<br>```pip install twilio```<br>
- twilio ๊ฐ์ ํ twilio ์น ๋ธ๋ผ์ฐ์  console๋ก ์ด๋ํด ``account_sid``์ ``auth_token`` ํ์ธ ํ ``main.py`` ํ์ผ๊ณผ ๋์ผํ ์ฝ๋๋ก ๋ฉ์ธ์ง ์ ์ก
