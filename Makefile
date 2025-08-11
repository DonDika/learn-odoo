WEB_DB_NAME = odoo-learn-db  # <- put your Odoo database name here
DOCKER = docker
DOCKER_COMPOSE = $(DOCKER) compose
CONTAINER_ODOO = odoo-app
CONTAINER_DB = odoo-db
DB_USER = odoo
DB_PASSWORD = myodoo

help:
	@echo "Available targets:"
	@echo "  start                  Start the compose with daemon"
	@echo "  stop                   Stop the compose"
	@echo "  restart                Restart the compose"
	@echo "  addons <addon_names>   Restart instance and upgrade addons (comma-separated)"
	@echo "  console                Odoo interactive console"
	@echo "  psql                   PostgreSQL interactive shell"
	@echo "  logs odoo              Logs the odoo container"
	@echo "  logs db                Logs the odoo-postgres container"

start:
	$(DOCKER_COMPOSE) up -d

stop:
	$(DOCKER_COMPOSE) down

restart:
	$(DOCKER_COMPOSE) restart

# psql:
# 	$(DOCKER) exec -it $(CONTAINER_DB) psql -U $(CONTAINER_ODOO) -d $(WEB_DB_NAME)
psql:
	$(DOCKER) exec -it $(CONTAINER_DB) psql -U $(DB_USER) -d $(WEB_DB_NAME)


# console:
# 	$(DOCKER) exec -it $(CONTAINER_ODOO) odoo shell --db_host=$(CONTAINER_DB) -d $(WEB_DB_NAME) -r $(CONTAINER_ODOO) -w $(CONTAINER_ODOO)
console:
	$(DOCKER) exec -it $(CONTAINER_ODOO) odoo shell --db_host=$(CONTAINER_DB) -d $(WEB_DB_NAME) -r $(DB_USER) -w $(DB_PASSWORD)

define log_target
	@if [ "$(1)" = "odoo" ]; then \
		$(DOCKER_COMPOSE) logs -f $(CONTAINER_ODOO); \
	elif [ "$(1)" = "db" ]; then \
		$(DOCKER_COMPOSE) logs -f $(CONTAINER_DB); \
	else \
		echo "Invalid logs target. Use 'make logs odoo' or 'make logs db'."; \
	fi
endef

logs:
	$(call log_target,$(word 2,$(MAKECMDGOALS)))

# define upgrade_addons
# 	$(DOCKER) exec -it $(CONTAINER_ODOO) odoo --db_host=$(CONTAINER_DB) -d $(WEB_DB_NAME) -r $(CONTAINER_ODOO) -w $(CONTAINER_ODOO) -u $(1) --dev xml
# endef
define upgrade_addons
	$(DOCKER) exec -it $(CONTAINER_ODOO) odoo --db_host=$(CONTAINER_DB) -d $(WEB_DB_NAME) -r $(DB_USER) -w $(DB_PASSWORD) -u $(1) --dev xml
endef


addons: restart
	@for addon in $(filter-out $@,$(MAKECMDGOALS)); do \
		$(call upgrade_addons,$$addon); \
	done

.PHONY: start stop restart console psql logs odoo db addons