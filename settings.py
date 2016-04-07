# Django settings for wayf project.
import os
here = lambda x: os.path.join(os.path.abspath(os.path.dirname(__file__)), x)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = ''           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = ''             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Athens'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = here('static')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'w70vxdbe(^&92@^a)b%jm=8p0@-o$ykbfal2)tn%ssky(t*z5l'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    #'filesystem_multilingual.load_template_source',
    'django.template.loaders.filesystem.Loader',
    #'django.template.loaders.app_directories.load_template_source',
    # 'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'middleware.VhostMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    here('templates'),
)

INSTALLED_APPS = (
    'wayf',
    'aai',
)

IDP_COOKIE = 'grnet_selected_idp'
SHIB_METADATA = 'federation-metadata.xml'
LAST_IDP_COOKIE = 'grnet_last_idp'
COOKIE_DOMAIN = '.grnet.gr'
LANGUAGE_COOKIE_NAME = 'grnet_aai_language'

WAYF_SITENAME='localhost:8000'
INSTITUTION_CATEGORIES = (
      ('university', ("Universities")),
      ('tei',  ("Technological educational institutes")),
      ('school',  ("Other academic institutions")),
      ('institute', ("Research institutes")),
      ('other', ("Please select your institute")),
      ('test', ("Testing")),
)
P3P_HEADER = 'CP="NOI CUR DEVa OUR IND COM NAV PRE"'
