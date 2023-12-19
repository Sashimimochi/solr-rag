#!/bin.bash

add_dih() {
    # リポジトリ追加
    docker-compose exec solr_node1 bin/solr package add-repo data-import-handler "https://raw.githubusercontent.com/searchscale/dataimporthandler/master/repo/"
    # パッケージのインストール
    docker-compose exec solr_node1 bin/solr package install data-import-handler
    # パッケージのデプロイ
    docker-compose exec solr_node1 bin/solr package deploy data-import-handler -y -collections langchain
}

index() {
    echo curl "http://localhost:8983/solr/langchain/dataimport?command=full-import&entity=tutorial"
}
