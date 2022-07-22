from venv import create
from django.test import TestCase, Client
from django.urls import reverse, resolve
import pdb

from .factories import UserFactory, ChatFactory
from chat.views import *
from chat.models import *


class TestViews(TestCase):
    def setUp(self):
        self.user = UserFactory.get_new_user()
        self.user["user"] = UserFactory.create_user(self.user)

        self.admin = UserFactory.get_new_user()
        self.admin["user"] = UserFactory.create_user(self.admin)

        self.chat = ChatFactory.get_chat_group()
        self.chat["chat"] = ChatFactory.create_chat_group(self.chat)
        self.chat["chat"].admin.add(self.admin["user"])

        self.login_url = reverse("login")
        self.logout_url = reverse("logout")
        self.signup_url = reverse("signup")
        self.home_url = reverse("chat:home")
        self.chat_url = reverse(
            "chat:chat",
            kwargs={
                "name": self.chat["chat"].slug,
            },
        )
        self.accept_url = reverse(
            "chat:accept-membership",
            kwargs={"name": self.chat["chat"].slug, "user": self.user["user"].id},
        )
        self.revoke_url = reverse(
            "chat:revoke-membership",
            kwargs={"name": self.chat["chat"].slug, "user": self.user["user"].id},
        )
        self.deny_url = reverse(
            "chat:deny-membership",
            kwargs={"name": self.chat["chat"].slug, "user": self.user["user"].id},
        )
        self.apply_url = reverse(
            "chat:apply-membership", kwargs={"name": self.chat["chat"].slug}
        )
        self.invite_url = reverse(
            "chat:invite-membership", kwargs={"group_id": self.chat["chat"].id}
        )

        self.client = Client()
