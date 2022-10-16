deploy:
	docker compose up -d

dev_deploy:
    docker compose up -d --remove-orphans