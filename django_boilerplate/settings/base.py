# -*- coding: utf-8 -*-
"""Base settings."""

# Standard Library
from os import getenv
from pathlib import Path

# 3rd-party
from django.contrib.messages import constants as messages
from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = getenv("DJANGO_SECRET_KEY")
DEBUG = getenv("DEBUG", False)

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Apps
    "users",
    # 3rd party modules
    "crispy_forms",
    "social_django",
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

ROOT_URLCONF = "django_boilerplate.urls"

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
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ],
        },
    },
]

WSGI_APPLICATION = "django_boilerplate.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": getenv("POSTGRES_DB_NAME"),
        "USER": getenv("POSTGRES_DB_USER"),
        "PASSWORD": getenv("POSTGRES_DB_PASSWORD"),
        "HOST": getenv("POSTGRES_DB_HOST"),
        "PORT": getenv("POSTGRES_DB_PORT"),
    },
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
CRISPY_TEMPLATE_PACK = "bootstrap4"

AUTH_USER_MODEL = "users.CustomUser"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = getenv("OUTGOING_GMAIL_ADDRESS")
EMAIL_HOST_PASSWORD = getenv("OUTGOING_GMAIL_APP_PASSWORD")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST

# Convert django messages to bootstrap.
MESSAGE_TAGS = {
    messages.DEBUG: "alert-secondary",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}

SOCIAL_AUTH_JSONFIELD_ENABLED = True
SOCIAL_AUTH_CONFIG = {
    "Google": {
        "enabled": True,
        "backend": "social_core.backends.google.GoogleOAuth2",
        "icon": "fa-brands fa-google",
        "human_readable_name": "Google",
        "url": reverse_lazy("social:begin", args=["google-oauth2"]),
        "key": getenv("GOOGLE_OAUTH2_KEY"),
        "secret": getenv("GOOGLE_OAUTH2_SECRET"),
        "scope": ["profile", "email"],
    },
    "Facebook": {
        "enabled": True,
        "backend": "social_core.backends.facebook.FacebookOAuth2",
        "icon": "fa-brands fa-facebook",
        "human_readable_name": "Facebook",
        "url": reverse_lazy("social:begin", args=["facebook"]),
        "key": getenv("FACEBOOK_OAUTH2_KEY"),
        "secret": getenv("FACEBOOK_OAUTH2_SECRET"),
        "scope": ["email"],
    },
    "Azure AD": {
        "enabled": True,
        "backend": "social_core.backends.azuread.AzureADOAuth2",
        "icon": "fa-brands fa-microsoft",
        "human_readable_name": "Microsoft",
        "url": reverse_lazy("social:begin", args=["azuread-oauth2"]),
        "key": getenv("AZUREAD_OAUTH2_KEY"),
        "secret": getenv("AZUREAD_OAUTH2_SECRET"),
    },
    "Django": {
        "enabled": True,
        "backend": "django.contrib.auth.backends.ModelBackend",
        "icon": "fa-solid fa-envelope",
        "human_readable_name": "email",
        "url": reverse_lazy("sign-up-email"),
    },
}

# This stuff is fed from the dict above
AUTHENTICATION_BACKENDS = [
    *[provider["backend"] for provider in SOCIAL_AUTH_CONFIG.values() if provider["enabled"]],
]
SOCIAL_AUTH_URL_NAMESPACE = "social_auth"
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = SOCIAL_AUTH_CONFIG["Google"]["key"]
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = SOCIAL_AUTH_CONFIG["Google"]["secret"]
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = SOCIAL_AUTH_CONFIG["Google"]["scope"]
SOCIAL_AUTH_FACEBOOK_KEY = SOCIAL_AUTH_CONFIG["Facebook"]["key"]
SOCIAL_AUTH_FACEBOOK_SECRET = SOCIAL_AUTH_CONFIG["Facebook"]["secret"]
SOCIAL_AUTH_FACEBOOK_SCOPE = SOCIAL_AUTH_CONFIG["Facebook"]["scope"]
SOCIAL_AUTH_AZUREAD_OAUTH2_KEY = SOCIAL_AUTH_CONFIG["Azure AD"]["key"]
SOCIAL_AUTH_AZUREAD_OAUTH2_SECRET = SOCIAL_AUTH_CONFIG["Azure AD"]["secret"]
