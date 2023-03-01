
.PHONY: build
build:
	python manage.py makemigrations
	python manage.py migrate

.PHONY: start
start:
	python manage.py runserver

.PHONY: restart
restart:
	make build
	make start