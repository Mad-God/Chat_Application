Feature: Signup
    A site where you can publish your articles.

    Scenario: Valid Signup details Credentials
        Given I go to signup page
        When I enter the details <username>, <email>, <name>, <mobile> and <password> and hit signup
        Then I get redirected to the Login Page
        And My user account has been created with <email>
        Examples:
        | email            | password    | name  | username | mobile     | 
        | admin@admin.com  |  admin      | admin | admin    | 1234512345 |
        | user1@user.com   | strongpswd1 | admin | admin    | 1234512345 | 