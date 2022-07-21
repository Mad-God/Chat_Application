from django.test import SimpleTestCase
from django.urls import resolve, reverse
import pdb


from chat.views import *

class TestChatUrls(SimpleTestCase):

    def test_invite_url(self):
        index_url = reverse("chat:invite-membership", kwargs={"group_id":1})
        self.assertEqual(resolve(index_url).func.view_class, InviteMemberShip)

    def test_revoke_url(self):
        index_url = reverse("chat:revoke-membership", kwargs={"name":"slug", "user":2})
        self.assertEqual(resolve(index_url).func.view_class, RevokeMemberShip)

    def test_deny_url(self):
        index_url = reverse("chat:deny-membership", kwargs={"name":"slug", "user":2})
        self.assertEqual(resolve(index_url).func.view_class, DenyMemberShip)
    
    def test_accept_url(self):
        index_url = reverse("chat:accept-membership", kwargs={"name":"slug", "user":2})
        self.assertEqual(resolve(index_url).func.view_class, AcceptMemberShip)
    
    def test_lobby_url(self):
        index_url = reverse("chat:chat", kwargs={"name":"some-slug"})
        self.assertEqual(resolve(index_url).func.view_class, Lobby)
    
    def test_home_url(self):
        index_url = reverse("chat:home")
        self.assertEqual(resolve(index_url).func.view_class, HomeView)


