install:
	pip install -r requirements.txt

migrate:
	python manage.py makemigrations --settings=bill.settings.development
	python manage.py migrate --settings=bill.settings.development

run:
	python manage.py runserver 0.0.0.0:3122 --settings=bill.settings.development

shell:
	python manage.py shell --settings=bill.settings.development

container:
	docker-compose build
	docker-compose up
