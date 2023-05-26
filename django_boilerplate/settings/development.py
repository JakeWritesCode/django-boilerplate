# -*- coding: utf-8 -*-
"""Development settings."""

# Local
from .base import *  # noqa: F403

DEBUG = getenv("DEBUG", True)  # noqa: F405

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase', # This is where you put the name of the db file.
                 # If one doesn't exist, it will be created at migration time.
    }
}
