#!/bin/bash
set -euo pipefail

SOLR_URL="${SOLR_URL:-http://localhost:8983/solr}"
COLLECTION="${1:-langchain}"
MODEL_ID="${2:-BAAI/bge-m3}"
MODEL_NAME="embedding"

: "${HUGGINGFACE_API_KEY:?Set HUGGINGFACE_API_KEY before configuring the embedding model.}"

curl --fail-with-body -sS \
  -X PUT "${SOLR_URL}/${COLLECTION}/schema/text-to-vector-model-store" \
  -H "Content-Type: application/json" \
  --data-binary @- <<JSON
{
  "class": "dev.langchain4j.model.huggingface.HuggingFaceEmbeddingModel",
  "name": "${MODEL_NAME}",
  "params": {
    "accessToken": "${HUGGINGFACE_API_KEY}",
    "modelId": "${MODEL_ID}"
  }
}
JSON

printf "\nEmbedding model '%s' configured for collection '%s'.\n" "${MODEL_ID}" "${COLLECTION}"
