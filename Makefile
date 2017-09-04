clean: clean_pyc
clean_pyc:
	find . -type f -name "*.pyc" -delete || true

migrate:
	DJANGOENV=$(ENVIRONMENT) $(PROJECT_NAME)/manage.py migrate --noinput

reusedb_unittests:
	DJANGO_SETTINGS_MODULE=$(PROJECT_NAME).testing.settings REUSE_DB=1 DJANGOENV=testing $(PYTHON) $(PROJECT_NAME)/manage.py test $(TESTONLY) --with-spec --spec-color --nologcapture --keepdb

unittests:
	DJANGO_SETTINGS_MODULE=$(PROJECT_NAME).testing.settings DJANGOENV=testing $(PROJECT_NAME)/manage.py test $(TESTONLY) --with-spec --spec-color --nologcapture

run:
	python3 $(PROJECT_NAME)/manage.py runserver_plus 0.0.0.0:8000 --settings=$(PROJECT_NAME).$(ENVIRONMENT).settings || python $(PROJECT_NAME)/manage.py runserver 0.0.0.0:8000 --settings=$(PROJECT_NAME).$(ENVIRONMENT).settings

shell:
	python3 $(PROJECT_NAME)/manage.py shell_plus --settings=$(PROJECT_NAME).$(ENVIRONMENT).settings || python manage.py shell --settings=$(PROJECT_NAME).$(ENVIRONMENT).settings
