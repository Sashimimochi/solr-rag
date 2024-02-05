#!/bin/bash

solr_url="http://localhost:8983/solr"
collection_name=$1

# Solrのコンテナ起動待機
wait_lanch_services() {
    while [ `curl -LI $solr_url -o /dev/null -w '%{http_code}\n' -s` -ne 200 ]; do
        echo "[INFO] waiting launch services. retry in 30s"
        sleep 30
    done
    echo "[INFO] successfully launch services!"
}

create_collection() {
        curl "${solr_url}/admin/collections?action=CREATE&name=${collection_name}&collection.configName=${collection_name}_conf&numShards=1&replicationFactor=1&maxShardsPerNode=1"
}

create_collection_with_retry() {
    max_retries=10
    retry_interval=5

    for ((retry_count=1; retry_count<=$max_retries; retry_count++)); do
        # コレクション一覧を取得
        collections_list=$(curl "$solr_url/admin/collections?action=LIST")

        # 取得した一覧に対象のコレクションが含まれているか確認
        if [[ "$collections_list" =~ "$collection_name" ]]; then
            echo "Collection '$collection_name' exists."
            break
        else
            echo "Collection '$collection_name' not found (Retry $retry_count/$max_retries)."
            curl "${solr_url}/admin/collections?action=CREATE&name=${collection_name}&collection.configName=${collection_name}_conf&numShards=1&replicationFactor=1&maxShardsPerNode=1"
            if [ $retry_count -eq $max_retries ]; then
                echo "Maximum retries reached. Exiting."
                exit 1
            fi
            sleep $retry_interval
        fi
    done
}

wait_lanch_services
create_collection_with_retry
