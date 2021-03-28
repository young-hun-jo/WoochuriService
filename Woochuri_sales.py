import pandas as pd
import pymysql


class InsertSale:


    def insert_sale(self, today_sale, remark_str):
        today = (pd.Timestamp.now() - pd.Timedelta(days=1)).strftime("%Y-%m-%d")

        # Insert today's sale of Woochuri store
        sales_dict = {}
        flag = 1
        while flag:
            sale = today_sale
            if type(sale) == int:
                remark = remark_str
                sales_dict['날짜'] = [today]
                sales_dict['일매출'] = [sale]
                sales_dict['remark'] = [remark]
                flag = 0
            else:
                print('-' * 50)
                print("** 매출을 잘못 입력하였습니다! 다시 입력하십시오! **")

        # Store today's sale in local DB
        db = pymysql.connect(host='localhost',
                             user='root',
                             password='watson1259@',
                             db='sales_db',
                             charset='utf8')
        cursor = db.cursor()

        rows = map(list, zip(*sales_dict.values()))
        for row in rows:
            sql = """INSERT INTO sales VALUES('""" + row[0] + """',
            '""" + str(row[1]) + """',
            '""" + row[2] + """')"""
            cursor.execute(sql)
            db.commit()

        db.close()

