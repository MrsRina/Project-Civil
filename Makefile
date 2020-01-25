install:
	pip install -r server/requirements/development.txt

run:
	python manage.py runserver 0.0.0.0:8000 --settings=server.settings.development

migrate:
	python manage.py makemigrations --settings=server.settings.development
	python manage.py migrate --settings=server.settings.development

shell:
	python manage.py shell	--settings=server.settings.development
