# -*- coding: utf-8 -*-
"""Tests for the users app admin."""

# 3rd-party
from django.test import TestCase

# Project
from users.admin import UserAdmin


class TestUserAdmin(TestCase):
    """Tests for the custom user admin."""

    def setUp(self) -> None:  # noqa: D102
        self.admin = UserAdmin

    def test_username_is_not_shown_in_admin(self):
        """The username field should not be shown in the admin."""
        for i in self.admin.fieldsets:
            for j in i:
                if isinstance(j, dict):
                    assert "username" not in j["fields"]

        for i in self.admin.add_fieldsets:
            for j in i:
                if isinstance(j, dict):
                    assert "username" not in j["fields"]

        assert "username" not in self.admin.list_display
        assert "username" not in self.admin.search_fields
