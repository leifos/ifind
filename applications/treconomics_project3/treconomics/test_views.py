from django.core.urlresolvers import reverse

__author__ = 'mickeypash'
from django.test import TestCase


class LandingViewTests(TestCase):

    def test_home_view_status_code(self):
        """
        Testing the response status codes
        Status expected - 200 OK
        """
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_login_view_status_code(self):
        """
        Testing the response status codes
        Status expected - 200 OK
        """
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_logout_view_status_code(self):
        """
        Testing the response status codes
        Status expected - 200 OK
        """
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 200)

    def test_start_exp_view_status_code(self):
        """
        Testing the response status codes
        Status expected - 200 OK
        """
        response = self.client.get(reverse("start-experiment"))
        self.assertEqual(response.status_code, 200)

    def test_start_exp_view_status_code(self):
        """
        Testing the response status codes
        Status expected - 200 OK
        """
        response = self.client.get(reverse("pre-experiment"))
        self.assertEqual(response.status_code, 200)