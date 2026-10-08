DOC_DIR=./mysql/data/
LOG_DIR=./solr/logs/
INDEX_DIR=./solr/data/
APP_PYCACHE_DIR=./app/__pycache__/
BATCH_PYCACHE_DIR=./batch/__pycache__/
CALM2_MODEL=calm2-7b-chat.Q5_K_M.gguf
CALM2_URL=https://huggingface.co/TheBloke/calm2-7B-chat-GGUF/resolve/main/$(CALM2_MODEL)?download=true
MODEL_DIR=./app/model/
CT2_MODEL_DIR=ct2_model
CT2_MODEL_PATH=./app/$(CT2_MODEL_DIR)
RIINA_MODEL=rinna/japanese-gpt-neox-3.6b-instruction-ppo
EMBEDDING_MODEL=BAAI/bge-m3

tsv:
	bash ./scripts/make_data.sh
log:
	mkdir -p $(LOG_DIR)
	sudo chmod 777 $(LOG_DIR)
download-calm2:
	mkdir -p $(MODEL_DIR)
	if [ ! -e $(MODEL_DIR)/$(CALM2_MODEL) ]; then wget $(CALM2_URL) -O $(MODEL_DIR)/$(CALM2_MODEL); fi
docker-launch:
	docker-compose --profile basic up -d
upload-configset:
	bash ./scripts/upload_configset.sh langchain
create-collection:
	sudo chmod -R 777 $(INDEX_DIR)
	bash ./scripts/create_collection.sh langchain
	sudo chmod -R 777 $(INDEX_DIR)
make-collection:
	@make upload-configset
	@make create-collection
configure-embedding:
	bash ./scripts/configure_embedding.sh langchain $(EMBEDDING_MODEL)
create-index:
	@make configure-embedding
	docker-compose exec batch python index_pipeline.py
add-index:
	@make create-index
quantize:
	if [ ! -e $(CT2_MODEL_PATH) ]; then docker-compose exec app ct2-transformers-converter --model $(RIINA_MODEL) --quantization int8 --output_dir $(CT2_MODEL_DIR); fi
	sudo chmod -R 777 $(CT2_MODEL_PATH)
launch:
	@make docker-launch
	@make upload-configset
	@make make-collection
	@make configure-embedding
	open http://localhost:8501
all:
	@make tsv
	@make log
	@make download-calm2
	@make docker-launch
	@make upload-configset
	@make create-collection
	@make quantize
	@make add-index
	open http://localhost:8501
data-clean:
	rm -rf $(DOC_DIR)
	rm -rf $(INDEX_DIR)
	rm -rf $(MODEL_DIR)
	rm -rf $(CT2_MODEL_PATH)
docker-clean:
	docker-compose down
	docker volume prune
	rm -rf $(LOG_DIR)
	sudo rm -rf $(BATCH_PYCACHE_DIR)
	sudo rm -rf $(APP_PYCACHE_DIR)
clean:
	@make docker-clean
	@make data-clean
