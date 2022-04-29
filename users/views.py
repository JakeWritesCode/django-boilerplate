# -*- coding: utf-8 -*-
"""
Views for users app.

We've overridden a bunch of stuff here because you'll inevitably want to change it.
"""

# 3rd-party
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

# Project
from users.forms import CustomUserCreationForm
from users.forms import CustomUserLoginForm
from users.models import CustomUser


def sign_up(request):
    """Basic sign up view."""
    if request.user.is_authenticated:
        return redirect(reverse("index"))

    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            login(request, user)
            return redirect(reverse("index"))

    return render(request, "sign_up.html", {"form": form})


def log_out(request):
    """Log the user out."""
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse("index"))


def log_in(request):
    """Log the user in."""
    if request.user.is_authenticated:
        return redirect(reverse("index"))

    form = CustomUserLoginForm()
    if request.method == "POST":
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.get(email=form.cleaned_data["email"])
            login(request, user)
            return redirect(reverse("index"))
    return render(request, "log_in.html", {"form": form})
