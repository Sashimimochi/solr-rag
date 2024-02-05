# Solr RAG Sample

## System Architecture

![system-architecture](images/rag.png)

## Environment

### Machine Spec

|      | Size |
| :--- | :--- |
| RAM  | 16GB |
| VRAM | 8GB  |

###

|                | Version  |
| :------------- | :------- |
| Docker         | 20.10.21 |
| docker-compose | 1.29.2   |

## Usage

```bash
# initial
$ make all
# index already exists
$ make launch
```

Access http://localhost:8501 by any Browser.

## Related Documents

- [Solr でも RAG できるもん！](https://zenn.dev/sashimimochi/articles/be1122c813d989)
- [Solr でも RAG できるもん！の裏話](https://zenn.dev/sashimimochi/articles/29d78fadaf8b17)
