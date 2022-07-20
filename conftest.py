from click import password_option
import pytest
from pytest_factoryboy import register
from django.contrib import auth
import sys
import os
import pdb


from base.models import User
from chat.models import ChatGroup
from tests.factories import UserFactory

register(
    UserFactory
)  # even tho the name is UserFactory, user_factory is the name that will be used.


@pytest.fixture
def new_user(request, db, user_factory, num_users=5):
    class ThingFactory(object):
        def get():
            thing = user_factory.create_new_user()
            return thing

    return ThingFactory


@pytest.fixture
def get_user_data():
    return {
        "email": "user_email@user.com",
        "username": "username",
        "name": "name",
        "mobile": "1234512345",
        "password": "strongpswd1",
        "password1": "strongpswd1",
        "password2": "strongpswd1",
    }


@pytest.fixture
@pytest.mark.django_db
def get_user(db, get_user_data):
    get_user_data.pop("password1")
    get_user_data.pop("password2")
    user = User.objects.create_user(**get_user_data)
    return user


@pytest.fixture
@pytest.mark.django_db
def get_authenticated_user(db, get_user):
    auth.authenticate(get_user_data)
    return get_user_data


@pytest.fixture
@pytest.mark.django_db
def get_chat_group(db, get_user_data):
    return {"name": "ChatGroup", "slug": "ChatGroup"}


@pytest.fixture
@pytest.mark.django_db
def create_chat_group(db, get_chat_group):
    return ChatGroup.objects.create(**get_chat_group)
