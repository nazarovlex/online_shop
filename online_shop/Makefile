

.PHONY: build
build:
	pip install -r requirements.txt
	python manage.py makemigrations
	python manage.py migrate

.PHONY: start
start:
	python manage.py runserver

.PHONY: restart
restart:
	make build
	make start