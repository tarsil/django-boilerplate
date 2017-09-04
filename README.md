Django boilerplate - The kolaiah Solution for all!
===============================================================================

# To install from template base
- `django-admin startproject --template=https://github.com/tiagoarasilva/django-boilerplate/archive/master.zip --extension=py,md,html,txt,less project_name`
- Make sure you change the project name

# Docker
- Change the {{ project_name }} in your docker file to the desired name

## Directory Structure
    {{ project_name }}/
        accounts/
            management/
                commands/
            app.py
            models.py
            views.py
            forms.py
        settings/
            settings.py
            utils.py
        static/
        templates/
        {{ project_name }}/
            settings.py
            urls.py
            wsgi.py
        manage.py
    requirements/
        common.txt
        developement.txt
        live.txt

# {{ project_name }} Docker
-  Run `docker volume create --name={{ project_name }}_db_data`
-  Run `docker-compose up`. It will download all the resources needed to build your docker image
-  Run `docker-compose exec {{ project_name }} bash` to go inside the container
-  Run `make run` to start the server (inside docker container)
-  Run `make shell` to start the shell_plus

If you want, you can create alias in your local machine inside the bash_profile to do automatically this for you

E.g.:

```Shell
alias shell_plus='docker-compose up exec {{ project_name }} bash && make run'
alias run_server='docker-compose up exec {{ project_name }} bash && make shell'
```


# Run Tests (If you ran migrations before and need to reconstruct the DB schema)
`make unittests TESTONLY='profiles.tests.models_tests'`
- OR
`make unittests TESTONLY='profiles.tests.models_tests:ProfileUserTest.test_create_user'` for a specific test

# If you only need to run the tests and models weren't changed before
`make reusedb_unittests TESTONLY='addresses.tests.models_tests`
### apps

All of your Django "apps" go in this directory. THese have models, views, forms,
templates or all of the above. These should be Python packages you would add to
your project's `INSTALLED_APPS` list.


### Requirements for MacOS and Windows

Install Homebrew (MacOS Users)
`/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`

Install OpenSSL or Upgrade (MacOS Users)
`brew install openssl`

Install VirtualenvWrapper
`https://virtualenvwrapper.readthedocs.io/en/latest/install.html`

Upgrade pip
`pip install --upgrade pip`

### Templates

Project-wide templates are located in templates/ template that defines
these blocks:

#### manage.py

The standard Django `manage.py`.

#### settings.py

Many good default settings for Django applications

#### urls.py

GrowYz `url_patterns` to serve static media when in solo development mode.
