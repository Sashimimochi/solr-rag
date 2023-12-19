from indexer import Indexer, LangChainIndexer, ImageIndexer
from db import MySQLClient, MongoClient
from langchain.docstore.document import Document
from mylogging import logger

def index_from_mongo():
    client = MongoClient()
    docs = client.select()
    if len(docs) == 0:
        logger.warning("Index Data is Empty.")
    indexer = Indexer()
    indexer.add(collection="langchain", docs=docs)

def index_from_mysql():
    client = MySQLClient()
    indexer = LangChainIndexer()

    rows = client.select()
    if len(rows) == 0:
        logger.warning("Index Data is Empty.")
    # 使用可能な型が限定されているので加工する
    docs = []
    for row in rows:
        metadata = {}
        content = row.get(indexer.page_content_field)
        for k, v in row.items():
            if v is not None:
                metadata[k] = v
            if k in ["created_at"]:
                metadata[k] = indexer.convert_datetime(v)
        docs.append(Document(page_content=content, metadata=metadata))
    indexer.add(docs=docs)

def index_from_file():
    indexer = ImageIndexer()
    import pandas as pd
    rows = pd.read_csv("./data/log.csv").to_dict(orient="records")
    docs = []
    for row in rows:
        content = row.pop("prompt")
        metadata = row
        docs.append(Document(page_content=content, metadata=metadata))
    indexer.add(docs)

def main():
    index_from_mysql()
    index_from_file()

if __name__ == '__main__':
    main()
