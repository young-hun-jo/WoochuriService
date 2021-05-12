import pandas as pd
from model import WoochuriPredModel
from twilio.rest import Client

print('예측하려는 날짜:', pd.Timestamp.now())

# Load updated crawling dataset and modeling to predict tomorrow's sale
# Setting parameters using local MySQL id, password
user, password = 'root', 'your_pw@'
end_time = (pd.Timestamp.now() - pd.Timedelta(days=1)).strftime("%Y-%m-%d")

# run crawling, preprocess datasets, and finally prediction at one time
PredModel = WoochuriPredModel(user=user, password=password, end_time=end_time,
                                  today_sale=0, remark='특이휴무')
FinalDataset = PredModel.execute()
result = PredModel.run(FinalDataset)

# Sending message
account_sid = 'AC8f9d9f4c8983ee648153f5347ee027a9'
auth_token = 'your_auth_token'  # customize your_auth_token
client = Client(account_sid, auth_token)

woochuri_master = '+821094125854'
message = client.messages.create(from_='+13132543287', body=result, to=woochuri_master)
print(message.sid)


