# -*- coding: utf-8 -*-
"""Users forms."""

# 3rd-party
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError

# Project
from users.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Custom user creation form."""

    class Meta:  # noqa: D106
        model = CustomUser
        fields = ("email", "first_name", "last_name")


class CustomUserLoginForm(forms.Form):
    """Log the user in."""

    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean_email(self):
        """Check that the email exists."""
        email = self.cleaned_data["email"]
        try:
            CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise ValidationError("A user with this email does not exist.")
        return email

    def clean_password(self):
        """Check the password."""
        password = self.data["password"]
        try:
            user = CustomUser.objects.get(email=self.cleaned_data["email"])
        except KeyError:
            return password
        if not check_password(password, user.password):
            raise ValidationError("The entered password is incorrect.")
        return password
