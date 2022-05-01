# -*- coding: utf-8 -*-
"""Factories for user models."""

# 3rd-party
from django.contrib.auth.hashers import make_password
from factory.django import DjangoModelFactory
from faker import Faker

# Project
from users.models import CustomUser

fake = Faker()


class CustomUserFactory(DjangoModelFactory):
    """CustomUser factory."""

    email = fake.email()
    first_name = fake.first_name()
    last_name = fake.last_name()
    password = make_password(fake.password())

    class Meta:  # noqa: D106
        model = CustomUser
