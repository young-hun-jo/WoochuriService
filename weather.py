import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import pandas as pd
import pymysql


class CrawlWeather:

    def crawl_weather(self):
        '''
        $$ 날씨 데이터 때문에 밤 12시 땡해야 크롤링 가능함..!
        for 20일 매출 예측, 19일 날씨 데이터를 얻기 위해서는 19일->20일 넘어가는 12시에 크롤링 가능(결국 모델예측도 12시 땡!하면 가능할듯..)
        '''
        # 날씨는 오늘날짜 기준으로 어제 날씨까지만 있으므로 어제 날짜로 지정
        present_time = pd.Timestamp.now() - pd.Timedelta(days=1)
        present_time = present_time.strftime("%Y%m%d")
        print(present_time)
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        res = session.get(f'http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList?serviceKey=j%2FJXmL%2BFxwnNYqN%2FyoLJSfJx3ioQV1HnmM9E7b%2FaGLjLv51g0vZSGQjk0UVyJmGZckzK7Cm8Jds6G42cqdkX0w%3D%3D&numOfRows=999&pageNo=1&dataCd=ASOS&dateCd=DAY&startDt={present_time}&endDt={present_time}&stnIds=133')
        soup = BeautifulSoup(res.content, 'html.parser')
        contents = soup.select('item')

        data_dict = {}
        # 각 변수 값들 담을 list
        region_lst, datetime_lst = [], []
        avg_temp_lst, min_temp_lst = [], []
        min_temp_lst, max_temp_lst = [], []
        max_1h_rain_lst, sum_rain_lst = [], []
        avg_wind_lst, max_wind_lst = [], []
        avg_humid_lst, min_humid_lst = [], []
        max_1h_sun_lst, sum_sun_lst = [], []

        # 각 페이지에서 변수 별 데이터 수집
        for content in contents:
            region = content.select_one('stnnm').get_text()
            datetime = content.select_one('tm').get_text()
            avg_temp = content.select_one('avgta').get_text()
            min_temp = content.select_one('minta').get_text()
            max_temp = content.select_one('maxta').get_text()
            max_1h_rain = content.select_one('hr1maxrn').get_text()
            sum_rain = content.select_one('sumrn').get_text()
            avg_wind = content.select_one('avgws').get_text()
            max_wind = content.select_one('maxws').get_text()
            avg_humid = content.select_one('avgrhm').get_text()
            min_humid = content.select_one('minrhm').get_text()
            max_1h_sun = content.select_one('hr1maxicsr').get_text()
            sum_sun = content.select_one('sumgsr').get_text()

            region_lst.append(region)
            datetime_lst.append(datetime)
            avg_temp_lst.append(avg_temp)
            min_temp_lst.append(min_temp)
            max_temp_lst.append(max_temp)
            max_1h_rain_lst.append(max_1h_rain)
            sum_rain_lst.append(sum_rain)
            avg_wind_lst.append(avg_wind)
            max_wind_lst.append(max_wind)
            avg_humid_lst.append(avg_humid)
            min_humid_lst.append(min_humid)
            max_1h_sun_lst.append(max_1h_sun)
            sum_sun_lst.append(sum_sun)

        data_dict['지역'] = region_lst
        data_dict['시간'] = datetime_lst
        data_dict['평균기온'] = avg_temp_lst
        data_dict['최저기온'] = min_temp_lst
        data_dict['최고기온'] = max_temp_lst
        data_dict['1시간최다강수량'] = max_1h_rain_lst
        data_dict['일강수량'] = sum_rain_lst
        data_dict['평균풍속'] = avg_wind_lst
        data_dict['최대풍속'] = max_wind_lst
        data_dict['평균상대습도'] = avg_humid_lst
        data_dict['최소상대습도'] = min_humid_lst
        data_dict['1시간최다일사량'] = max_1h_sun_lst
        data_dict['일사량'] = sum_sun_lst

        # 로컬 MySQL DB에 저장
        db = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             password='watson1259@',
                             db='weather_db',
                             charset='utf8')
        cursor = db.cursor()

        rows = map(list, zip(*data_dict.values()))
        for row in rows:
            sql = """INSERT INTO weather VALUES('""" + row[0] + """',
            '""" + row[1] + """','""" + row[2] + """','""" + row[3] + """',
            '""" + row[4] + """','""" + row[5] + """','""" + row[6] + """',
            '""" + row[7] + """','""" + row[8] + """','""" + row[9] + """',
            '""" + row[10] + """','""" + row[11] + """','""" + row[12] + """')"""
            cursor.execute(sql)
            db.commit()

        db.close()

