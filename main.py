'''
 무조건 예측날 아침에 돌려야 함!!
'''
import pandas as pd
from weather import CrawlWeather
from beef_pork import CrawlPrices
from Woochuri_sales import InsertSale
from model import WoochuriPredModel
from twilio.rest import Client

print(pd.Timestamp.now())
# Crawling today's weather dataset in Public data API and store it in local DB
crawling_weather = CrawlWeather()
crawling_weather.crawl_weather()

# Crawling today's beef, pork price dataset in Public data API and store it in local DB
crawling_prices = CrawlPrices()
crawling_prices.crawl_beef()  # Beef price
crawling_prices.crawl_pork()  # Pork price

# Insert today's sales of Woochuri store and store it in local DB
today_sale = 435700  # 금일 매출 입력하기
remark_str = '평일'  # 금일 휴무 여부 입력하기!
insert_sale = InsertSale()
insert_sale.insert_sale(today_sale=today_sale, remark_str=remark_str)

# Load updated crawling dataset and modeling to predict tomorrow's sale
# Setting parameters using local MySQL id, password
user, password = 'root', 'watson1259@'
end_time = (pd.Timestamp.now() - pd.Timedelta(days=1)).strftime("%Y-%m-%d")

PredModel = WoochuriPredModel(user=user, password=password, end_time=end_time)
woochuri_df = PredModel.load_datasets()
result = PredModel.fit_predict(woochuri_df)

# Sending Meassage
account_sid = 'AC8f9d9f4c8983ee648153f5347ee027a9'
auth_token = 'your_auth_token' # your_auth_token 따로 적어놓기
client = Client(account_sid, auth_token)

woochuri_master = '+821094125854'
message = client.messages.create(from_='+13132543287', body=result, to=woochuri_master)
print(message.sid)
