from pytest_bdd import *
# from behave import *
# from base.features import test_login_feature
import pytest
from django.test import Client
from django.urls import resolve, reverse
from base.models import User
from django import urls
from django.contrib.auth import get_user_model
import pdb
from pytest_bdd import scenario, parsers, scenarios
from pathlib import Path


from .conftest import new_user





@scenario("test_login_feature.feature", 'Invalid Login Credentials')
def finish():
    pass

@pytest.mark.django_db
@given("I go to login page", target_fixture = "get_client")
def login_page_Access2(new_user):
    client = Client()
    login_url = reverse("login")
    return{"client":client, "url":login_url}


@when(parsers.cfparse('I enter the credentials "{email}" and "{pwd}" and login'), target_fixture = "login_response")
def login_page_Access(get_client, new_user, email, pwd, **kwargs):
    user = new_user.get(password = pwd + "1234", email = email + "1234")
    response = get_client["client"].post(get_client["url"], data = {"email":email, "password":pwd})
    return response


@then("The login page reloads")
def login_page_Access1(login_response):
    # print("get_user_data, email, pwd")
    pdb.set_trace()
    assert login_response.status_code == 200
    # return "return value of foobar"
    assert True

@then("I am not logged in")
def login_page_Access1(login_response):
    print("Anonymous user logged in")
    assert login_response.wsgi_request.user.is_anonymous
    pdb.set_trace()
    assert True



