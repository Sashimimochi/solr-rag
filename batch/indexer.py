import time

import pysolr
from tqdm.auto import tqdm

from mylogging import logger
from solr import SolrClient


class Indexer(SolrClient):
    def __init__(self):
        super().__init__()

    def add(
        self,
        collection: str,
        docs: list,
        commit: bool = True,
        max_post: int = 100,
    ):
        solr = pysolr.SolrCloud(
            self.zookeeper,
            collection=collection,
            timeout=120,
            retry_count=5,
            retry_timeout=1,
            always_commit=False,
        )
        solr.ping()

        for i in tqdm(range(0, len(docs), max_post)):
            solr.add(
                docs[i : i + max_post],
                handler="update/vector",
                commit=False,
            )
            time.sleep(2)

        if commit:
            solr.commit()

        logger.info(f"{len(docs)} documents are indexed.")
