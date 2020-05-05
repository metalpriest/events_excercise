test:
	pytest

install:
	pip install -r requirements.txt
	python manage.py migrate

run:
	python manage.py runserver 127.0.0.1:8000

test-docker:
	docker-compose exec api pytest
