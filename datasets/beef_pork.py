import requests
from bs4 import BeautifulSoup
import pandas as pd
import pymysql



class CrawlPrices:
    '''
    for 20일 매출을 예측, 19일->20일 넘어가는 밤 12시 땡할 때는 19일에 대한 소, 돼지가격 데이터 API에 올라와 있음!
    '''

    # 소고기 가격 데이터 크롤링 후 DB저장
    def crawl_beef(self):
        # API URI - 2023년까지
        beef_url = 'http://data.ekape.or.kr/openapi-data/service/user/grade/auct/cattleApperence?baseYmd=2017-09-10&ServiceKey=0OhBU7ZCGIobDVKDeBJDpmDRqK3IRNF6jlf%2FJB2diFAf%2FfR2czYO9A4UTGcsOwppV6W2HVUeho%2FFPwXoL6DwqA%3D%3D'
        # 크롤링 데이터 담을 dict
        beef_dict = {}

        dates = []
        beefs = []
        beef_ks = []
        regions = []
        prices = []

        present_time = pd.Timestamp.now() - pd.Timedelta(days=1)
        present_time = present_time.strftime("%Y-%m-%d")
        datetimes = pd.date_range(start=present_time, end=present_time, freq='D').strftime('%Y-%m-%d').tolist()

        for datetime in datetimes:
            beef_url = f'http://data.ekape.or.kr/openapi-data/service/user/grade/auct/cattleApperence?baseYmd={datetime}&ServiceKey=0OhBU7ZCGIobDVKDeBJDpmDRqK3IRNF6jlf%2FJB2diFAf%2FfR2czYO9A4UTGcsOwppV6W2HVUeho%2FFPwXoL6DwqA%3D%3D'
            res = requests.get(beef_url)
            soup = BeautifulSoup(res.content, 'html.parser')
            contents = soup.select('item')
            print(datetime)  # 크롤링 날짜 확인
            for content in contents:
                date = content.select_one('baseymd').get_text()
                beef = content.select_one('judgekindnm').get_text()
                beef_k = content.select_one('judgebreednm').get_text()
                region = content.select_one('localnm').get_text()
                price = content.select_one('auctamt').get_text()

                dates.append(date)
                beefs.append(beef)
                beef_ks.append(beef_k)
                regions.append(region)
                prices.append(price)

        beef_dict['날짜'] = dates
        beef_dict['동물'] = beefs
        beef_dict['종류'] = beef_ks
        beef_dict['지역'] = regions
        beef_dict['가격'] = prices

        # 로컬 MySQL DB에 저장
        db = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             password='watson1259@',
                             db='beef_pork_db',
                             charset='utf8')
        cursor = db.cursor()

        rows = map(list, zip(*beef_dict.values()))

        # 한 row씩 DB에 insert하기
        for row in rows:
            sql = """INSERT INTO beef_prices VALUES('""" + row[0] + """','""" + row[1] + """','""" + row[2] + """',
            '""" + str(row[3]) + """','""" + str(row[4]) + """')"""
            cursor.execute(sql)
            db.commit()

        db.close()

    # 돼지고기 가격 데이터 크롤링 후 DB 저장
    def crawl_pork(self):
        pork_url = 'http://data.ekape.or.kr/openapi-data/service/user/grade/auct/pigApperence?baseYmd=20170908&ServiceKey=0OhBU7ZCGIobDVKDeBJDpmDRqK3IRNF6jlf%2FJB2diFAf%2FfR2czYO9A4UTGcsOwppV6W2HVUeho%2FFPwXoL6DwqA%3D%3D'
        pork_dict = {}

        dates = []
        porks = []
        pork_ks = []
        regions = []
        prices = []

        present_time = (pd.Timestamp.now() - pd.Timedelta(days=1)).strftime("%Y-%m-%d")
        datetimes = pd.date_range(start=present_time, end=present_time, freq='D').strftime('%Y%m%d').tolist()
        for datetime in datetimes:
            pork_url = f'http://data.ekape.or.kr/openapi-data/service/user/grade/auct/pigApperence?baseYmd={datetime}&ServiceKey=0OhBU7ZCGIobDVKDeBJDpmDRqK3IRNF6jlf%2FJB2diFAf%2FfR2czYO9A4UTGcsOwppV6W2HVUeho%2FFPwXoL6DwqA%3D%3D'
            res = requests.get(pork_url)
            soup = BeautifulSoup(res.content, 'html.parser')
            contents = soup.select('item')
            print(datetime)  # 크롤링 날짜 확인
            for content in contents:
                date = content.select_one('baseymd').get_text()
                pork = content.select_one('judgekindnm').get_text()
                pork_k = content.select_one('skinnm').get_text()
                region = content.select_one('localnm').get_text()
                price = content.select_one('auctamt').get_text()

                dates.append(date)
                porks.append(pork)
                pork_ks.append(pork_k)
                regions.append(region)
                prices.append(price)

        pork_dict['날짜'] = dates
        pork_dict['동물'] = porks
        pork_dict['종류'] = pork_ks
        pork_dict['지역'] = regions
        pork_dict['가격'] = prices

        # 로컬 MySQL DB에 저장
        db = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             password='watson1259@',
                             db='beef_pork_db',
                             charset='utf8')
        cursor = db.cursor()

        rows = map(list, zip(*pork_dict.values()))

        # 한 row씩 DB에 insert하기
        for row in rows:
            sql = """INSERT INTO pork_prices VALUES('""" + row[0] + """','""" + row[1] + """','""" + row[2] + """',
            '""" + str(row[3]) + """','""" + str(row[4]) + """')"""
            cursor.execute(sql)
            db.commit()

        db.close()

