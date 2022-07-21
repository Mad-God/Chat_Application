from django.test import SimpleTestCase
from django.urls import resolve, reverse
import pdb


from base.views import *


class TestBaseUrls(SimpleTestCase):
    def test_login_url(self):
        index_url = reverse("login")
        self.assertEqual(resolve(index_url).func.view_class, LoginPageView)

    def test_logout_url(self):
        index_url = reverse("logout")
        self.assertEqual(resolve(index_url).func.view_class, Logout)

    def test_signup_url(self):
        index_url = reverse("signup", kwargs={})
        self.assertEqual(resolve(index_url).func.view_class, SignupView)
