# development.settings will pull in (probably global) local_settings,
# which messes things up
from {{ project_name }}.settings import *
import os

DEBUG = True

TESTING = True

DJANGOENV = "testing"

REUSE_DB = bool(int(os.environ.get("REUSE_DB", 0)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'postgres',
        'PORT': '5432',
    }
}

if REUSE_DB:
    DATABASE_ROUTERS = []

POSTGIS_TEMPLATE = "template_postgis"
POSTGIS_VERSION = (2, 1, 2)

SOUTH_TESTS_MIGRATE = bool(int(os.environ.get("MIGRATE", 0)))

DEBUG_TOOLBAR_PANELS = ()

SECURE_SSL_REDIRECT = False

# ensure that no matter what's in local_settings we use that
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
MEDIA_URL = '/media/'

STATIC_ROOT = '/tmp/assets-upload'
STATIC_URL = "/static/"

MEDIA_ROOT = '/tmp/media-root'

# Roll in the API URLs so we can test everything in one go
API_URLS_IN_MAIN = True

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Shut up debugging spam from Django by default
NOSE_ARGS = ["--logging-clear-handlers", "--logging-filter", "INFO"]

# Give ourselves a test instance of redis
REDIS_SERVER = ('redis', 6379, 2)  # host, port, dbs
REDIS_PASSWORD = None

# We don't want to run Memcached for tests.
SESSION_ENGINE = "django.contrib.sessions.backends.db"


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
    'api': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
    'staticfiles': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
    'depictions': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
    'thumbnails': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
}

# allow for a local override that won't be used by development
try:
    from {{ project_name }}.{{ project_name }}.testing.local_settings import *
except ImportError:
    pass


# We don't care about secure password for tests, use MD5 which is faster.
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
    # This one is only needed for some of the old fixtures.
    'django.contrib.auth.hashers.SHA1PasswordHasher',
)


LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    'root': {
        'level': 'INFO',
        'handlers': ['console'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    "handlers": {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    }
}


MIDDLEWARE = list(MIDDLEWARE)
if 'bugsnag.django.middleware.BugsnagMiddleware' in MIDDLEWARE:
    MIDDLEWARE.remove('bugsnag.django.middleware.BugsnagMiddleware')

COMPRESS_ENABLED = False
