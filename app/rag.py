import MeCab
import streamlit as st
from eurelis_langchain_solr_vectorstore import Solr
from llm import Calm2, Rinna
from embedder import Embedder
from mylogging import logger

class RAG:
    def __init__(self, core_name="langchain", lang="ja") -> None:
        embedder = self.load_embedder(lang)
        self.vector_store = Solr(embedder, core_kwargs={
            'page_content_field': 'body',  # field containing the text content
            'vector_field': 'vector',        # field containing the embeddings of the text content
            'core_name': core_name,        # core name
            'url_base': 'http://solr_node1:8983/solr' # base url to access solr
        })  # with custom default core configuration

    @st.cache_resource
    def load_embedder(_self, lang):
        if lang == "ja":
            model_name = "pkshatech/GLuCoSE-base-ja"
        else:
            model_name = "intfloat/multilingual-e5-large"
        embedder = Embedder(model_name=model_name).embeddings
        return embedder

    def make_filter(self, query):
        logger.info(f"query:{query}")
        dict_path = "/usr/lib/x86_64-linuxgnu/mecab/dic/mecab-ipadic-neologd"
        mt = MeCab.Tagger(dict_path)
        node = mt.parseToNode(query)
        words = []
        while node:
            features = node.feature.split(",")
            word = node.surface
            logger.info(f"word:{word}, features:{features}")
            if features[1] in ['固有名詞']:
                words.append(word)
            node = node.next
        return {"body": f"({' AND '.join(words)})"} if len(words) > 0 else {}

    def load_model(self, model_name):
        if model_name == "Rinna":
            self.model = Rinna()
        else:
            self.model = Calm2()

    def generate(self, query, model_name):
        self.load_model(model_name)

        answer = self._generate(query)

        context = self.retrieval(query)
        answer_with_rag = self._generate_with_rag(query=query, context=context)

        return answer, answer_with_rag

    def _generate(self, query):
        return self.model.generate(query)

    def _generate_with_rag(self, query, context):
        return self.model.generate_with_rag(query, context)

    def _retrieval(self, query, k, fq):
        retriever = self.vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": k,
                "filter": fq,
                "score_threshold": 0.5
            }
        )
        docs = retriever.get_relevant_documents(query=query)
        return docs

    def retrieval(self, query, k=2):
        fq = self.make_filter(query)
        logger.info(f"fq={fq}")
        docs = self._retrieval(query, k, fq)
        res = "".join([doc.page_content for doc in docs])
        logger.info(f"検索結果:{res}")
        return res
