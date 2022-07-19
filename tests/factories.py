import factory
from faker import Faker
fake = Faker()
import pytest
from Chat_Application.wsgi import *


from base.models import User

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = fake.name()
    name = fake.name()
    mobile="1234512345"
    email = fake.email()
    password =fake.password()


