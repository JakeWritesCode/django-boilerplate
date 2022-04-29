# -*- coding: utf-8 -*-
"""Urls for users app."""
# 3rd-party
from django.urls import path

# Local
from . import views

urlpatterns = [
    path("sign-up", views.sign_up, name="sign-up"),
    path("log-in", views.log_in, name="log-in"),
    path("log-out", views.log_out, name="log-out"),
]
