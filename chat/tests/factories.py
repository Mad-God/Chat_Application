import factory
from faker import Faker

fake = Faker()
import pytest
import pdb
from datetime import datetime


from Chat_Application.wsgi import *


from base.models import User
from chat.models import ChatGroup


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    def create_user(user_object):
        return User.objects.create_user(**user_object)

    def get_new_user():
        user_object = {}
        user_object["username"] = fake.name()
        user_object["name"] = fake.name()
        user_object["mobile"] = "1234512345"
        user_object["email"] = fake.email()
        user_object["password"] = fake.password()
        return user_object


class ChatFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ChatGroup

    def get_chat_group():
        chat_object = {}
        chat_object["name"] = fake.name()[:8]
        return chat_object

    def create_chat_group(chat_object):
        return ChatGroup.objects.create(name=chat_object["name"])
