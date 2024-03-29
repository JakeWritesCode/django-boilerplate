# -*- coding: utf-8 -*-
"""App for users."""
# 3rd-party
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """App config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
