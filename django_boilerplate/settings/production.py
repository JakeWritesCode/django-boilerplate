# -*- coding: utf-8 -*-
"""Production settings."""

# Standard Library
from os import getenv  # noqa: F401

# 3rd-party
from base import *  # noqa: F403 F401

DEBUG = getenv("DEBUG", False)  # noqa: F405
ALLOWED_HOSTS = ["*"]
