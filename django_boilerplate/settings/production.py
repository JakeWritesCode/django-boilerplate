# -*- coding: utf-8 -*-
"""Production settings."""

# 3rd-party
from base import *  # noqa: F403

DEBUG = getenv("DEBUG", False)  # noqa: F405
ALLOWED_HOSTS = ["*"]
