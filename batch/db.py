import mysql.connector
from tqdm import tqdm

class MySQLClient:
    def __init__(self) -> None:
        self.config = {
            'user': 'solrtutorial',
            'password': 'solrtutorial',
            'host': 'mysql',
            'database': 'lcc',
            'use_pure': True
        }

    def select_news(self):
        query = f'''
            SELECT id, media, url, created_at, title, body
            FROM news
        '''
        return self._select(query)

    def select_lcc(self):
        query = f'''
            SELECT id, media, url, created_at, title, body
            FROM lcc
        '''
        return self._select(query)

    def select_knbc(self):
        query = f'''
            SELECT id, doc, emotion
            FROM knbc
        '''
        return [
            {
                'id': row.get('id'),
                'media': None,
                'url': None,
                'created_at': None,
                'title': row.get('emotion'),
                'body': row.get('doc')
            } for row in self._select(query)
        ]

    def select_kwdlc(self):
        query = f'''
            SELECT id, body
            FROM kwdlc
        '''
        return [
            {
                'id': row.get('id'),
                'media': None,
                'url': None,
                'created_at': None,
                'title': None,
                'body': row.get('body')
            } for row in self._select(query)
        ]
    
    def select_with_query(self, query):
        return self._select(query)

    def select(self, topK:int=None):
        data = []
        #data += self.select_lcc()
        #data += self.select_knbc()
        #data += self.select_kwdlc()
        data += self.select_news()
        return data[:topK] if topK else data

    def _select(self, query):
        cnx = None
        res = None

        try:
            cnx = mysql.connector.connect(**self.config)

            cursor = cnx.cursor()
            cursor.execute(query)
            columns = cursor.column_names

            results = []
            for row in cursor.fetchall():
                result = {}
                for i, value in enumerate(row):
                    result[columns[i]] = value
                results.append(result)

            cursor.close()
        except Exception as e:
            results = e
            raise Exception(e)
        finally:
            if cnx:
                cnx.close()
            return results

    def insert_vector(self, vectors:list):
        try:
            cnx = mysql.connector.connect(**self.config)

            # 各レコードにベクトルデータを挿入
            cursor = cnx.cursor()
            update_query = "UPDATE news SET vector = %s WHERE id = %s"

            # 各レコードごとにデータを挿入
            for id, vector in enumerate(tqdm(vectors), start=1):
                cursor.execute(update_query, (vector, id))
                cnx.commit()

            cursor.close()
        except Exception as e:
            raise Exception(e)
        finally:
            if cnx:
                cnx.close()

import pymongo

class MongoClient:
    def __init__(self) -> None:
        self.client = pymongo.MongoClient("mongodb://solr:solr@mongodb:27017/")

    def insert(self, data:list, db_name="solr", collection_name="news"):
        mydb = self.client[db_name]
        mycollection = mydb[collection_name]
        insert_result = mycollection.insert_many(data)
        print(f'{len(insert_result.inserted_ids)}件のデータが挿入されました。')

    def select(self, db_name="solr", collection_name="news"):
        mydb = self.client[db_name]
        mycollection = mydb[collection_name]
        result = list(mycollection.find())
        for row in result:
            del row['_id']
            row['created_at'] = json_serial(row['created_at'])
        return result


from datetime import date, datetime

# date, datetimeの変換関数
def json_serial(obj):
    # 日付型の場合には、文字列に変換します
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()+"Z"
    # 上記以外はサポート対象外.
    raise TypeError ("Type %s not serializable" % type(obj))
