# -*- coding: utf-8 -*-
"""Tests for the users forms."""
# 3rd-party
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from django.test import TestCase

# Project
from users.forms import CustomUserCreationForm
from users.forms import CustomUserLoginForm
from users.models import CustomUser
from users.tests.factories import CustomUserFactory


class TestCustomUserCreationForm(TestCase):
    """Tests for the CustomUserCreationForm."""

    def setUp(self) -> None:  # noqa: D102
        self.form = CustomUserCreationForm()

    def test_form_subclasses_django_default_from(self):
        """Form should build on the django basic form."""
        assert isinstance(self.form, UserCreationForm)

    def test_form_config(self):
        """Check form configuration."""
        assert self.form.Meta.model == CustomUser
        assert self.form.Meta.fields == ("email", "first_name", "last_name")


class TestCustomUserLoginForm(TestCase):
    """Tests for CustomUserLoginForm."""

    def setUp(self) -> None:  # noqa: D102
        self.form = CustomUserLoginForm()

    def test_fields(self):
        """Email and password field should be configured, password should be password widget."""
        assert isinstance(self.form.base_fields["email"], forms.EmailField)
        assert isinstance(self.form.base_fields["password"], forms.CharField)
        assert isinstance(self.form.base_fields["password"].widget, forms.PasswordInput)

    def test_form_does_not_validate_if_no_existing_user(self):
        """If there is no matching user, form should raise a ValidationError."""
        self.form = CustomUserLoginForm(data={"email": "not@real.com", "password": "mypassword"})
        self.form.is_valid()
        assert self.form.errors["email"] == ["A user with this email does not exist."]

    def test_form_does_not_validate_if_incorrect_password(self):
        """Form should not validate if password is incorrect."""
        password = "testpassword"
        user = CustomUserFactory(password=make_password(password))
        self.form = CustomUserLoginForm(data={"email": user.email, "password": "notdapassword"})
        assert not self.form.is_valid()
        assert self.form.errors["password"] == ["The entered password is incorrect."]

    def test_form_validates_if_existing_user_and_correct_password(self):
        """If there is a matching user, form should validate."""
        password = "testpassword"
        user = CustomUserFactory(password=make_password(password))
        self.form = CustomUserLoginForm(data={"email": user.email, "password": password})
        assert self.form.is_valid()
