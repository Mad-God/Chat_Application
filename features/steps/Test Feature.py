from behave import *
from selenium import webdriver

@given(u'Start to type your Given step here')
def test_start(context):
    # launch the browser
    context.driver = webdriver.Chrome(executable_path=r"/home/dell/Desktop/Chat_Application-master/chromedriver_linux64/chromedriver")



@when(u'I test the BDD test')
def action_occurred(context):
    # open the project
        context.driver.get("http://127.0.0.1:8000/")
        status = context.driver.find_element_by_xpath('//header/div[1]/a[1]/*[1]').is_displayed()  
        assert status is True


@then(u'Start to type your Then step here')
def action_handled(context):
    pass
    # raise NotImplementedError(u'STEP: Then Start to type your Then step here')


@then(u'Close browser')
def action_handled2(context):
    context.driver.close()
    # raise NotImplementedError(u'STEP: Then Close browser')


@given(u'Launch the Browser')
def step_impl(context):
    context.driver = webdriver.Chrome(executable_path=r"/home/dell/Desktop/Chat_Application-master/chromedriver_linux64/chromedriver")


@when(u'GO to login page')
def step_impl(context):
    context.driver.get("http://127.0.0.1:8000/login/")
    status = context.driver.find_element_by_xpath("//input[@id='id_email']").is_displayed()  
    assert status is True


@then(u'Enter the credetials with "{email}" and "{pwd}"')
def step_impl(context, email, pwd):
    context.driver.find_element_by_id("id_email").send_keys(email)
    context.driver.find_element_by_id("id_password").send_keys(pwd)


@then(u'Login the User in')
def step_impl(context):
    context.driver.find_element_by_xpath("//button[contains(text(),'Log-In')]").click()


@then(u'Close the Browser')
def step_impl(context):
    assert context.driver.find_element_by_xpath("//header/div[1]/nav[1]/a[4]").is_displayed()
