# -*- coding: utf-8 -*-
"""Urls for users app."""
# 3rd-party
from django.conf import settings
from django.urls import path

# Local
from . import views

urlpatterns = [
    path("sign-up", views.sign_up, name="sign-up"),
    path("sign-up/email", views.sign_up_email, name="sign-up-email"),
    path("log-in", views.log_in, name="log-in"),
    path("log-out", views.log_out, name="log-out"),
    path("change-password", views.change_password, name="change-password"),
    path("reset-password", views.password_reset, name="reset-password"),
    path(
        "reset-password-confirm/<uidb64>/<token>",
        views.CustomPasswordResetConfirmView.as_view(),
        name="reset-password-confirm",
    ),
]

if settings.DEBUG:
    # 3rd-party
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
