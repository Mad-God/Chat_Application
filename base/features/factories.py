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

    def create_new_user(**kwargs):
        object_data = {}
        object_data["username"] = kwargs.get("username", fake.name())
        object_data["name"] = kwargs.get("name", fake.name())
        object_data["mobile"] = "1234512345"
        object_data["email"] = kwargs.get("email", fake.email())
        object_data["password"] = kwargs.get("password", fake.password())
        return User.objects.create_user(**object_data)
