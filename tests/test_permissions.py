# creating and testing permissions and test groups in django tests.
from tkinter import N
from django.contrib.auth.models import Permission, Group
from django.test import TestCase
from django.test import Client
from django.urls import reverse
from faker import Faker
import pdb

from tests.factories import UserFactory

fake = Faker()




from base.models import User
from chat.models import ChatGroup, Member



class ExampleGroupPermissionsTests(TestCase):

    def setUp(self):
        self.client = Client()

        object_data = {}
        object_data["username"] = fake.name()
        object_data["name"] = fake.name()
        object_data["mobile"] = "1234512345"
        object_data["email"] = fake.email()
        object_data["password"] = fake.password()
        self.admin_password = object_data["password"]
        self.admin = User.objects.create(**object_data)

        object_data = {}
        object_data["username"] = fake.name()
        object_data["name"] = fake.name()
        object_data["mobile"] = "1234512345"
        object_data["email"] = fake.email()
        object_data["password"] = fake.password()
        self.user_password = object_data["password"]
        self.user = User.objects.create(**object_data)

        self.chatgroup = ChatGroup.objects.create(name=fake.name())

    def tearDown(self):
        self.user.delete()
        self.admin.delete()
        self.chatgroup.delete()

    def test_user_can_access(self):
        """
        user NOT in group should not have access
        """
        self.client.force_login(user = self.user)
        Member.objects.create(group=self.chatgroup, user=self.user, accepted = True)
        index_url = reverse("chat:chat",kwargs={"name":self.chatgroup.slug})
        response = self.client.get(index_url)
        self.assertEqual(response.status_code, 200, u'user in group should have access')
        

    def test_user_cannot_access(self):
        """
        user NOT in group should not have access
        """
        self.client.force_login(user = self.user)
        Member.objects.create(group=self.chatgroup, user=self.user, accepted = False)
        index_url = reverse("chat:chat",kwargs={"name":self.chatgroup.slug})
        response = self.client.get(index_url)
        self.assertEqual(response.status_code, 403, u'user in group should have access')
    

    # def test_user_can_access(self):
    #     """user in group should have access
    #     """
    #     self.user.groups.add(self.group)
    #     self.user.save()
    #     self.c.login(username='test', password='test')
    #     response = self.c.get("/my_view")
    #     self.assertEqual(response.status_code, 200, u'user in group should have access')




