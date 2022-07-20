import pytest
from base.models import User
from django import urls
from django.contrib.auth import get_user_model
import pdb


@pytest.mark.parametrize(
    "param",
    [
        ("chat:home"),
        ("login"),
        ("signup"),
    ],
)
@pytest.mark.django_db
def test_render_views(client, param):
    temp_url = urls.reverse(param)
    resp = client.get(temp_url)
    assert resp.status_code == 200


@pytest.mark.django_db
def test_signup(client, get_user_data):
    user_model = get_user_model()
    assert user_model.objects.count() == 0
    signup_url = urls.reverse("signup")
    get_user_data.pop("password")
    resp = client.post(signup_url, data = get_user_data)
    assert user_model.objects.count() == 1
    assert resp.status_code == 302


def test_login(client, get_user_data, get_user):
    login_url = urls.reverse("login")
    # get_user_data.pop("password1")
    # get_user_data.pop("password2")
    resp = client.post(login_url, data=get_user_data)
    assert resp.status_code == 302
    assert True


def test_logout(client, get_authenticated_user, get_user_data):
    user = get_user_data
    logout_url = urls.reverse("logout")
    resp = client.get(logout_url)
    assert resp.status_code == 302
    assert True
