import pytest
from base.models import User
from django import urls
from django.contrib.auth import get_user_model
import pdb

"""
    path("", views.HomeView.as_view(), name='home'),
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

 
@pytest.mark.django_db
def test_index(client):
    index_url = urls.reverse("chat:home")
    resp = client.get(index_url)
    assert resp.status_code == 200
    assert True




@pytest.mark.django_db
def test_index(client):
    index_url = urls.reverse("chat:home")
    resp = client.get(index_url)
    assert resp.status_code == 200
    assert True

# @pytest.mark.parametrize()
@pytest.mark.django_db
def test_index(client, get_chat_group):
    index_url = urls.reverse("chat:home")
    resp = client.get(index_url)
    assert resp.status_code == 200
    assert True




def test_group_create(client, get_chat_group):
    assert True
    index_url = urls.reverse("chat:home")
    resp = client.post(index_url, get_chat_group)
    assert resp.status_code == 200
    assert True


 