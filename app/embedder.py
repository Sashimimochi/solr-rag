from langchain.embeddings import HuggingFaceEmbeddings

class Embedder:
    def __init__(self, model_name) -> None:
        self.embeddings = HuggingFaceEmbeddings(model_name=model_name)  # you are free to use any embeddings method allowed by langchain

    def embedding_docs(self, docs):
        embeds = self.embeddings.embed_documents(docs)
        return embeds
