from tokenize import group
from conftest import create_chat_group
import pytest
from base.models import User
from django import urls
from django.contrib.auth import get_user_model
import pdb



from chat.models import ChatGroup, Member
 


@pytest.mark.django_db
def test_index(client, get_chat_group):
    index_url = urls.reverse("chat:home")
    resp = client.get(index_url)
    assert resp.status_code == 200
    assert True

 

# def test_group_create(client, get_chat_group, new_user):
#     index_url = urls.reverse("chat:home")
#     client.force_login(user = User.objects.get(username=new_user.username))
#     resp = client.post(index_url, get_chat_group)
#     assert resp.status_code == 302
#     assert str(resp.url).lower() == f"/chat/{get_chat_group['slug']}".lower()
#     assert ChatGroup.objects.count() == 1

 

# def test_group_apply(client, create_chat_group, new_user):
#     index_url = urls.reverse("chat:apply-membership", kwargs={"name":"ChatGroup"})
#     client.force_login(user = User.objects.get(username=new_user.username))
#     resp = client.get(index_url)
#     assert ChatGroup.objects.count() == 1
#     assert resp.status_code == 302
#     assert resp.url == f"/"
#     assert Member.objects.count() == 1


@pytest.mark.db
def test_group_accept(client, create_chat_group, new_user):
    chat_group = create_chat_group
    user = new_user.get()
    admin = new_user.get()
    index_url = urls.reverse("chat:accept-membership", kwargs={"name":chat_group.name, 'user':user.id})
    Member.objects.create(group = chat_group, user = user, accepted = False)
    chat_group.admin.add(admin.id)
    assert chat_group.admin.count() == 1
    client.force_login(user = User.objects.get(username=admin.username))
    resp = client.get(index_url)
    assert ChatGroup.objects.count() == 1
    assert resp.status_code == 302
    assert resp.url.lower() == f"/chat/{chat_group.slug}".lower()
    assert Member.objects.count() == 1 

        

# def test_group_deny(client, create_chat_group, new_user, get_user):
#     chat_group = create_chat_group
#     index_url = urls.reverse("chat:deny-membership", kwargs={"name":chat_group.name, 'user':new_user.id})
#     Member.objects.create(group = chat_group, user = new_user, accepted = False)
#     chat_group.admin.add(get_user.id)
#     client.force_login(user = User.objects.get(username=get_user.username))
#     resp = client.get(index_url)
#     assert resp.status_code == 302
#     assert resp.url.lower() == f"/chat/{chat_group.slug}".lower()
#     assert Member.objects.count() == 0



# def test_group_revoke(client, create_chat_group, new_user, get_user):
#     chat_group = create_chat_group
#     index_url = urls.reverse("chat:revoke-membership", kwargs={"name":chat_group.name, 'user':new_user.id})
#     Member.objects.create(group = chat_group, user = new_user, accepted = True)
#     chat_group.admin.add(get_user.id)
#     client.force_login(user = User.objects.get(username=get_user.username))
#     resp = client.get(index_url)
#     assert resp.status_code == 302
#     assert resp.url.lower() == f"/chat/{chat_group.slug}".lower()
#     assert Member.objects.count() == 0



# def test_group_invite(client, create_chat_group, new_user, get_user):
#     chat_group = create_chat_group
#     index_url = urls.reverse("chat:invite-membership", kwargs={"group_id":chat_group.id,})
#     assert Member.objects.count() == 0
#     client.force_login(user = User.objects.get(username=new_user.username))
#     resp = client.get(index_url)
#     assert resp.status_code == 302
#     assert Member.objects.count() == 1
#     assert str(resp.url).lower() == f"/chat/{chat_group.slug}".lower()

