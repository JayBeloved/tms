"""
Django settings for tenantproject project.

"""

from pathlib import Path

import dj_database_url
from decouple import Csv, config

from django.contrib.messages import constants as messages

BASE_DIR = Path(__file__).resolve().parent.parent


# ==============================================================================
# CORE SETTINGS
# ==============================================================================

SECRET_KEY = config("SECRET_KEY", default='django-insecure-#h(%%r9srq(y#vxfr9g3^a)n4g3=19!ag#$viqbz1=f*2zjh*u')

DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="127.0.0.1,localhost", cast=Csv())


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "tms.apps.accounts",
    "tms.apps.core",
    "tms.apps.landlords",
    "tms.apps.properties",
    "tms.apps.tenants",

]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ROOT_URLCONF = "tms.urls"

INTERNAL_IPS = ["127.0.0.1"]

WSGI_APPLICATION = "tms.wsgi.application"

# ==============================================================================
# MIDDLEWARE SETTINGS
# ==============================================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ==============================================================================
# TEMPLATES SETTINGS
# ==============================================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ==============================================================================
# DATABASES SETTINGS
# ==============================================================================

DATABASES = {
    "default": dj_database_url.config(
        default=config("DATABASE_URL", default="mysql://tms_admin:my-tms2022_@localhost:3306/tms"),
        conn_max_age=600,
    )
}

# ==============================================================================
# AUTHENTICATION AND AUTHORIZATION SETTINGS
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# ==============================================================================
# I18N AND L10N SETTINGS
# ==============================================================================

LANGUAGE_CODE = config("LANGUAGE_CODE", default="en-us")

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = False

LOCALE_PATHS = [BASE_DIR / "locale"]

# ==============================================================================
# STATIC FILES SETTINGS
# =============================================================================

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR.parent.parent / "staticfiles"

STATICFILES_DIRS = [BASE_DIR / "static"]


# ==============================================================================
# MEDIA FILES SETTINGS
# ==============================================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR.parent.parent / "media"


# ==============================================================================
# THIRD-PARTY SETTINGS
# ==============================================================================


# ==============================================================================
# FIRST-PARTY SETTINGS
# ==============================================================================

TMS_ENVIRONMENT = config("TMS_ENVIRONMENT", default="local")

# Custom Auth Settings
AUTH_USER_MODEL = 'accounts.user'

LOGIN_URL = 'login'

LOGOUT_URL = 'logout'

LOGOUT_REDIRECT_URL = 'landing'

# Messages built-in framework

MESSAGE_TAGS = {
    messages.DEBUG: 'text-primary',
    messages.INFO: 'text-info',
    messages.SUCCESS: 'text-success',
    messages.WARNING: 'text-warning',
    messages.ERROR: 'text-danger',
}
