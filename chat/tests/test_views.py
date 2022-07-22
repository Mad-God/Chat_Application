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

    def test_home_get(self):
        response = self.client.get(
            self.home_url,
        )
        assert response.status_code == 200
    
    def test_home_post(self):
        ChatGroup.objects.all().delete()
        self.client.force_login(self.admin["user"])
        self.chat.pop("chat")
        assert ChatGroup.objects.count() == 0
        response = self.client.post(
            self.home_url,
            data = self.chat
        )
        assert ChatGroup.objects.count() == 1
        assert ChatGroup.objects.first().admin.last() == self.admin["user"]
        assert response.status_code == 302

    def test_apply_membership(self):
        self.client.force_login(self.user["user"])
        response = self.client.get(self.apply_url)
        assert Member.objects.count() == 1
        assert Member.objects.last().user == self.user["user"]
        assert Member.objects.last().group == self.chat["chat"]
        assert response.status_code == 302

    def test_accept_membership_fail_no_member(self):
        self.client.force_login(self.admin["user"])
        Member.objects.create(
            user=self.user["user"], group=self.chat["chat"], accepted=False
        )
        response = self.client.get(self.accept_url)
        assert Member.objects.count() == 1
        assert Member.objects.last().user == self.user["user"]
        assert Member.objects.last().group == self.chat["chat"]
        assert response.status_code == 302

    def test_accept_membership_fail_not_admin(self):
        self.client.force_login(self.user["user"])
        Member.objects.create(
            user=self.user["user"], group=self.chat["chat"], accepted=False
        )
        response = self.client.get(self.accept_url)
        assert Member.objects.filter(accepted=True).count() == 0
        assert Member.objects.last().group == self.chat["chat"]
        assert response.status_code == 403

    def test_deny_membership(self):
        self.client.force_login(self.admin["user"])
        Member.objects.create(
            user=self.user["user"], group=self.chat["chat"], accepted=False
        )
        assert Member.objects.count() == 1
        response = self.client.get(self.deny_url)
        assert Member.objects.count() == 0
        assert response.status_code == 302

    def test_deny_membership_not_admin(self):
        Member.objects.create(
            user=self.user["user"], group=self.chat["chat"], accepted=False
        )
        assert Member.objects.count() == 1
        self.client.force_login(self.user["user"])
        response = self.client.get(self.deny_url)
        assert Member.objects.count() == 1
        assert response.status_code == 403

    def test_revoke_membership(self):
        self.client.force_login(self.admin["user"])
        Member.objects.create(
            user=self.user["user"], group=self.chat["chat"], accepted=True
        )
        response = self.client.get(self.revoke_url)
        assert Member.objects.count() == 0
        assert response.status_code == 302

    def test_revoke_membership_fail_not_admin(self):
        self.client.force_login(self.user["user"])
        Member.objects.create(
            user=self.user["user"], group=self.chat["chat"], accepted=True
        )
        response = self.client.get(self.revoke_url)
        assert Member.objects.count() == 1
        assert response.status_code == 403

    def test_invite_membership(self):
        self.client.force_login(self.user["user"])
        assert Member.objects.count() == 0
        response = self.client.get(self.invite_url)
        assert Member.objects.count() == 1
        assert response.status_code == 302

