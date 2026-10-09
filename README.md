# Solr RAG Sample

## System Architecture

![system-architecture](images/rag.png)

## Environment

The application runs Solr 10.0.0 and uses Solr's Language Models module for text embedding.

### Tools

|                | Version  |
| :------------- | :------- |
| Docker         | 20.10.21 |
| docker-compose | 1.29.2   |
| wget           | 1.20.3   |

## Embedding

Embedding is handled by Solr through Cohere's embedding API rather than by the Python application.

- Model: `embed-multilingual-v3.0`
- Provider: Cohere
- Supported languages: 100+ languages including Japanese
- Dimension: 1024
- Similarity: cosine

Solr uses the Language Models module for both sides of the RAG flow:

1. The `textToVector` Update Request Processor converts `body` into the `vector` field using the `embedding-document` model.
2. The `knn_text_to_vector` query parser converts the user's query and runs KNN search against `vector` using the `embedding-query` model.

The two model registrations use the same Cohere model but different `inputType` values (`search_document` and `search_query`), as recommended for retrieval. The model outputs 1024-dimensional vectors, matching the Solr schema.

Text is sent to Cohere's hosted API for embedding. Review Cohere's service terms, privacy requirements, rate limits, and pricing before indexing sensitive or large datasets.

## Prepare

If you would like to use your original data, please put `mydata.tsv` in `mysql/data/mydata` directory.

```text
mysql/
└── data/
    └── mydata/
        └── mydata.tsv
```

Set a Cohere API key before starting the initial setup:

```bash
export COHERE_API_KEY=your-cohere-api-key
```

## Usage

```bash
# initial setup
$ make all

# start an existing setup
$ make launch

# re-index
$ make add-index
```

Access http://localhost:8501 in a browser.

## Related Documents

- [Solr でも RAG できるもん！](https://zenn.dev/sashimimochi/articles/be1122c813d989)
- [Solr でも RAG できるもん！の裏話](https://zenn.dev/sashimimochi/articles/29d78fadaf8b17)

## References

- [Apache Solr Text to Vector](https://solr.apache.org/guide/solr/10_0/query-guide/text-to-vector.html)
- [Apache Solr Solr Modules](https://solr.apache.org/guide/solr/10_0/configuration-guide/solr-modules.html)
- [Apache Solr 10.0 Upgrade Notes](https://solr.apache.org/guide/solr/10_0/upgrade-notes/major-changes-in-solr-10.html)
- [Cohere Embed models and supported languages](https://docs.cohere.com/docs/cohere-embed)
