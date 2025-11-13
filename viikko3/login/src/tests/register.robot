*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application Create User And Go To Register Page

*** Test Cases ***

Register With Valid Username And Password
    Set Username  pekka
    Set Password  pekka123456
    Set Password Confirmation  pekka123456
    Click Button  Register
    Register Should Succeed

Register With Too Short Username And Valid Password
    Set Username  pe
    Set Password  pekka123456
    Set Password Confirmation  pekka123456
    Click Button  Register
    Register Should Fail With Message  Username must be at least 3 characters long

Register With Valid Username And Too Short Password
    Set Username  pekka
    Set Password  pekka12
    Set Password Confirmation  pekka12
    Click Button  Register
    Register Should Fail With Message  Password must be at least 8 characters long and not consist of only letters

Register With Valid Username And Invalid Password
# salasana ei sisällä halutunlaisia merkkejä
    Set Username  pekka
    Set Password  pekkapekka
    Set Password Confirmation  pekkapekka
    Click Button  Register
    Register Should Fail With Message  Password must be at least 8 characters long and not consist of only letters

Register With Nonmatching Password And Password Confirmation
    Set Username  pekka
    Set Password  pekka123
    Set Password Confirmation  pekka1234
    Click Button  Register
    Register Should Fail With Message  Passwords do not match

Register With Username That Is Already In Use
    Set Username  pekka
    Set Password  pekka123
    Set Password Confirmation  pekka123
    Click Button  Register
    Register Should Succeed

    Go To Register Page
    Set Username  pekka
    Set Password  pekka123
    Set Password Confirmation  pekka123
    Click Button  Register
    Register Should Fail With Message  User with username pekka already exists

*** Keywords ***
Reset Application Create User And Go To Register Page
    Reset Application
    Create User  kalle  kalle123
    Go To Register Page

Set Username
    [Arguments]  ${username}
    Input Text  username  ${username}

Set Password
    [Arguments]  ${password}
    Input Password  password  ${password}

Set Password Confirmation
    [Arguments]  ${password_confirmation}
    Input Password  password_confirmation  ${password_confirmation}

Register Should Succeed
    Welcome Page Should Be Open

Register Should Fail With Message
    [Arguments]  ${message}
    Register Page Should Be Open
    Page Should Contain  ${message}