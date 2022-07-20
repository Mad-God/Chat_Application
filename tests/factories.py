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

    def create_new_user():
        object_data = {}
        object_data["username"] = fake.name()
        object_data["name"] = fake.name()
        object_data["mobile"] = "1234512345"
        object_data["email"] = fake.email()
        object_data["password"] = fake.password()
        return User.objects.create(**object_data)
