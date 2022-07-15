import pytest
from base.models import User
from django import urls
from django.contrib.auth import get_user_model
import pdb

 

@pytest.mark.parametrize(
    'param', 
    [
        ("chat:home"),
        ("login"),
        ("signup"),
    ]
)
@pytest.mark.django_db
def test_render_views(client, param):
    temp_url = urls.reverse(param)
    resp = client.get(temp_url)
    assert resp.status_code == 200

@pytest.mark.django_db
def test_signup(client, get_user_data):
    pdb.set_trace()
    user_model = get_user_model()
    assert user_model.objects.count() == 0
    signup_url = urls.reverse("signup")
    resp = client.post(signup_url, get_user_data)
    assert user_model.objects.count() == 1
    assert resp.status_code == 302


def test_login(client, get_user_data, get_user):
    user = get_user
    login_url = urls.reverse("login")
    print(get_user)
    pdb.set_trace()
    resp = client.post(login_url, data = get_user_data)
    assert resp.status_code == 302
    # assert resp.url =
    assert True



