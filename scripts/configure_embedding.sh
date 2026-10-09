#!/bin/bash
set -euo pipefail

SOLR_URL="${SOLR_URL:-http://localhost:8983/solr}"
COLLECTION="${1:-langchain}"
MODEL_ID="${2:-embed-multilingual-v3.0}"

: "${COHERE_API_KEY:?Set COHERE_API_KEY before configuring the embedding models.}"

register_model() {
  local model_name="$1"
  local input_type="$2"

  curl --fail-with-body -sS \
    -X PUT "${SOLR_URL}/${COLLECTION}/schema/text-to-vector-model-store" \
    -H "Content-Type: application/json" \
    --data-binary @- <<JSON
{
  "class": "dev.langchain4j.model.cohere.CohereEmbeddingModel",
  "name": "${model_name}",
  "params": {
    "apiKey": "${COHERE_API_KEY}",
    "modelName": "${MODEL_ID}",
    "inputType": "${input_type}",
    "timeout": 60,
    "logRequests": false,
    "logResponses": false,
    "maxRetries": 5
  }
}
JSON
}

# Cohere v3 embedding models distinguish document and query embeddings.
register_model "embedding-document" "search_document"
register_model "embedding-query" "search_query"

printf "\nCohere model '%s' configured for collection '%s'.\n" "${MODEL_ID}" "${COLLECTION}"
