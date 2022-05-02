# -*- coding: utf-8 -*-
"""Test for users views."""
# 3rd-party
from django.contrib.auth.hashers import make_password
from django.test import TestCase
from django.urls import reverse

# Project
from users import views
from users.forms import CustomUserLoginForm
from users.tests.factories import CustomUserFactory


class TestLogIn(TestCase):
    """Tests for the login view."""

    def setUp(self) -> None:  # noqa: D102
        self.url = reverse(views.log_in)
        self.password = "mypassword"
        self.user = CustomUserFactory(password=make_password(self.password))

    def test_view_renders_correct_template(self):
        """View should render the correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "log_in.html")

    def test_view_redirects_if_user_is_logged_in(self):
        """View should redirect if the user is authed."""
        self.client.login(email=self.user.email, password=self.password)
        response = self.client.get(self.url)
        assert response.url == reverse("index")

    def test_view_renders_correct_form(self):
        """View should render the corect form."""
        response = self.client.get(reverse("log-in"))
        assert isinstance(response.context["form"], CustomUserLoginForm)

    def test_unsuccessful_login_renders_errors(self):
        """Unsuccessful login should render the applicable errors in the template."""
        response = self.client.post(
            self.url,
            data={"email": "barry@white.com", "password": "not_a_password"},
        )
        for error in response.context["form"].errors.values():
            for error_text in error:
                assert error_text in str(response.content)

    def test_successful_login_auths_user_and_redirects(self):
        """A successful login should auth the user and redirect."""
        response = self.client.post(
            self.url,
            data={"email": self.user.email, "password": self.password},
        )
        assert response.wsgi_request.user.is_authenticated
        assert response.url == reverse("index")
