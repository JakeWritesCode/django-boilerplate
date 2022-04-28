# -*- coding: utf-8 -*-
"""Production settings."""

from base import *

DEBUG = getenv("DEBUG", False)
ALLOWED_HOSTS = ["*"]