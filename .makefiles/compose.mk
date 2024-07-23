.PHONY: up-local

command-prefix=docker compose -f compose.local.yml

up-local: merge-dotenv
	$(command-prefix) up -d

build-local: merge-dotenv
	$(command-prefix) build
	docker system prune -f

down-local:
	$(command-prefix) down -v

restart-local:
	$(command-prefix) restart

attach-instance:
	$(command-prefix) exec instance sh
