# -*- coding: utf-8 -*-
"""Users forms."""

# 3rd-party
from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Custom user creation form."""

    class Meta:  # noqa: D106
        model = CustomUser
        fields = ("first_name", "last_name")
