# -*- coding: utf-8 -*-
"""Tests for the users app apps.py."""

# 3rd-party
from django.test import SimpleTestCase

# Project
from users.apps import UsersConfig


class TestUsersConfig(SimpleTestCase):
    """Test the app config."""

    def test_config(self):
        """Test the app is configured correctly."""
        config = UsersConfig
        assert config.default_auto_field == "django.db.models.BigAutoField"
        assert config.name == "users"
