LCC_DIR=./mysql/data/lcc/
KNBC_DIR=./mysql/data/knbc/
KWDLC_DIR=./mysql/data/kwdlc/
LOG_DIR=./solr/logs/
DATA_DIR=./solr/data/
APP_PYCACHE_DIR=./app/__pycache__/
BATCH_PYCACHE_DIR=./batch/__pycache__/
CALM2_URL=https://huggingface.co/TheBloke/calm2-7B-chat-GGUF/blob/main/calm2-7b-chat.Q5_K_M.gguf
MODEL_DIR=./app/model/

tsv:
	bash ./scripts/make_data.sh
log:
	mkdir -p $(LOG_DIR)
	sudo chmod 777 $(LOG_DIR)
clean:
	docker-compose down
	rm -rf $(LCC_DIR)
	rm -rf $(KNBC_DIR)
	rm -rf $(KWDLC_DIR)
	rm -f $(LOG_DIR)/*
	sudo rm -rf $(PYCACHE_DIR)
create-index:
	docker-compose exec batch python embedding_pipeline.py
docker-clean:
	docker-compose down
	docker volume prune
	rm -rf solr/logs/*
	sudo rm -rf $(BATCH_PYCACHE_DIR)
	sudo rm -rf $(APP_PYCACHE_DIR)
launch:
	docker-compose --profile basic up -d
upload-configset:
	bash ./scripts/upload_configset.sh langchain
	bash ./scripts/upload_configset.sh image
create-collection:
	sudo chmod 777 $(DATA_DIR)
	bash ./scripts/create_collection.sh langchain
	bash ./scripts/create_collection.sh image
make-collection:
	@make upload-configset
	@make create-collection
delete-collection:
	bash ./scripts/delete_collection.sh langchain
	bash ./scripts/delete_collection.sh image
add-index:
	docker-compose exec batch python index_pipeline.py
download-calm2:
	mkdir -p $(MODEL_DIR)
	wget $(CALM2_URL) -O $(MODEL_DIR)
quantize:
	docker-compose exec app ct2-transformers-converter --model $(MODEL_NAME) --quantization int8 --output_dir ct2_model_$(MODEL_NAME)
all:
	@make launch
	@make upload-configset
	@make create-collection
#	make create-index
	make add-index
