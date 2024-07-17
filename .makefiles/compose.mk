.PHONY: up-local

command-prefix=docker compose -f compose.local.yml

up-local: merge-dotenv
	$(command-prefix) up -d

build-local: merge-dotenv
	$(command-prefix) build
	docker system prune -f

down-local:
	$(command-prefix) down -v
