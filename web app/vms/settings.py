from pathlib import Path
import env
import os
import pymysql

pymysql.install_as_MySQLdb()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ""  # i removed this secret code for my research privacy

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ["*"]

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "web.apps.WebConfig",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "vms.urls"
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

WSGI_APPLICATION = "vms.wsgi.application"


# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "vms",
        "USER": "root",
        "PASSWORD": "",
        "HOST": "127.0.0.1",
        "PORT": "3306",
        "OPTIONS": {"init_command": "SET sql_mode='STRICT_TRANS_TABLES'"},
    }
}


# Password validation
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


# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Tehran"
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = f"{BASE_DIR}/staticfiles"
STATICFILES_DIRS = [f"{BASE_DIR}/static"]

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# My constants ====
APP_LANGUAGE = "fa"
AVAILABLE_LANGUAGE = {"en", "fa"}
VERIFY_CODE_LENGTH = 4
CSRF_FAILURE_VIEW = "web.forms.csrf_failure"
LOW_BOUND_AGE = 18
HIGH_BOUND_AGE = 90  # Oldest person living: Kane Tanaka (119yrs)
DELETE_ACCOUNT_REASON_MAX_LENGTH = 5000
EMAIL_MOBILE_MAX_LENGTH = 255
SHOW_TIME = 600
REST_TIME = 800
BLOCK_PER_PARTICIPANT = 5
MAX_FLAG = 3
TARGET_PER_BLOCK = 30
FILLERS_PER_BLOCK = 22
VIGILANCE_PER_BLOCK = 9

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = env.API_EMAIL
EMAIL_HOST_PASSWORD = env.API_PASSWORD

SMS_USERNAME = env.API_SMS_USERNAME
SMS_PASSWORD = env.API_SMS_PASSWORD
SMS_PATTERN = env.API_SMS_PATTERN
