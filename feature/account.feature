Feature: Account Management

  Scenario: Sign up for a new account
    Given the user is on the sign-up page
    When they enter their email, password, and confirm password
    And they click the sign-up button
    Then they should be redirected to the account page
    And they should see a success message confirming their account has been created

  Scenario: Log in to an existing account
    Given the user is on the login page
    When they enter their email and password
    And they click the login button
    Then they should be redirected to the account page
    And they should see a welcome message with their name

  Scenario: View account details
    Given the user is on the account page
    When they click the "view details" button
    Then they should see their account information, including their name, email, and password

  Scenario: Update account information
    Given the user is on the account page
    When they click the "edit" button
    And they update their name and/or email
    And they click the "save changes" button
    Then they should see a success message confirming their changes have been saved
    And their name and/or email should be updated on the account page

  Scenario: Change account password
    Given the user is on the account page
    When they click the "change password" button
    And they enter their current password, new password, and confirm new password
    And they click the "save changes" button
    Then they should see a success message confirming their password has been updated
    And they should be redirected to the login page to log in with their new password

  Scenario: Delete account
    Given the user is on the account page
    When they click the "delete account" button
    And they confirm the deletion
    Then they should see a success message confirming their account has been deleted
    And they should be redirected to the login page to create a new account
