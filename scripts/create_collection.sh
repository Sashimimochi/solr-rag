#!/bin/bash

curl "http://localhost:8983/solr/admin/collections?action=CREATE&name=$1&collection.configName=$1_conf&numShards=1&replicationFactor=1&maxShardsPerNode=1"
