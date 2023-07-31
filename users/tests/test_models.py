# -*- coding: utf-8 -*-
"""Tests for users models."""
# Standard Library
from unittest.mock import MagicMock

# 3rd-party
from django.contrib.auth.hashers import check_password
from django.test import TestCase

# Project
from users.models import CustomUser
from users.models import CustomUserManager


class TestCustomUserManager(TestCase):
    """Tests for the CustomUserManager."""

    def setUp(self) -> None:  # noqa: D102
        self.manager = CustomUserManager()

    def test_create_user_raises_error_if_no_email_set(self):
        """_create_user should raise an error of there is no email."""
        with self.assertRaises(ValueError) as e:
            self.manager._create_user(email="", password="passwordz")
        assert "The user must have an email." in str(e.exception)

    def test_create_user_creates_a_user(self):
        """_create_user should raise an error of there is no email."""
        self.manager.model = CustomUser
        self.manager._create_user(email="jake@test.com", password="passwordz")
        user = CustomUser.objects.first()
        assert user.email == "jake@test.com"
        assert check_password("passwordz", user.password)

    def test_create_user_calls_hidden_method(self):
        """Public method should call private method."""
        self.manager._create_user = MagicMock()
        self.manager.create_user(email="barry@white.com", password="DaPassword", is_admin=True)
        self.manager._create_user.assert_called_once_with(
            "barry@white.com",
            "DaPassword",
            is_admin=True,
            is_staff=False,
            is_superuser=False,
        )

    def test_create_superuser_raises_error_if_staff_or_superuser_overridden(self):
        """Function should error if you try to override is_staff or is_superuser."""
        with self.assertRaises(ValueError) as e:
            self.manager.create_superuser("barry@manilow.com", "SickPassword1", is_staff=False)
        assert "Superuser must have is_staff=True." in str(e.exception)

        with self.assertRaises(ValueError) as e:
            self.manager.create_superuser("barry@manilow.com", "SickPassword1", is_superuser=False)
        assert "Superuser must have is_superuser=True." in str(e.exception)

    def test_create_superuser_calls_create_user(self):
        """Function should call _create_user method with correct args."""
        self.manager._create_user = MagicMock()
        self.manager.create_superuser(email="barry@white.com", password="DaPassword", is_admin=True)
        self.manager._create_user.assert_called_once_with(
            "barry@white.com",
            "DaPassword",
            is_admin=True,
            is_staff=True,
            is_superuser=True,
        )


class TestCustomUser(TestCase):
    """Tests for the custom user model."""

    def setUp(self) -> None:  # noqa: D102
        self.model = CustomUser

    def test_config(self):
        """Test basic model config."""
        assert isinstance(self.model.objects, CustomUserManager)
        assert self.model.USERNAME_FIELD == "email"
        assert self.model.REQUIRED_FIELDS == ["first_name", "last_name"]
