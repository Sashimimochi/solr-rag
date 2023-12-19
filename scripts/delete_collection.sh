#!/bin/bash

curl "http://localhost:8983/solr/admin/collections?action=DELETE&name=$1"
