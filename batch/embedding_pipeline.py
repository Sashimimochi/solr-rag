from mylogging import logger
from db import MySQLClient, MongoClient
from embedder import Embedder


model_name = "pkshatech/GLuCoSE-base-ja"
embedder = Embedder(model_name=model_name)

mysql_client = MySQLClient()
rows = mysql_client.select()
docs = [row.get('body') or '' for row in rows]
logger.info("embedding documents...")
embeds = embedder.embedding_docs(docs)
for row, embed in zip(rows, embeds):
    row['vector'] = embed

mongo_client = MongoClient()
mongo_client.insert(rows)
