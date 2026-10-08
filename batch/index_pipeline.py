from db import MySQLClient
from indexer import Indexer
from mylogging import logger


def index_from_mysql():
    client = MySQLClient()
    rows = client.select()
    if len(rows) == 0:
        logger.warning("Index Data is Empty.")
        return

    docs = []
    for row in rows:
        doc = dict(row)
        created_at = doc.get("created_at")
        if created_at is not None:
            doc["created_at"] = created_at.strftime("%Y-%m-%dT%H:%M:%SZ")
        if doc.get("id") is not None:
            doc["id"] = str(doc["id"])
        docs.append(doc)

    indexer = Indexer()
    indexer.add(collection="langchain", docs=docs)


def main():
    index_from_mysql()


if __name__ == "__main__":
    main()
