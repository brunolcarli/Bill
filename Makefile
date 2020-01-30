install:
	pip install -r requirements.txt

migrate:
	python manage.py makemigrations --settings=bill.settings.development
	python manage.py migrate --settings=bill.settings.development

run:
	python manage.py runserver 0.0.0.0:3122 --settings=bill.settings.development


init_bill:
	# python manage.py makemigrations --settings=bill.settings.docker
	# python manage.py migrate --settings=bill.settings.docker
	python manage.py runserver 0.0.0.0:3122 --settings=bill.settings.docker
