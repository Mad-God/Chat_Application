from django.test import TestCase, Client
from django.urls import reverse, resolve
import pdb

from .factories import UserFactory
from base.views import *
from base.models import User


class TestViews(TestCase):
    def setUp(self):
        self.user = UserFactory.get_new_user()
        self.user["user"] = UserFactory.create_user(self.user)
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")
        self.signup_url = reverse("signup")
        self.client = Client()

    def test_login(self):
        response = self.client.post(
            self.login_url,
            data={"email": self.user["email"], "password": self.user["password"]},
        )
        assert response.status_code == 302

    def test_login_fail_bad_credentials(self):
        response = self.client.post(self.login_url, data={"email": self.user["email"]})
        assert response.status_code == 200

    def test_signup(self):
        user = UserFactory.get_new_user()
        user["password1"] = user["password"]
        user["password2"] = user["password"]
        user.pop("password")
        response = self.client.post(self.signup_url, data=user)
        assert response.status_code == 302

    def test_signup_fail_bad_request(self):
        user = UserFactory.get_new_user()
        user["password1"] = user["password"]
        user["password2"] = user["password"] + "1234"  # mismatching passwords
        user.pop("password")
        response = self.client.post(self.signup_url, data=user)
        assert response.status_code == 400

    def test_logout(self):
        self.client.login(user=self.user["user"])
        response = self.client.post(self.logout_url)
        assert response.status_code == 302

    def tearDown(self) -> None:
        self.user["user"].delete()
        del self.user
        del self.login_url
        del self.logout_url
        del self.signup_url
        return super().tearDown()
