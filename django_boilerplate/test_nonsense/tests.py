"""Nonsense tests to keep coverage happy."""
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.test import TestCase, override_settings

from django_boilerplate import urls


class TestURLs(TestCase):

    @override_settings(DEBUG=True)
    def test_adds_static_urls_when_debugging(self):
        self.assertIn(str(staticfiles_urlpatterns()[0]), str(urls.urlpatterns))
