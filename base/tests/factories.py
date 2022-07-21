import factory
from faker import Faker

fake = Faker()
import pytest
import pdb
from datetime import datetime


from Chat_Application.wsgi import *


from base.models import User


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
