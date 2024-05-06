.ONESHELL:

SHELL=/bin/bash

.PHONY: migrate

migrate:
	python3 -m cli.migrate
