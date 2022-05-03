# -*- coding: utf-8 -*-
"""Test for users views."""
# Standard Library
from unittest.mock import ANY
from unittest.mock import MagicMock
from unittest.mock import patch

# 3rd-party
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import INTERNAL_RESET_SESSION_TOKEN
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory
from django.test import TestCase
from django.urls import reverse
from django.urls import reverse_lazy

# Project
from users import views
from users.forms import CustomUserCreationForm
from users.forms import CustomUserLoginForm
from users.models import CustomUser
from users.tests.factories import CustomUserFactory
from users.views import CustomPasswordResetConfirmView


class TestSignUp(TestCase):
    """Tests for the signup view."""

    def setUp(self) -> None:  # noqa: D102
        self.url = reverse(views.sign_up)
        self.password = "$uper_Str0ng_P4$$word!?"
        self.user = CustomUserFactory(password=make_password(self.password))
        self.user_data = {
            "email": "test@user.com",
            "first_name": "Test",
            "last_name": "User",
            "password1": self.password,
            "password2": self.password,
        }

    def test_view_renders_correct_template(self):
        """View should render the correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "sign_up.html")

    def test_view_redirects_if_user_is_logged_in(self):
        """View should redirect if the user is authed."""
        self.client.login(email=self.user.email, password=self.password)
        response = self.client.get(self.url)
        assert response.url == reverse("index")

    def test_view_renders_correct_form(self):
        """View should render the correct form."""
        response = self.client.get(self.url)
        assert isinstance(response.context["form"], CustomUserCreationForm)

    def test_unsuccessful_signup_renders_errors(self):
        """Unsuccessful signup should render the applicable errors in the template."""
        response = self.client.post(
            self.url,
            data={"email": "barry@white.com", "password": "not_a_password"},
        )
        for error in response.context["form"].errors.values():
            for error_text in error:
                assert error_text in str(response.content)

    def test_successful_signup_creates_new_user_in_db(self):
        """Successful signup should create a new user in the DB."""
        self.client.post(
            self.url,
            data=self.user_data,
        )
        self.user_data.pop("password1")
        self.user_data.pop("password2")
        users = CustomUser.objects.filter(**self.user_data)
        assert users.count() == 1
        assert check_password(self.password, users.first().password)

    def test_successful_signup_auths_user_and_redirects(self):
        """A successful signup should auth the user and redirect."""
        response = self.client.post(
            self.url,
            data=self.user_data,
        )
        assert response.wsgi_request.user.is_authenticated
        assert response.url == reverse("index")


class TestLogOut(TestCase):
    """Tests for the logout view."""

    def setUp(self) -> None:  # noqa: D102
        self.url = reverse(views.log_out)
        self.password = "mypassword"
        self.user = CustomUserFactory(password=make_password(self.password))

    def test_view_redirects_if_user_is_not_logged_in(self):
        """View should redirect if the user is authed."""
        response = self.client.get(self.url)
        assert response.url == reverse("index")

    def test_view_logs_user_out_and_redirects(self):
        """View should log the user out and redirect."""
        self.client.login(email=self.user.email, password=self.password)
        response = self.client.get(self.url)
        assert not response.wsgi_request.user.is_authenticated
        assert response.url == reverse("index")


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


class TestChangePassword(TestCase):
    """Tests for the change_password view."""

    def setUp(self) -> None:  # noqa: D102
        self.url = reverse(views.change_password)
        self.password = "mypassword"
        self.new_password = "D4B3stN3wP4$$word!"
        self.user = CustomUserFactory(password=make_password(self.password))

    def test_view_renders_correct_template(self):
        """View should render the correct template."""
        self.client.login(email=self.user.email, password=self.password)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "change_password.html")

    def test_view_redirects_if_user_is_not_logged_in(self):
        """View should redirect if the user is not authed."""
        response = self.client.get(self.url)
        assert response.url == reverse("log-in")

    def test_view_renders_correct_form(self):
        """View should render the correct form."""
        self.client.login(email=self.user.email, password=self.password)
        response = self.client.get(self.url)
        assert isinstance(response.context["form"], PasswordChangeForm)

    def test_unsuccessful_post_renders_errors(self):
        """Unsuccessful login should render the applicable errors in the template."""
        self.client.login(email=self.user.email, password=self.password)
        response = self.client.post(
            self.url,
            data={
                "password1": "elpassowordo",
                "password2": "something else",
            },
        )
        for error in response.context["form"].errors.values():
            for error_text in error:
                assert error_text in str(response.content)

    def test_successful_post_sets_password_and_redirects(self):
        """A successful password change should change the password and redirect."""
        self.client.login(email=self.user.email, password=self.password)
        response = self.client.post(
            self.url,
            data={
                "old_password": self.password,
                "new_password1": self.new_password,
                "new_password2": self.new_password,
            },
        )
        self.user.refresh_from_db()
        assert check_password(self.new_password, self.user.password)
        assert response.url == reverse("index")


class TestResetPassword(TestCase):
    """Tests for the password_reset view."""

    def setUp(self) -> None:  # noqa: D102
        self.url = reverse(views.password_reset)
        self.password = "mypassword"
        self.user = CustomUserFactory(password=make_password(self.password))

    def test_view_renders_correct_template(self):
        """View should render the correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "reset_password.html")

    def test_view_redirects_if_user_is_logged_in(self):
        """View should redirect if the user is authed."""
        self.client.login(email=self.user.email, password=self.password)
        response = self.client.get(self.url)
        assert response.url == reverse("change-password")

    def test_view_renders_correct_form(self):
        """View should render the correct form."""
        response = self.client.get(self.url)
        assert isinstance(response.context["form"], PasswordResetForm)

    def test_unsuccessful_post_renders_errors(self):
        """Unsuccessful login should render the applicable errors in the template."""
        response = self.client.post(
            self.url,
            data={
                "nood": "elpassowordo",
            },
        )
        for error in response.context["form"].errors.values():
            for error_text in error:
                assert error_text in str(response.content)

    @patch("users.views.PasswordResetForm.save")
    def test_successful_post_calls_form_save_with_overridden_args(self, save_mock):
        """A successful password change should call the form save method with args."""
        self.client.post(
            self.url,
            data={
                "email": self.user.email,
            },
        )

        save_mock.assert_called_once_with(
            subject_template_name="password_reset_subject.txt",
            email_template_name="password_reset_email.html",
            request=ANY,
        )


class TestCustomPasswordResetConfirmView(TestCase):
    """Tests for the custom password reset confirm view."""

    def setUp(self) -> None:  # noqa: D102
        self.request = RequestFactory().get("/")

        # adding session
        middleware = SessionMiddleware([])
        middleware.process_request(self.request)
        self.request.session[INTERNAL_RESET_SESSION_TOKEN] = "Fake token!"
        self.request.session.save()

        # adding messages
        messages = FallbackStorage(self.request)
        setattr(self.request, "_messages", messages)

    def test_class_subclasses_django_view(self):
        """Class should subclass PasswordResetConfirmView."""
        assert isinstance(CustomPasswordResetConfirmView(), PasswordResetConfirmView)

    def test_basic_config(self):
        """Test basic config."""
        assert CustomPasswordResetConfirmView.success_url == reverse_lazy("index")
        assert CustomPasswordResetConfirmView.template_name == "reset_password_confirm.html"
        assert CustomPasswordResetConfirmView.post_reset_login

    @patch("users.views.login")
    def test_form_valid_resets_password(self, mock_login):
        """Function should delete the session reset token."""
        view = CustomPasswordResetConfirmView()
        view.request = self.request
        view.form_valid(MagicMock())

        assert INTERNAL_RESET_SESSION_TOKEN not in self.request.session.keys()

    @patch("users.views.login")
    def test_form_valid_calls_form_save(self, mock_login):
        """Function should call the form save function."""
        view = CustomPasswordResetConfirmView()
        view.request = self.request
        form = MagicMock()
        view.form_valid(form)

        form.save.assert_called_once()

    @patch("users.views.login")
    def test_form_valid_logs_user_in(self, mock_login):
        """Function should log the user in."""
        view = CustomPasswordResetConfirmView()
        view.request = self.request
        form = MagicMock()
        form.save.return_value = "User"
        view.form_valid(form)

        mock_login.assert_called_once_with(self.request, "User", view.post_reset_login_backend)

    @patch("users.views.login")
    def test_form_valid_redirects_to_index(self, mock_login):
        """Function should redirect to the index page."""
        view = CustomPasswordResetConfirmView()
        view.request = self.request
        form = MagicMock()
        response = view.form_valid(form)

        assert response.url == reverse("index")
