import time
import pysolr
from tqdm.auto import tqdm
from eurelis_langchain_solr_vectorstore import Solr
from embedder import Embedder
from mylogging import logger

class ImageIndexer:
    def __init__(self) -> None:
        self.indexer = LangChainIndexer(lang="multilingual")

    def add(self, docs):
        self.indexer.add(docs, core_name="image")

class LangChainIndexer():
    def __init__(self, lang="ja") -> None:
        self.page_content_field = 'body'
        self.embedder = self.load_embedder(lang)

    def load_embedder(self, lang):
        if lang == "ja":
            model_name = "pkshatech/GLuCoSE-base-ja"
        else:
            model_name = "intfloat/multilingual-e5-large"
        embedder = Embedder(model_name=model_name).embeddings
        return embedder

    def convert_datetime(self, data):
        return data.strftime('%Y-%m-%d %H:%M:%S')

    def add(self, docs:list, core_name="langchain"):
        vector_store = Solr(self.embedder, core_kwargs={
            'page_content_field': self.page_content_field,  # field containing the text content
            'vector_field': 'vector',        # field containing the embeddings of the text content
            'core_name': core_name,        # core name
            'url_base': 'http://solr_node1:8983/solr' # base url to access solr
        })  # with custom default core configuration
        docs = vector_store.add_documents(docs)
        logger.info(f"{len(docs)} documents are indexed.")

from solr import SolrClient

class Indexer(SolrClient):
    def __init__(self):
        super().__init__()

    def add(self, collection: str, docs: list, commit: bool = True, max_post=1000):
        solr = pysolr.SolrCloud(
            self.zookeeper,
            collection=collection,
            timeout=30,
            retry_count=5,
            retry_timeout=0.2,
            always_commit=commit,
        )
        solr.ping()

        # 大きすぎるとタイムアウトするので max_post 件ずつ送る
        for i in tqdm(range(0, len(docs), max_post)):
            solr.add(docs[i : i + max_post])
            time.sleep(2)
