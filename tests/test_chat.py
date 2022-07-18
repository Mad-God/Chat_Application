import pytest
from base.models import User
from django import urls
from django.contrib.auth import get_user_model
import pdb


from chat.models import ChatGroup, Member

"""
    path("", views.HomeView.as_view(), name='home'),                                                    Done
    path("chat/<name>", views.Lobby.as_view(), name='chat'),                                            

    # membership urls
    path("apply/<name>", views.ApplyForMemberShip.as_view(), name='apply-membership'),
    path("accept/<name>/<int:user>", views.AcceptMemberShip.as_view(), name='accept-membership'),
    path("revoke/<name>/<int:user>", views.RevokeMemberShip.as_view(), name='revoke-membership'),
    path("deny/<name>/<int:user>", views.DenyMemberShip.as_view(), name='deny-membership'),
    path("invite/<int:group_id>", views.InviteMemberShip.as_view(), name='invite-membership'),

    # direct messages
    path("direct/<int:user_id>", views.DirectLobby.as_view(), name='direct'),
"""

 


# @pytest.mark.parametrize()
@pytest.mark.django_db
def test_index(client, get_chat_group):
    index_url = urls.reverse("chat:home")
    resp = client.get(index_url)
    assert resp.status_code == 200
    assert True




def test_group_create(client, get_chat_group, get_user_data):
    assert True
    index_url = urls.reverse("chat:home")
    client.force_login(user = User.objects.get(username="username"))
    resp = client.post(index_url, get_chat_group)
    assert resp.status_code == 302
    assert ChatGroup.objects.count() == 1




def test_group_apply(client, create_chat_group, get_user_data):
    pdb.set_trace()
    # index_url = urls.reverse("chat:apply-membership", kwargs={"name":get_chat_group["name"]})
    index_url = urls.reverse("chat:apply-membership", kwargs={"name":"ChatGroup"})
    # index_url = urls.reverse("chat:apply-membership", name="ChatGroup")
    client.force_login(user = User.objects.get(username="username"))
    resp = client.get(index_url)
    assert ChatGroup.objects.count() == 1
    assert resp.status_code == 302
    assert Member.objects.count() == 1


   
def test_group_apply(client, get_chat_data, create_chat_group, get_user_data):
    assert ChatGroup.objects.count() == 0
    index_url = urls.reverse("chat:apply-membership", kwargs={"name":get_chat_data["name"]})
    client.force_login(user = User.objects.get(username=get_user_data["username"]))
    resp = client.get(index_url)
    assert ChatGroup.objects.count() == 1
    assert resp.status_code == 302
    assert Member.objects.count() == 1


   
def test_group_accept(client, create_chat_group, get_chat_data,  get_user_data):
    pdb.set_trace()
    assert ChatGroup.objects.count() == 0
    index_url = urls.reverse("chat:apply-membership", kwargs={"name":get_chat_data["name"]})
    client.force_login(user = User.objects.get(username=get_user_data["username"]))
    resp = client.get(index_url)
    assert ChatGroup.objects.count() == 1
    assert resp.status_code == 302
    assert Member.objects.count() == 1

   


