# Django settings for wwwhisper_service project.

from site_settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = False

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # TODO: uncomment the next line for simple clickjacking protection
    # (here or in nginx?):
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# Don't use just sessionid, to avoid collision with apps protected by wwwhisper.
SESSION_COOKIE_NAME = 'wwwhisper-sessionid'
CSRF_COOKIE_NAME = 'wwwhisper-csrftoken'

# Make session cookie valid until a browser closes.
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# TODO: change this:
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True

ROOT_URLCONF = 'wwwhisper_service.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'wwwhisper_service.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django_browserid',
    'wwwhisper_auth',
    'wwwhisper_admin'
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'wwwhisper_auth.backend.BrowserIDBackend',
)


ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: "/admin/api/users/%s/" % u.username,
}

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# TODO: make this email working?
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

if DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(name)s %(message)s'
                },
            'simple': {
                'format': '%(levelname)s %(name)s %(message)s'
                },
            },
        'handlers': {
            'console':{
                'level':'DEBUG',
                'class':'logging.StreamHandler',
                'formatter': 'simple'
                },
            },
        'loggers': {
            'django_browserid': {
                'handlers':['console'],
                'propagate': True,
                'level':'DEBUG',
                },
            'wwwhisper_auth': {
                'handlers':['console'],
                'propagate': True,
                'level':'DEBUG',
                },
            'wwwhisper_admin': {
                'handlers':['console'],
                'propagate': True,
                'level':'DEBUG',
                },
            'django.request': {
                'handlers': ['console'],
                'propagate': True,
                'level': 'DEBUG',
            },
            }
        }