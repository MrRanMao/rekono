'''Django settings for rekono project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
'''

import os
import sys
from datetime import timedelta
from pathlib import Path
from typing import Any, Dict

from findings.enums import Severity
from input_types.enums import InputTypeNames
from targets.enums import TargetType
from tasks.enums import Status, TimeUnit
from tools.enums import IntensityRank

from rekono.config import RekonoConfigLoader
from rekono.environment import (ENV_REKONO_HOME, RKN_ALLOWED_HOSTS,
                                RKN_CMSEEK_RESULTS, RKN_DB_HOST, RKN_DB_NAME,
                                RKN_DB_PASSWORD, RKN_DB_PORT, RKN_DB_USER,
                                RKN_DD_API_KEY, RKN_DD_URL, RKN_EMAIL_HOST,
                                RKN_EMAIL_PASSWORD, RKN_EMAIL_PORT,
                                RKN_EMAIL_USER, RKN_FRONTEND_URL,
                                RKN_GITTOOLS_DIR, RKN_LOG4J_SCANNER_DIR,
                                RKN_OTP_EXPIRATION_HOURS, RKN_RQ_HOST,
                                RKN_RQ_PORT, RKN_SECRET_KEY, RKN_TELEGRAM_BOT,
                                RKN_TELEGRAM_TOKEN, RKN_TRUSTED_PROXY,
                                RKN_UPLOAD_FILES_MAX_MB)

################################################################################
# Rekono basic information                                                     #
################################################################################

DESCRIPTION = 'Execute full pentesting processes combining multiple hacking tools automatically'    # Rekono description
VERSION = '1.0.1'                                                               # Rekono version


################################################################################
# Paths and directories                                                        #
################################################################################

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')                               # Frontend directory

# Rekono home directory. By default /opt/rekono
REKONO_HOME = os.getenv(ENV_REKONO_HOME, '/opt/rekono')
if not os.path.isdir(REKONO_HOME):                                              # Rekono home doesn't exist
    REKONO_HOME = str(BASE_DIR.parent)                                          # Use current directory as home

REPORTS_DIR = os.path.join(REKONO_HOME, 'reports')                              # Directory to save tool reports
WORDLIST_DIR = os.path.join(REKONO_HOME, 'wordlists')                           # Directory to save wordlist files
LOGGING_DIR = os.path.join(REKONO_HOME, 'logs')                                 # Directory to save log files

for dir in [REPORTS_DIR, WORDLIST_DIR, LOGGING_DIR]:                            # Initialize directories if needed
    if not os.path.isdir(dir):
        os.mkdir(dir)

CONFIG_FILE = ''                                                                # Config file
for filename in ['config.yaml', 'config.yml', 'rekono.yaml', 'rekono.yml']:     # For each config filename
    if os.path.isfile(os.path.join(REKONO_HOME, filename)):                     # Check if config file exists
        CONFIG_FILE = os.path.join(REKONO_HOME, filename)
CONFIG = RekonoConfigLoader(CONFIG_FILE)                                        # Load configuration


################################################################################
# Django                                                                       #
################################################################################

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'taggit',
    'django_rq',
    'drf_spectacular',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'executions',
    'findings',
    'input_types',
    'processes',
    'projects',
    'rekono',
    'resources',
    'security',
    'targets',
    'tasks',
    'telegram_bot',
    'tools',
    'users'
]

MIDDLEWARE = [
    'security.middleware.RekonoSecurityMiddleware',                             # Includes security response headers
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rekono.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'email_notifications', 'templates')          # Templates for email messages
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'rekono.wsgi.application'

TESTING = 'test' in sys.argv                                                    # Tests execution


################################################################################
# Security                                                                     #
################################################################################

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(RKN_SECRET_KEY, CONFIG.SECRET_KEY)                       # Django secret key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TRUSTED_PROXY = os.getenv(RKN_TRUSTED_PROXY) == 'true'

allowed_hosts = os.getenv(RKN_ALLOWED_HOSTS)
if allowed_hosts and ' ' in allowed_hosts:
    ALLOWED_HOSTS = allowed_hosts.split(' ')                                    # Multiple allowed hosts from env
elif allowed_hosts and ',' in allowed_hosts:
    ALLOWED_HOSTS = allowed_hosts.split(',')                                    # Multiple allowed hosts from env
elif allowed_hosts:
    ALLOWED_HOSTS = [allowed_hosts]                                             # One allowed host from env
else:
    ALLOWED_HOSTS = CONFIG.ALLOWED_HOSTS                                        # Default allowed hosts

AUTH_USER_MODEL = 'users.User'                                                  # User model

# OTP expiration time in hours
OTP_EXPIRATION_HOURS = int(os.getenv(RKN_OTP_EXPIRATION_HOURS, CONFIG.OTP_EXPIRATION_HOURS))

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'security.passwords.PasswordComplexityValidator',               # Custom password policy
    }
]

# JWT configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),                              # Access token expiration after 5 min
    'REFRESH_TOKEN_LIFETIME': timedelta(hours=1),                               # Refresh token expiration after 1 hour
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS512',
    'SIGNING_KEY': SECRET_KEY
}

# Max allowed size in MB for upload files
UPLOAD_FILES_MAX_MB = int(1 if TESTING else os.getenv(RKN_UPLOAD_FILES_MAX_MB, CONFIG.UPLOAD_FILES_MAX_MB))

LOGGING = {                                                                     # Logging configuration
    'version': 1,
    'disable_existing_loggers': True,                                           # Disable default Django logging system
    'formatters': {
        'rekono': {
            'format': '%(asctime)s [%(levelname)s] - %(process)d %(module)s - %(source_ip)s - %(user)s - %(message)s'
        }
    },
    'filters': {
        'rekono': {
            '()': 'api.log.RekonoLoggingFilter',                                # Custom logging filter
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'rekono',
            'filters': ['rekono'],
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGGING_DIR, 'rekono.log'),
            'maxBytes': 50 * 1024 * 1024,                                       # Max. 50 MB per file
            'backupCount': 10,
            'formatter': 'rekono',
            'filters': ['rekono'],
        }
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'DEBUG' if DEBUG else 'INFO',
        'propagate': False,
    }
}

################################################################################
# API Rest                                                                     #
################################################################################

REST_FRAMEWORK: Dict[str, Any] = {
    'DEFAULT_METADATA_CLASS': None,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'api.filters.RekonoSearchFilter',
        'api.filters.RekonoOrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'api.pagination.Pagination',                    # Pagination configuration
    'ORDERING_PARAM': 'order',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',                    # Authentication via API token
        'rest_framework_simplejwt.authentication.JWTAuthentication',            # Authentication via JWT token
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',                           # Authentication required by default
        'rest_framework.permissions.DjangoModelPermissions',                    # Authorization based on permissions
        'security.authorization.permissions.ProjectMemberPermission',           # and in project membership
    ]
}
if not TESTING:                                                                 # Rate limit only for real environments
    REST_FRAMEWORK.update({                                                     # pragma: no cover
        'DEFAULT_THROTTLE_CLASSES': [
            'rest_framework.throttling.AnonRateThrottle',                       # Rate limit for anonymous users
            'rest_framework.throttling.UserRateThrottle',                       # Rate limit for authenticated users
            'rest_framework.throttling.ScopedRateThrottle',                     # Rate limit for specific cases
        ],
        'DEFAULT_THROTTLE_RATES': {
            # 2 requests by second by IP
            # To allow requests from different users with same public IP address
            # Note that most API requests requires authentication
            'anon': '100/min',
            # 4 request by second by user
            # It is enough for legitimate usage, but attacks will be blocked
            'user': '300/min',
            # Prevent brute force attacks in login and refresh token features
            # Login is not authenticated, we can receive many requests from different users with same public IP address
            'login': '30/min',
            # The frontend can generate many refresh requests for the same user
            'refresh': '30/min',
        }
    })

# Documentation

SPECTACULAR_SETTINGS = {
    'TITLE': 'Rekono API Rest',
    'DESCRIPTION': DESCRIPTION,
    'VERSION': VERSION,
    'PREPROCESSING_HOOKS': [
        'drf_spectacular.hooks.preprocess_exclude_path_format'
    ],
    'ENUM_NAME_OVERRIDES': {
        'StatusEnum': Status.choices,
        'SeverityEnum': Severity.choices,
        'TimeUnitEnum': TimeUnit.choices,
        'IntensityEnum': IntensityRank.choices,
        'InputTypeNamesEnum': InputTypeNames.choices,
        'TargetTypeEnum': TargetType.choices,
    }
}


################################################################################
# Database                                                                     #
################################################################################

# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

if TESTING:
    DATABASES = {                                                               # In memory database for testing
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:'
        }
    }
else:
    # Production database
    DATABASES = {                                                               # pragma: no cover
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv(RKN_DB_NAME, CONFIG.DB_NAME),
            'USER': os.getenv(RKN_DB_USER, CONFIG.DB_USER),
            'PASSWORD': os.getenv(RKN_DB_PASSWORD, CONFIG.DB_PASSWORD),
            'HOST': os.getenv(RKN_DB_HOST, CONFIG.DB_HOST),
            'PORT': os.getenv(RKN_DB_PORT, CONFIG.DB_PORT),
        }
    }

################################################################################
# Redis Queues                                                                 #
################################################################################

RQ_QUEUES = {
    'tasks-queue': {
        'HOST': os.getenv(RKN_RQ_HOST, CONFIG.RQ_HOST),
        'PORT': os.getenv(RKN_RQ_PORT, CONFIG.RQ_PORT),
        'DB': 0,
        'DEFAULT_TIMEOUT': 60                                                   # 1 minute
    },
    'executions-queue': {
        'HOST': os.getenv(RKN_RQ_HOST, CONFIG.RQ_HOST),
        'PORT': os.getenv(RKN_RQ_PORT, CONFIG.RQ_PORT),
        'DB': 0,
        'DEFAULT_TIMEOUT': 7200                                                 # 2 hours
    },
    'findings-queue': {
        'HOST': os.getenv(RKN_RQ_HOST, CONFIG.RQ_HOST),
        'PORT': os.getenv(RKN_RQ_PORT, CONFIG.RQ_PORT),
        'DB': 0,
        'DEFAULT_TIMEOUT': 1200                                                 # 20 minutes
    },
    'emails-queue': {
        'HOST': os.getenv(RKN_RQ_HOST, CONFIG.RQ_HOST),
        'PORT': os.getenv(RKN_RQ_PORT, CONFIG.RQ_PORT),
        'DB': 0,
        'DEFAULT_TIMEOUT': 300                                                  # 5 minutes
    }
}


################################################################################
# Email                                                                        #
################################################################################

DEFAULT_FROM_EMAIL = 'Rekono <noreply@rekono.com>'                              # Email from address
EMAIL_HOST = os.getenv(RKN_EMAIL_HOST, CONFIG.EMAIL_HOST)                       # SMTP host
EMAIL_PORT = os.getenv(RKN_EMAIL_PORT, CONFIG.EMAIL_PORT)                       # SMTP port
EMAIL_HOST_USER = os.getenv(RKN_EMAIL_USER, CONFIG.EMAIL_USER)                  # User for auth in SMTP server
EMAIL_HOST_PASSWORD = os.getenv(RKN_EMAIL_PASSWORD, CONFIG.EMAIL_PASSWORD)      # Password for auth in SMTP server
EMAIL_USE_TLS = CONFIG.EMAIL_TLS


################################################################################
# Telegram                                                                     #
################################################################################

TELEGRAM_BOT = os.getenv(RKN_TELEGRAM_BOT, CONFIG.TELEGRAM_BOT)                 # Telegram bot name
TELEGRAM_TOKEN = os.getenv(RKN_TELEGRAM_TOKEN, CONFIG.TELEGRAM_TOKEN)           # Telegram token provided by BotFather


################################################################################
# Defect-Dojo                                                                  #
################################################################################

DEFECT_DOJO = {
    'URL': os.getenv(RKN_DD_URL, CONFIG.DD_URL),
    'API_KEY': os.getenv(RKN_DD_API_KEY, CONFIG.DD_API_KEY),                    # Defect-Dojo API key
    'VERIFY_TLS': CONFIG.DD_VERIFY_TLS,                                         # Defect-Dojo TLS verification
    'TAGS': CONFIG.DD_TAGS,                                                     # Tags to be included in DD entities
    'PRODUCT_TYPE': CONFIG.DD_PRODUCT_TYPE,                                     # Product type for new DD products
    'TEST_TYPE': CONFIG.DD_TEST_TYPE,                                           # Rekono test type name in Defect-Dojo
    'TEST': CONFIG.DD_TEST                                                      # Rekono test name in Defect-Dojo
}


################################################################################
# Tools                                                                        #
################################################################################

TOOLS = {
    'cmseek': {
        'directory': os.getenv(RKN_CMSEEK_RESULTS, CONFIG.TOOLS_CMSEEK_DIR)     # CMSeeK directory
    },
    'log4j-scanner': {
        'directory': os.getenv(RKN_LOG4J_SCANNER_DIR, CONFIG.TOOLS_LOG4J_SCANNER_DIR)     # Log4j Scanner directory
    },
    'gittools': {
        'directory': os.getenv(RKN_GITTOOLS_DIR, CONFIG.TOOLS_GITTOOLS_DIR)     # GitTools directory
    }
}


################################################################################
# Frontend                                                                     #
################################################################################

# Rekono frontend address. It's used to include links in notifications
FRONTEND_URL = os.getenv(RKN_FRONTEND_URL, CONFIG.FRONTEND_URL)


################################################################################
# Miscellaneous                                                                #
################################################################################

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'CET'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(REKONO_HOME, 'static')

if not os.path.isdir(STATIC_ROOT):
    os.mkdir(STATIC_ROOT)

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
