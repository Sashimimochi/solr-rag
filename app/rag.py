import MeCab
import requests
import streamlit as st

from llm import Calm2, Rinna
from mylogging import logger


class RAG:
    def __init__(
        self,
        core_name="langchain",
        lang="ja",
        solr_url="http://solr_node1:8983/solr",
    ) -> None:
        self.core_name = core_name
        self.lang = lang
        self.solr_url = f"{solr_url.rstrip('/')}/{core_name}"

    def make_filter(self, query):
        logger.info(f"query:{query}")
        dict_path = "/usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd"
        mt = MeCab.Tagger(dict_path)
        node = mt.parseToNode(query)
        words = []
        while node:
            features = node.feature.split(",")
            word = node.surface
            logger.info(f"word:{word}, features:{features}")
            if len(features) > 1 and features[1] in ["固有名詞"]:
                words.append(word)
            node = node.next
        return f"body:({' AND '.join(words)})" if words else None

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

    def retrieval(self, query, k=2):
        fq = self.make_filter(query)
        logger.info(f"fq={fq}")

        params = {
            "q": f"{{!knn_text_to_vector model=embedding f=vector topK={k}}}{query}",
            "rows": k,
            "fl": "body",
            "wt": "json",
        }
        if fq:
            params["fq"] = fq

        response = requests.get(
            f"{self.solr_url}/select",
            params=params,
            timeout=60,
        )
        response.raise_for_status()

        docs = response.json().get("response", {}).get("docs", [])
        result = "".join(doc.get("body", "") for doc in docs)
        logger.info(f"検索結果:{result}")
        return result
