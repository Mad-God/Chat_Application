Feature: Login

    Scenario: Valid Login Credentials
        Given I go to login page
        When I enter the credentials <email> and <password> and login
        Then I get redirected to the Home Page
        And I am logged in as <email>
        Examples:
        | email            | password    |
        | admin@admin.com  |  admin      |
        | user1@user.com   | strongpswd1 |




    Scenario: Invalid Login Credentials
        Given I go to login page
        When I enter the credentials "admin@admin.com" and "admin123" and login
        Then The login page reloads
        And I am not logged in




