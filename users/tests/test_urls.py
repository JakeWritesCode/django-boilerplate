# -*- coding: utf-8 -*-
"""Tests for urls.py."""


# 3rd-party
from django.test import SimpleTestCase
from django.urls import reverse

# Project
from users import views


class TestURLs(SimpleTestCase):
    """Test URLS for users app."""

    def test_sign_up_url(self):
        """Test url."""
        assert reverse(views.sign_up_email) == "/users/sign-up"

    def test_log_in_url(self):
        """Test url."""
        assert reverse(views.log_in) == "/users/log-in"

    def test_log_out_url(self):
        """Test url."""
        assert reverse(views.log_out) == "/users/log-out"

    def test_change_password_url(self):
        """Test url."""
        assert reverse(views.change_password) == "/users/change-password"

    def test_password_reset_url(self):
        """Test url."""
        assert reverse(views.password_reset) == "/users/reset-password"

    def test_password_reset_confirm_url(self):
        """Test url."""
        assert reverse("reset-password-confirm", args=[1, 1]) == "/users/reset-password-confirm/1/1"
