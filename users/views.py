# -*- coding: utf-8 -*-
"""
Views for users app.

We've overridden a bunch of stuff here because you'll inevitably want to change it.
"""

# 3rd-party
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import INTERNAL_RESET_SESSION_TOKEN
from django.contrib.auth.views import PasswordResetConfirmView
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.urls import reverse_lazy

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
        messages.info(request, "Logged out successfully.")
    return redirect(reverse("index"))


def log_in(request):
    """Log the user in."""
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect(reverse("index"))

    form = CustomUserLoginForm()
    if request.method == "POST":
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.get(email=form.cleaned_data["email"])
            login(request, user)
            messages.info(
                request,
                f"Logged in successfully. Welcome {user.first_name} {user.last_name}",
            )
            return redirect(reverse("index"))
    return render(request, "log_in.html", {"form": form})


def change_password(request):
    """Change the users password."""
    if not request.user.is_authenticated:
        return redirect(reverse("log-in"))

    form = PasswordChangeForm(user=request.user)
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            new_password = make_password(form.cleaned_data["new_password1"])
            request.user.password = new_password
            request.user.save()
            messages.info(request, "Password changed successfully.")
            return redirect(reverse("index"))
    return render(request, "change_password.html", {"form": form})


def password_reset(request):
    """Reset the users password."""
    if request.user.is_authenticated:
        return redirect(reverse("change-password"))

    form = PasswordResetForm()
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                subject_template_name="password_reset_subject.txt",
                email_template_name="password_reset_email.html",
                request=request,
            )
            messages.info(
                request,
                "If a matching email has been found, it will receive a password reset "
                "email. Please check your inbox.",
            )
            return redirect(reverse("index"))
    return render(request, "reset_password.html", {"form": form})


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """Override defaults."""

    success_url = reverse_lazy("index")
    template_name = "reset_password_confirm.html"

    def form_valid(self, form):
        """Send the confirmation of password rest as a message instead of a whole view."""
        user = form.save()
        del self.request.session[INTERNAL_RESET_SESSION_TOKEN]
        if self.post_reset_login:
            login(self.request, user, self.post_reset_login_backend)
        messages.info(self.request, "Your password has been reset!")
        return super().form_valid(form)
