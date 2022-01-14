CONTAINERNAME=switch-neo4j

help:
	@echo "Utility commands"

setup: # Setup container to be ran
	@sh scripts/setup_neo4j.sh $(CONTAINERNAME)

clean: # Remove container
	@docker rm --force $(CONTAINERNAME)

veryclean: clean # Remove container and files
	@rm -rf neo4j

shell: # Run a shell inside runnig container
	@docker exec -it $(CONTAINERNAME) bash

create-dataset: # Download the dataset
	@echo "The dataset will be downloaded and mounted. This might take a while."
	@python scripts/setup_test_dataset.py
