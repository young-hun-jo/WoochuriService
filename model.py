from datasets.weather import CrawlWeather
from datasets.beef_pork import CrawlPrices
from datasets.Woochuri_sales import InsertSale
import pymysql
import numpy as np
import pandas as pd
import holidays
from itertools import chain
from sklearn.impute import KNNImputer
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
import warnings
warnings.filterwarnings(action='ignore')


class WoochuriPredModel:
    '''
    Class including that crawl, preprocess data, modeling and finally prediction
    '''

    def __init__(self, user, password, end_time, today_sale, remark):
        """
        Args:
            - _user : local DB 'user_id'
            - _password : local DB 'password'
            - _end_time : today's datetime
            - _remark : whether holiday or not
        """
        self._user = user
        self._password = password
        self._end_time = end_time  # time that will be predicted
        self._today_sale = today_sale
        self._remark = remark

    def _crawl_datasets(self):
        """
        Function: Crawling public datasets and insert today's sale into local DB
        """
        CrawlWeather().crawl_weather()
        CrawlPrices().crawl_beef()
        CrawlPrices().crawl_pork()
        InsertSale().insert_sale(today_sale=self._today_sale, remark_str=self._remark)

    def _load_beef_pork(self):
        """
        Function: crawl and load beef and pork dataset. And preprocess it.
        """
        # Crawling all datasets
        self._crawl_datasets()

        # connect local MySQL
        db = pymysql.connect(host='localhost', user=self._user,
                             password=self._password, db='beef_pork_db',
                             charset='utf8')
        cursor = db.cursor()
        # Select datasets using SQL
        beef_sql = "SELECT DISTINCT * FROM beef_prices WHERE 날짜 < '2011-03-03' AND 지역 = '전국'\
                            UNION\
                            SELECT DISTINCT * FROM beef_prices WHERE 날짜 >= '2011-03-03' AND 지역 = '중부권'\
                            ORDER BY 날짜"
        pork_sql = "SELECT DISTINCT * FROM pork_prices ORDER BY 날짜"

        beef_df = pd.read_sql(beef_sql, db)
        pork_df = pd.read_sql(pork_sql, db)

        # Preprocess beef dataset
        hanwoo_df = beef_df[beef_df['종류'] == '한우']
        yukwoo_df = beef_df[beef_df['종류'] == '육우']
        hanwoo_df = hanwoo_df.rename(columns={'종류': '한우', '가격': '한우가격'})
        yukwoo_df = yukwoo_df.rename(columns={'종류': '육우', '가격': '육우가격'})

        raw_date_df = pd.DataFrame(pd.date_range(start='2009-01-01', end=self._end_time, freq='D'))
        raw_date_df = raw_date_df.rename(columns={0: '날짜'})
        hanwoo_df = raw_date_df.merge(hanwoo_df, how='left')
        hanwoo_df = hanwoo_df[['날짜', '한우가격']]
        yukwoo_df = raw_date_df.merge(yukwoo_df, how='left')
        yukwoo_df = yukwoo_df[['날짜', '육우가격']]
        hanwoo_df = hanwoo_df.fillna(method='ffill')
        yukwoo_df = yukwoo_df.fillna(method='ffill')
        merge_beef_df = hanwoo_df.merge(yukwoo_df, how='inner', on='날짜')

        # Preprocess pork dataset
        cond_tang = pork_df['종류'] == '탕박'
        cond_n = pork_df['지역'] == '전국'
        pork_df = pork_df[(cond_tang) & (cond_n)]

        raw_date_df = pd.DataFrame(pd.date_range(start='2009-01-01', end=self._end_time, freq='D'))
        raw_date_df = raw_date_df.rename(columns={0: '날짜'})
        merge_pork_df = raw_date_df.merge(pork_df, how='left')
        merge_pork_df = merge_pork_df.fillna(method='ffill')
        merge_pork_df = merge_pork_df.rename(columns={'가격': '돼지탕박가격'})
        merge_cols = ['날짜', '돼지탕박가격']
        merge_pork_df = merge_pork_df[merge_cols]

        # Merge beef and pork dataset
        beef_pork_df = merge_beef_df.merge(merge_pork_df, how='inner', on='날짜')

        # Remove outlier (한우가격 < 육우가격)
        cond0 = beef_pork_df['한우가격'] < beef_pork_df['육우가격']
        cond1 = beef_pork_df['육우가격'] > 18000
        beef_pork_df.loc[(cond0 | cond1), '육우가격'] = beef_pork_df.loc[(cond0 | cond1)]['한우가격'] * (10 / 18)

        cond2 = beef_pork_df['한우가격'] < 1e4
        beef_pork_df.loc[cond2, '한우가격'] = beef_pork_df.loc[cond2]['육우가격'] * (18 / 10)

        return beef_pork_df

    def _load_weather(self):
        """
        Function: load weather dataset and preprocess it
        """
        # load weather dataset
        db = pymysql.connect(host='localhost', user=self._user,
                             password=self._password, db='weather_db',
                             charset='utf8')
        cursor = db.cursor()
        # Select datasets using SQL
        weather_sql = "SELECT DISTINCT 지역, 시간,\
                                      NULLIF(평균기온, '') AS 평균기온,\
                                      NULLIF(최저기온, '') AS 최저기온,\
                                      NULLIF(최고기온, '') AS 최고기온,\
                                      NULLIF(1시간최다강수량, '') AS 1시간최다강수량,\
                                      NULLIF(일강수량, '') AS 일강수량,\
                                      NULLIF(평균풍속, '') AS 평균풍속,\
                                      NULLIF(최대풍속, '') AS 최대풍속,\
                                      NULLIF(평균상대습도, '') AS 평균상대습도,\
                                      NULLIF(최소상대습도, '') AS 최소상대습도,\
                                      NULLIF(1시간최다일사량, '') AS 1시간최다일사량,\
                                      NULLIF(일사량, '') AS 일사량\
                                      FROM weather\
                                      ORDER BY 시간"
        weather = pd.read_sql(weather_sql, db)
        weather = weather.rename(columns={'시간': '날짜'})

        # Replace missing values in weather dataset
        dataset = weather.copy()
        dataset = dataset.drop(['1시간최다강수량'], axis=1)
        dataset['일강수량'] = dataset['일강수량'].fillna(0.0)

        avg_wind = dataset[['평균풍속', '최대풍속']]  # 결측치:평균풍속
        avg_humid = dataset[['평균상대습도', '최소상대습도', '최저기온', '일강수량', '평균기온', '최고기온']]  # 결측치:평균상대습도
        max_sun_h = dataset[['1시간최다일사량', '최고기온', '평균기온', '최저기온', '최소상대습도']]  # 결측치:1시간최다일사량
        max_sun = dataset[['일사량', '최고기온', '평균기온', '최저기온', '최소상대습도']]  # 결측치:일사량

        knn_datasets = [avg_wind, avg_humid, max_sun_h, max_sun]
        after_datasets = []
        for data in knn_datasets:
            imputer = KNNImputer(n_neighbors=5, weights='uniform', metric='nan_euclidean')
            imputer.fit(data.values)
            after_values = imputer.transform(data.values)  # array
            after_dataset = pd.DataFrame(after_values, columns=data.columns)
            after_datasets.append(after_dataset)
        concat_df = pd.concat([after_datasets[0], after_datasets[1], after_datasets[2], after_datasets[3]], axis=1)
        concat_cols = concat_df.columns.tolist()
        transform_dict = {}

        for i, v in enumerate(concat_df.values.T):
            transform_dict[concat_cols[i]] = v
        transform_df = pd.DataFrame(transform_dict)

        standard_cols = set(dataset.columns) - set(transform_df.columns)
        dataset = pd.concat([dataset[standard_cols], transform_df], axis=1)

        weather = dataset.copy()
        weather = weather.drop('지역', axis=1)

        return weather

    def _load_woochuri(self):
        """
        Function: load Woochuri daily sales and preprocess it
        """
        db = pymysql.connect(host='localhost', user=self._user,
                             password=self._password, db='sales_db',
                             charset='utf8')
        cursor = db.cursor()

        sales_sql = "SELECT DISTINCT * FROM sales ORDER BY 날짜"
        sales = pd.read_sql(sales_sql, db)

        present_time = int(pd.Timestamp.now().strftime("%Y"))
        kor_holidays = holidays.Korea(years=[d for d in range(2008, present_time + 1)])

        holidays_dates = []
        holidays_names = []
        for date, name in kor_holidays.items():
            holidays_dates.append(date)
            holidays_names.append(name)

        holidays_df = pd.DataFrame({'공휴일날짜': holidays_dates,
                                    '공휴일명': holidays_names}).sort_values(by='공휴일날짜')
        holidays_df['공휴일날짜'] = pd.to_datetime(holidays_df['공휴일날짜'])

        next_five_time = pd.date_range(start=self._end_time, freq='D', periods=6)[-1].strftime('%Y-%m-%d')
        extra_datetime = pd.DataFrame(pd.date_range(start='2009-01-01', end=next_five_time, freq='D'),
                                      columns=['가중치위한날짜'])
        sales = extra_datetime.merge(sales, how='left', left_on='가중치위한날짜', right_on='날짜')
        sales = sales.drop('날짜', axis=1)
        sales = sales.rename(columns={'가중치위한날짜': '날짜'})
        sales_holiday_df = sales.merge(holidays_df, how='left', left_on='날짜', right_on='공휴일날짜')

        hol_cols = ['날짜', '일매출', 'remark', '공휴일날짜', '공휴일명']
        holidays_data = sales_holiday_df[hol_cols]
        holidays_data['요일'] = holidays_data['날짜'].dt.day_name()
        hol_cols = ['날짜', '요일', '일매출', 'remark', '공휴일날짜', '공휴일명']
        holidays_data = holidays_data[hol_cols]

        lunar_chuseok = ["The day preceding of Lunar New Year's Day", "The day preceding of Chuseok"]
        lunar_chuseok_dates = holidays_data[holidays_data['공휴일명'].isin(lunar_chuseok)]['날짜'].dt.strftime(
            '%Y-%m-%d').values
        lunar_chuseok_around_dates = []
        for date in lunar_chuseok_dates:
            around = pd.date_range(end=date, freq='D', periods=6)
            lunar_chuseok_around_dates.append(around)
        lunar_chuseok_arounds = list(chain.from_iterable(lunar_chuseok_around_dates))

        lunar_chuseok_dict = {}
        weight = 0
        for around_date in lunar_chuseok_arounds:
            weight += 1
            if weight > 6:
                weight = 1
            lunar_chuseok_dict[around_date] = weight

        def holidays_weights(df):
            df['설_추석_가중치'] = 0
            df['일반공휴일가중치'] = 0
            if df['날짜'] in list(lunar_chuseok_dict.keys()):
                df['설_추석_가중치'] = lunar_chuseok_dict[df['날짜']]
            return df

        holidays_data = holidays_data.apply(holidays_weights, axis=1)
        holidays_data.loc[(~holidays_data['공휴일명'].str.contains('Lunar|Chuseok', na=False)) & (
            holidays_data['공휴일명'].notnull()), '일반공휴일가중치'] = 1

        need_cols = ['날짜', '요일', '일매출', '설_추석_가중치', '일반공휴일가중치']
        holidays_data = holidays_data[need_cols]

        return holidays_data

    def _merge_datasets(self, beef_pork, weather, sales):
        """
        Function: Merge all datasets
        Args:
            - beef_pork: 예측하려는 날 이전 데이터까지 존재
            - weather: 예측하려는 날 이전 데이터까지 존재
            - sales: 예측하려는 날로부터 미래 5일까지의 데이터가 존재
        """
        # Check each shape of dataframes
        print('Beef & Pork:', beef_pork.shape)
        print(beef_pork.tail())
        print('-'*50)
        print('Weather:', weather.shape)
        print(weather.tail())
        print('-' * 50)
        print('Woochuri Sales:', sales.shape)
        print(sales.tail())
        print('-' * 50)

        # Merge all datasets
        beef_pork_weather = beef_pork.merge(weather, how='inner', on='날짜')
        dataset = sales.merge(beef_pork_weather, how='left', on='날짜')
        dataset = dataset.iloc[:-5]  # remove more five rows
        print("Final dataset:", dataset.shape)

        # Preprocess zero-sales
        days = dataset.groupby('요일')['일매출'].mean().index
        means = dataset.groupby('요일')['일매출'].mean().values
        weekdays_means = dict(zip(days, means))

        def replace_zero_sales(df):
            if df['일매출'] == 0:
                df['일매출'] = weekdays_means[df['요일']]
            return df

        dataset = dataset.apply(replace_zero_sales, axis=1)

        # Give weights to weekday
        weekdays = dataset.groupby('요일')['일매출'].mean().index
        values = dataset.groupby('요일')['일매출'].mean().values
        weekdays_dict = dict(zip(weekdays, values))
        dataset['요일'] = dataset['요일'].map(weekdays_dict)

        # Give weights to day(1day~31day)
        dataset['일'] = dataset['날짜'].dt.day
        daily = dataset.groupby('일')['일매출'].mean().index
        values = dataset.groupby('일')['일매출'].mean().values
        daily_dict = dict(zip(daily, values))
        dataset['일'] = dataset['일'].map(daily_dict)

        # remove multi-Colinearity
        multi_cols = ['최소상대습도', '최저기온', '평균기온', '1시간최다일사량']
        final_dataset = dataset.drop(multi_cols, axis=1)
        final_dataset = final_dataset.set_index('날짜')

        return final_dataset

    def execute(self):
        """
        Function: After loading, preprocessing each dataset, merge all datasets into final dataset
        """
        BeefPork = self._load_beef_pork()
        Weather = self._load_weather()
        Sales = self._load_woochuri()
        FinalDataset = self._merge_datasets(BeefPork, Weather, Sales)

        return FinalDataset

    def run(self, final_dataset):
        """
        Function: modeling and predict tomorrow sales of 'Woochuri Store'
        """
        # Make target variable
        final_dataset['target'] = np.append(np.array(final_dataset['일매출'][1:]), 0)

        # Split train and test data
        X_train, y_train = final_dataset.iloc[:-1, :-1], final_dataset.iloc[:-1, -1]
        X_test = final_dataset.iloc[-1, :-1]
        X_test = pd.DataFrame(X_test.values.reshape(1, -1),
                              columns=X_test.index)  # Create one-row dataframe

        # Apply MinMaxScaler partly
        scaler = MinMaxScaler()
        no_scale_cols = ['설_추석_가중치', '일반공휴일가중치']
        scale_cols = ['일매출', '요일', '일', '한우가격', '육우가격', '돼지탕박가격', '평균상대습도', '최고기온', '평균풍속', '최대풍속',
                      '일사량', '일강수량']

        X_train_scale = X_train[scale_cols]
        X_train_no_scale = X_train[no_scale_cols]
        X_test_scale = X_test[scale_cols]
        X_test_no_scale = X_test[no_scale_cols]

        X_train_scale = pd.DataFrame(scaler.fit_transform(X_train_scale),
                                     columns=X_train_scale.columns,
                                     index=X_train_scale.index)
        X_test_scale = pd.DataFrame(scaler.transform(X_test_scale),
                                    columns=X_test_scale.columns,
                                    index=X_test_scale.index)

        X_train = pd.concat([X_train_scale, X_train_no_scale], axis=1)
        X_test = pd.concat([X_test_scale, X_test_no_scale], axis=1)

        # fit model
        model = RandomForestRegressor(n_estimators=100,
                                      min_samples_split=2,
                                      random_state=42)
        model.fit(X_train, y_train)

        # Predict sale of next day
        y_pred = model.predict(X_test)
        res = int(y_pred[0]) / 1e4
        # print result
        weekday_map = {'Sunday': '일요일', 'Monday': '월요일',
                       'Tuesday': '화요일', 'Wednesday': '수요일',
                       'Thursday': '목요일', 'Friday': '금요일',
                       'Saturday': '토요일'}

        pred_time = pd.Timestamp.now()
        day_name = pred_time.day_name()
        str_pred_time = pred_time.strftime("%Y-%m-%d")
        result = f"[우추리 축산 AI] - {str_pred_time}일 {weekday_map[day_name]} 우추리축산 매출은{res: .0f}만원 입니다."
        print(result)

        return result





