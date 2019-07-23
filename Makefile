install:
	pip install -r requirements.txt

migrate:
	python manage.py makemigrations --settings=bill.settings.development
	python manage.py migrate --settings=bill.settings.development

run:
	python manage.py runserver 0.0.0.0:5000 --settings=bill.settings.development
